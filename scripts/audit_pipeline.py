#!/usr/bin/env python3
"""Offline, read-only validation for a content lifecycle registry."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path

ARTIFACT_TYPES = {
    "content_brief", "copy_package", "edit_package", "release_package",
    "metric_snapshot", "analysis_brief",
}
ADAPTERS = {"filesystem", "document_archive", "object_storage", "scheduler", "platform_metrics"}
DIRECTIONS = {"export", "import", "observe"}
WORKFLOW_STATES = {
    "planned", "drafted", "in_review", "changes_requested",
    "approved_for_release", "awaiting_authorization", "released",
    "measuring", "analyzed", "blocked",
}
SENSITIVE_KEY = re.compile(r"(?:password|passwd|secret|token|api[_-]?key|credential|private[_-]?key)", re.I)
SUSPICIOUS_VALUE = re.compile(
    r"(?:-----BEGIN|bearer\s+|(?:api|access|auth)[_-]?token\s*[=:]|(?:password|secret|credential)\s*[=:]|AKIA[0-9A-Z]{12,})",
    re.I,
)
URI_LIKE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
WINDOWS_ABSOLUTE = re.compile(r"^[a-z]:[\\/]", re.I)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def safe_ref(value: object) -> bool:
    """Accept only neutral relative references; never resolve them."""
    if not nonempty(value):
        return False
    text = value.strip()
    if text.startswith(("/", "\\", "~")) or WINDOWS_ABSOLUTE.match(text) or URI_LIKE.match(text):
        return False
    return all(segment != ".." for segment in re.split(r"[\\/]", text))


def privacy_errors(value: object) -> list[str]:
    """Inspect structure without returning user-supplied values."""
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(key, str) and SENSITIVE_KEY.search(key):
                errors.append("sensitive_key_detected")
            errors.extend(privacy_errors(nested))
    elif isinstance(value, list):
        for nested in value:
            errors.extend(privacy_errors(nested))
    elif isinstance(value, str) and SUSPICIOUS_VALUE.search(value):
        errors.append("sensitive_value_detected")
    return errors


def artifact_path(base_dir: Path, reference: str) -> Path:
    """Resolve an already-validated portable reference below a local registry."""
    return base_dir / Path(reference.replace("\\", "/"))


def audit(registry: object, *, base_dir: Path | None = None, check_refs: bool = False) -> list[str]:
    """Return privacy-safe error codes; do not contact or mutate any target."""
    if not isinstance(registry, dict):
        return ["registry_not_object"]
    errors = privacy_errors(registry)
    if not nonempty(registry.get("registry_version")):
        errors.append("registry_version_missing")
    artifacts = registry.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return errors + ["artifacts_missing"]

    seen: set[str] = set()
    summaries: dict[str, dict] = {}
    for item in artifacts:
        if not isinstance(item, dict):
            errors.append("artifact_summary_not_object")
            continue
        artifact_id = item.get("artifact_id")
        if not nonempty(artifact_id):
            errors.append("artifact_id_missing")
        elif artifact_id in seen:
            errors.append("artifact_id_duplicate")
        else:
            seen.add(artifact_id)
            summaries[artifact_id] = item
        if item.get("artifact_type") not in ARTIFACT_TYPES:
            errors.append("artifact_type_invalid")
        for field in ("version", "owner_role", "status"):
            if not nonempty(item.get(field)):
                errors.append("artifact_summary_field_missing")
        if item.get("status") not in WORKFLOW_STATES:
            errors.append("artifact_status_invalid")
        if not safe_ref(item.get("artifact_ref")):
            errors.append("artifact_ref_invalid")
        elif check_refs and base_dir is not None and not artifact_path(base_dir, item["artifact_ref"]).is_file():
            errors.append("artifact_ref_missing")
        upstream = item.get("upstream_artifact_ids")
        if not isinstance(upstream, list) or any(not nonempty(source) for source in upstream):
            errors.append("artifact_upstream_invalid")
        else:
            versions = item.get("upstream_artifact_versions")
            if not isinstance(versions, dict) or set(versions) != set(upstream) or any(not nonempty(version) for version in versions.values()):
                errors.append("artifact_upstream_versions_invalid")

    expected_upstream_type = {
        "copy_package": "content_brief",
        "edit_package": "copy_package",
        "release_package": "edit_package",
        "metric_snapshot": "release_package",
        "analysis_brief": "metric_snapshot",
    }
    for artifact_id, item in summaries.items():
        upstream = item.get("upstream_artifact_ids")
        if not isinstance(upstream, list):
            continue
        if any(source not in seen for source in upstream):
            errors.append("artifact_upstream_unknown")
            continue
        upstream_summaries = [summaries[source] for source in upstream]
        declared_versions = item.get("upstream_artifact_versions")
        if isinstance(declared_versions, dict) and any(declared_versions.get(source) != summaries[source].get("version") for source in upstream):
            errors.append("artifact_upstream_version_mismatch")
        required_type = expected_upstream_type.get(item.get("artifact_type"))
        if required_type and not any(source.get("artifact_type") == required_type for source in upstream_summaries):
            errors.append("artifact_upstream_type_invalid")
        if item.get("artifact_type") == "release_package" and item.get("status") == "released":
            if not safe_ref(item.get("release_evidence_ref")):
                errors.append("release_evidence_missing")
        if item.get("artifact_type") == "metric_snapshot" and item.get("status") in {"measuring", "analyzed"}:
            releases = [source for source in upstream_summaries if source.get("artifact_type") == "release_package"]
            if not any(source.get("status") == "released" for source in releases):
                errors.append("measurement_before_confirmed_release")

    declarations = registry.get("adapter_declarations")
    if not isinstance(declarations, list):
        errors.append("adapter_declarations_missing")
        return errors
    for declaration in declarations:
        if not isinstance(declaration, dict):
            errors.append("adapter_declaration_not_object")
            continue
        if declaration.get("adapter") not in ADAPTERS:
            errors.append("adapter_invalid")
        if declaration.get("direction") not in DIRECTIONS:
            errors.append("adapter_direction_invalid")
        sources = declaration.get("source_artifact_ids")
        if not isinstance(sources, list) or not sources or any(not nonempty(source) for source in sources):
            errors.append("adapter_sources_invalid")
        elif any(source not in seen for source in sources):
            errors.append("adapter_source_unknown")
        if not safe_ref(declaration.get("target_ref")):
            errors.append("adapter_target_invalid")
        external_action = declaration.get("external_action")
        completed = declaration.get("operation_claimed_complete")
        if not isinstance(external_action, bool) or not isinstance(completed, bool):
            errors.append("adapter_action_flags_invalid")
            continue
        if external_action and not safe_ref(declaration.get("authorization_ref")):
            errors.append("adapter_authorization_missing")
        if declaration.get("direction") == "observe" or completed:
            if not safe_ref(declaration.get("evidence_ref")):
                errors.append("adapter_evidence_missing")
    return errors


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def self_test() -> int:
    valid = {
        "registry_version": "1",
        "artifacts": [{"artifact_type": "content_brief", "artifact_id": "brief-1", "version": "v1", "owner_role": "planner", "status": "planned", "artifact_ref": "artifacts/brief-1.yaml", "upstream_artifact_ids": [], "upstream_artifact_versions": {}}],
        "adapter_declarations": [{"adapter": "filesystem", "direction": "export", "source_artifact_ids": ["brief-1"], "target_ref": "handoffs/briefs", "external_action": False, "operation_claimed_complete": False}],
    }
    assert audit(valid) == []
    invalid_adapter = json.loads(json.dumps(valid))
    invalid_adapter["adapter_declarations"][0].update({"adapter": "platform_metrics", "direction": "observe", "external_action": True})
    assert {"adapter_authorization_missing", "adapter_evidence_missing"}.issubset(audit(invalid_adapter))
    for unsafe_target in ("/private/location", "../escape", "custom:reference"):
        unsafe_ref = json.loads(json.dumps(valid))
        unsafe_ref["adapter_declarations"][0]["target_ref"] = unsafe_target
        assert "adapter_target_invalid" in audit(unsafe_ref)
    sensitive = json.loads(json.dumps(valid))
    sensitive["access_token"] = "Bearer fictional-value"
    assert {"sensitive_key_detected", "sensitive_value_detected"}.issubset(audit(sensitive))
    with tempfile.TemporaryDirectory() as temporary:
        base_dir = Path(temporary)
        artifacts = base_dir / "artifacts"; artifacts.mkdir()
        (artifacts / "brief-1.yaml").write_text("fictional artifact\n", encoding="utf-8")
        path = base_dir / "registry.json"
        path.write_text(json.dumps(valid), encoding="utf-8")
        assert audit(load_json(path), base_dir=base_dir, check_refs=True) == []
        (artifacts / "brief-1.yaml").unlink()
        assert "artifact_ref_missing" in audit(load_json(path), base_dir=base_dir, check_refs=True)
    invalid_measurement = {
        "registry_version": "1",
        "artifacts": [
            valid["artifacts"][0],
            {"artifact_type": "copy_package", "artifact_id": "copy-1", "version": "v1", "owner_role": "writer", "status": "drafted", "artifact_ref": "artifacts/copy-1.yaml", "upstream_artifact_ids": ["brief-1"], "upstream_artifact_versions": {"brief-1": "v1"}},
            {"artifact_type": "edit_package", "artifact_id": "edit-1", "version": "v1", "owner_role": "editor", "status": "in_review", "artifact_ref": "artifacts/edit-1.yaml", "upstream_artifact_ids": ["copy-1"], "upstream_artifact_versions": {"copy-1": "v1"}},
            {"artifact_type": "release_package", "artifact_id": "release-1", "version": "v1", "owner_role": "release_coordinator", "status": "awaiting_authorization", "artifact_ref": "artifacts/release-1.yaml", "upstream_artifact_ids": ["edit-1"], "upstream_artifact_versions": {"edit-1": "v1"}},
            {"artifact_type": "metric_snapshot", "artifact_id": "metrics-1", "version": "v1", "owner_role": "analyst", "status": "measuring", "artifact_ref": "artifacts/metrics-1.json", "upstream_artifact_ids": ["release-1"], "upstream_artifact_versions": {"release-1": "v1"}},
        ],
        "adapter_declarations": [],
    }
    assert "measurement_before_confirmed_release" in audit(invalid_measurement)
    print(json.dumps({"result": "self_test_passed", "checks": 8}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a local registry without contacting targets.")
    parser.add_argument("registry", nargs="?", type=Path, help="Local JSON registry path")
    parser.add_argument("--self-test", action="store_true", help="Run offline checks")
    parser.add_argument("--check-refs", action="store_true", help="Require artifact_ref files to exist below the local registry directory")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.registry is None:
        parser.error("registry is required unless --self-test is used")
    try:
        errors = audit(load_json(args.registry), base_dir=args.registry.parent, check_refs=args.check_refs)
    except (OSError, json.JSONDecodeError):
        print(json.dumps({"result": "invalid_input", "errors": ["registry_unreadable"]}))
        return 2
    summary = {"result": "valid" if not errors else "invalid", "error_count": len(errors), "errors": sorted(set(errors))}
    print(json.dumps(summary, sort_keys=True))
    return 0 if not errors else 3


if __name__ == "__main__":
    raise SystemExit(main())
