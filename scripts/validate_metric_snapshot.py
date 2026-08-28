#!/usr/bin/env python3
"""Offline validation for an unambiguous metric snapshot."""

from __future__ import annotations

import argparse
import copy
import json
import math
import tempfile
from datetime import datetime
from pathlib import Path

METRIC_STATES = {"observed", "zero", "unavailable", "immature"}
PROVENANCE_KINDS = {"fact", "observation", "judgment", "hypothesis"}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def parse_timestamp(value: object) -> datetime | None:
    if not nonempty(value):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def validate(snapshot: object, allow_partial: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(snapshot, dict):
        return ["snapshot_not_object"], warnings
    if snapshot.get("artifact_type") != "metric_snapshot":
        errors.append("artifact_type_invalid")
    for field in ("artifact_id", "version", "owner_role", "status"):
        if not nonempty(snapshot.get(field)):
            errors.append("artifact_identity_field_missing")
    created_at = parse_timestamp(snapshot.get("created_at"))
    updated_at = parse_timestamp(snapshot.get("updated_at"))
    if created_at is None or updated_at is None or updated_at < created_at:
        errors.append("artifact_timestamp_invalid")
    sources = snapshot.get("sources")
    if not isinstance(sources, list) or not sources or any(not isinstance(source, dict) or source.get("kind") not in PROVENANCE_KINDS or not nonempty(source.get("statement")) for source in sources):
        errors.append("sources_invalid")
    if "approval_refs" in snapshot and (not isinstance(snapshot["approval_refs"], list) or any(not nonempty(ref) for ref in snapshot["approval_refs"])):
        errors.append("approval_refs_invalid")

    identity = snapshot.get("published_identity")
    if not isinstance(identity, dict) or identity.get("confirmed") is not True or not nonempty(identity.get("reference")):
        errors.append("published_identity_unconfirmed")
    window = snapshot.get("measurement_window")
    start = end = None
    if not isinstance(window, dict) or not nonempty(window.get("timezone")):
        errors.append("window_invalid")
    else:
        start = parse_timestamp(window.get("start"))
        end = parse_timestamp(window.get("end"))
        if start is None or end is None:
            errors.append("window_invalid")
        elif start >= end:
            errors.append("window_order_invalid")
    collection = snapshot.get("collection")
    observed_at = None
    if not isinstance(collection, dict) or collection.get("adapter") != "platform_metrics" or not nonempty(collection.get("evidence_ref")):
        errors.append("collection_invalid")
    else:
        observed_at = parse_timestamp(collection.get("observed_at"))
        if observed_at is None:
            errors.append("collection_timestamp_invalid")
        elif start is not None and observed_at < start:
            errors.append("collection_before_window")

    metrics = snapshot.get("metrics")
    if not isinstance(metrics, dict) or not metrics:
        errors.append("metrics_missing")
    else:
        for name, entry in metrics.items():
            if not nonempty(name) or not isinstance(entry, dict):
                errors.append("metric_invalid")
                continue
            state = entry.get("state")
            if state not in METRIC_STATES:
                errors.append("metric_state_invalid")
            elif state == "observed":
                value = entry.get("value")
                if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value <= 0:
                    errors.append("observed_value_invalid")
            elif state == "zero":
                value = entry.get("value")
                if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value != 0:
                    errors.append("zero_value_invalid")
            else:
                if "value" in entry:
                    errors.append("non_numeric_state_has_value")
                if not nonempty(entry.get("reason")):
                    errors.append("metric_reason_missing")

    partial = snapshot.get("partial") is True or snapshot.get("complete") is not True
    if partial:
        if allow_partial:
            warnings.append("partial_allowed")
        else:
            errors.append("partial_or_ambiguous")
    return errors, warnings


def result_name(errors: list[str], warnings: list[str]) -> str:
    if errors:
        return "invalid"
    return "partial" if warnings else "valid"


def exit_code(errors: list[str]) -> int:
    return 0 if not errors else 3


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def self_test() -> int:
    valid = {
        "artifact_type": "metric_snapshot", "artifact_id": "metrics-1", "version": "v1", "owner_role": "analyst", "status": "measuring",
        "created_at": "2030-01-02T01:00:00Z", "updated_at": "2030-01-02T01:00:00Z", "complete": True,
        "sources": [{"kind": "observation", "statement": "A permitted observation recorded the sample states."}], "approval_refs": ["approvals/metric-1"],
        "published_identity": {"confirmed": True, "reference": "fictional-item-1"},
        "measurement_window": {"start": "2030-01-01T00:00:00Z", "end": "2030-01-02T00:00:00Z", "timezone": "UTC"},
        "collection": {"adapter": "platform_metrics", "observed_at": "2030-01-02T01:00:00Z", "evidence_ref": "evidence/metric-1"},
        "metrics": {"views": {"state": "observed", "value": 12}, "shares": {"state": "zero", "value": 0}, "replies": {"state": "immature", "reason": "Window is not mature."}},
    }
    errors, warnings = validate(valid)
    assert errors == [] and warnings == []
    bad_window = copy.deepcopy(valid)
    bad_window["measurement_window"]["end"] = bad_window["measurement_window"]["start"]
    assert "window_order_invalid" in validate(bad_window)[0]
    observed_zero = copy.deepcopy(valid)
    observed_zero["metrics"]["views"]["value"] = 0
    assert "observed_value_invalid" in validate(observed_zero)[0]
    nonfinite = copy.deepcopy(valid)
    nonfinite["metrics"]["views"]["value"] = json.loads("NaN")
    assert "observed_value_invalid" in validate(nonfinite)[0]
    missing_reason = copy.deepcopy(valid)
    del missing_reason["metrics"]["replies"]["reason"]
    assert "metric_reason_missing" in validate(missing_reason)[0]
    partial = copy.deepcopy(valid)
    partial["complete"] = False
    default_partial_errors, _ = validate(partial)
    assert "partial_or_ambiguous" in default_partial_errors and exit_code(default_partial_errors) == 3
    partial_errors, partial_warnings = validate(partial, allow_partial=True)
    assert partial_errors == [] and partial_warnings == ["partial_allowed"] and result_name(partial_errors, partial_warnings) == "partial" and exit_code(partial_errors) == 0
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "snapshot.json"
        path.write_text(json.dumps(valid), encoding="utf-8")
        assert validate(load_json(path))[0] == []
    print(json.dumps({"result": "self_test_passed", "checks": 8}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a local metric snapshot without collecting metrics.")
    parser.add_argument("snapshot", nargs="?", type=Path, help="Local metric snapshot JSON path")
    parser.add_argument("--allow-partial", action="store_true", help="Permit explicit partial data and report it as partial")
    parser.add_argument("--self-test", action="store_true", help="Run offline checks")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.snapshot is None:
        parser.error("snapshot is required unless --self-test is used")
    try:
        errors, warnings = validate(load_json(args.snapshot), args.allow_partial)
    except (OSError, json.JSONDecodeError):
        print(json.dumps({"result": "invalid_input", "errors": ["snapshot_unreadable"]}))
        return 2
    summary = {"result": result_name(errors, warnings), "error_count": len(errors), "errors": sorted(set(errors)), "warnings": sorted(set(warnings))}
    print(json.dumps(summary, sort_keys=True))
    return exit_code(errors)


if __name__ == "__main__":
    raise SystemExit(main())
