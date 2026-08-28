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


def audit(registry: object) -> list[str]:
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
        if item.get("artifact_type") not in ARTIFACT_TYPES:
            errors.append("artifact_type_invalid")
        for field in ("version", "owner_role", "status"):
            if not nonempty(item.get(field)):
                errors.append("artifact_summary_field_missing")
        if not safe_ref(item.get("artifact_ref")):
            errors.append("artifact_ref_invalid")

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
        "artifacts": [{"artifact_type": "content_brief", "artifact_id": "brief-1", "version": "v1", "owner_role": "planner", "status": "planned", "artifact_ref": "artifacts/brief-1.yaml"}],
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
        path = Path(temporary) / "registry.json"
        path.write_text(json.dumps(valid), encoding="utf-8")
        assert audit(load_json(path)) == []
    print(json.dumps({"result": "self_test_passed", "checks": 6}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a local registry without contacting targets.")
    parser.add_argument("registry", nargs="?", type=Path, help="Local JSON registry path")
    parser.add_argument("--self-test", action="store_true", help="Run offline checks")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.registry is None:
        parser.error("registry is required unless --self-test is used")
    try:
        errors = audit(load_json(args.registry))
    except (OSError, json.JSONDecodeError):
        print(json.dumps({"result": "invalid_input", "errors": ["registry_unreadable"]}))
        return 2
    summary = {"result": "valid" if not errors else "invalid", "error_count": len(errors), "errors": sorted(set(errors))}
    print(json.dumps(summary, sort_keys=True))
    return 0 if not errors else 3


if __name__ == "__main__":
    raise SystemExit(main())
