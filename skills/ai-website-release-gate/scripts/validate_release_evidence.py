#!/usr/bin/env python3
"""Validate one local, JSON-compatible YAML website release evidence record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "ai-website-release-gate.v0.1"
LAYERS = ("source", "build", "runtime", "public_web", "browser_device", "status")
STOP_GATES = (
    "privacy_or_asset_rights_unknown",
    "production_identity_unproven",
    "indexing_policy_conflict",
    "unknown_path_returns_200",
    "critical_interaction_failed",
    "rollback_unavailable",
    "authorization_scope_unknown",
)


def assess(record: dict[str, Any]) -> dict[str, Any]:
    assessment = record.get("assessment")
    if not isinstance(assessment, dict) or assessment.get("object_type") != "website_release":
        return {"outcome": "no_candidate", "blockers": [], "reason": "input does not identify a website release object"}

    blockers: list[dict[str, str]] = []
    if record.get("schema") != SCHEMA:
        blockers.append({"field": "schema", "reason": f"expected {SCHEMA}"})

    layers = record.get("layers")
    if not isinstance(layers, dict):
        layers = {}
        blockers.append({"field": "layers", "reason": "must be an object"})
    for name in LAYERS:
        layer = layers.get(name)
        if not isinstance(layer, dict):
            blockers.append({"field": f"layers.{name}", "reason": "required layer is missing"})
            continue
        required = layer.get("required") is True
        state = layer.get("state")
        refs = layer.get("evidence_refs")
        if required and state != "passed":
            blockers.append({"field": f"layers.{name}.state", "reason": "required layer has not passed"})
        if required and (not isinstance(refs, list) or not any(isinstance(ref, str) and ref.strip() for ref in refs)):
            blockers.append({"field": f"layers.{name}.evidence_refs", "reason": "required layer has no evidence reference"})

    gates = record.get("stop_gates")
    if not isinstance(gates, dict):
        gates = {}
        blockers.append({"field": "stop_gates", "reason": "must be an object"})
    for gate in STOP_GATES:
        value = gates.get(gate)
        if value is True:
            blockers.append({"field": f"stop_gates.{gate}", "reason": "stop gate is active"})
        elif value is not False:
            blockers.append({"field": f"stop_gates.{gate}", "reason": "stop gate must be explicitly true or false"})

    rollback_ref = record.get("rollback_ref")
    if not isinstance(rollback_ref, str) or not rollback_ref.strip():
        blockers.append({"field": "rollback_ref", "reason": "an executable rollback reference is required"})

    if blockers:
        return {"outcome": "blocker", "blockers": blockers, "reason": "release evidence is incomplete or a stop gate is active"}
    return {
        "outcome": "candidate",
        "blockers": [],
        "reason": "evidence may enter human release review; this is not release authorization",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        raw = json.loads(args.record.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("root must be an object")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"outcome": "blocker", "blockers": [{"field": "record", "reason": str(exc)}]}, ensure_ascii=False, indent=2))
        return 2
    result = assess(raw)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["outcome"] in {"candidate", "no_candidate"} else 3


if __name__ == "__main__":
    raise SystemExit(main())

