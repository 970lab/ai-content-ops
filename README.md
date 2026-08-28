# AI Content Operations

This public skill package coordinates content-team artifacts from planning through feedback while keeping human authority at every external-action boundary.

## Included

- `SKILL.md`: routing, role handoffs, and core safety rules.
- `references/`: artifact, state, approval, and adapter contracts.
- `scripts/`: offline validators that read local JSON only.
- `examples/`: fictional artifact records.

## Quick check

```sh
python3 scripts/audit_pipeline.py examples/registry.example.json
python3 scripts/validate_metric_snapshot.py examples/metric_snapshot.example.json
```

The scripts do not connect to networks, interact with accounts, upload, publish, collect metrics, or modify declared targets. A valid package supports preparation and verification only; release actions still require current, scoped human authorization.

Both validators return `0` for a valid result, `2` for unreadable or malformed input, and `3` for contract or policy violations. With `--allow-partial`, the metric validator returns `0` but reports `"result": "partial"` and the `partial_allowed` warning; that output is not equivalent to a complete valid snapshot.

## Distribution note

The included MIT notice names the project collective "AI Content Operations contributors." A downstream distributor may replace that notice when its own legal policy requires it.

## Scope

Use replaceable adapters such as `filesystem`, `document_archive`, `object_storage`, `scheduler`, and `platform_metrics`. Keep source, archive, release, and metric evidence separate. Store one declared registry rather than starting a parallel ledger or database.
