# AI Content Operations

This public skill package coordinates content-team artifacts from planning through feedback while keeping human authority at every external-action boundary.

It was distilled from a workflow used for real content operations, then deidentified and separated from local paths, accounts, credentials, brand policy, and platform-specific settings. It is most useful when copywriters, visual editors, release coordinators, and analysts need AI-assisted handoffs that remain inspectable outside a chat window.

## Five-module workflow

1. **Source discovery** turns approved source material into a traceable `content_brief` or `copy_package`.
2. **Asset production** records editable visual or video work in an `edit_package` without changing approved claims.
3. **Platform adaptation** assembles a destination-ready `release_package` and exposes every required adaptation.
4. **Release control** stops at the human authorization boundary and records release evidence separately from approval.
5. **Measurement feedback** records a `metric_snapshot`, then separates observation from interpretation in an `analysis_brief`.

See `references/module-map.md` and `examples/full-lifecycle.example.json` for the complete handoff chain.

## Included

- `SKILL.md`: routing, role handoffs, and core safety rules.
- `references/`: artifact, state, approval, and adapter contracts.
- `scripts/`: offline validators that read local JSON only.
- `examples/`: fictional artifact records.

## Quick check

```sh
python3 scripts/audit_pipeline.py examples/registry.example.json --check-refs
python3 scripts/audit_pipeline.py examples/full-lifecycle.example.json --check-refs
python3 scripts/validate_metric_snapshot.py examples/metric_snapshot.example.json
```

The scripts do not connect to networks, interact with accounts, upload, publish, collect metrics, or modify declared targets. A valid package supports preparation and verification only; release actions still require current, scoped human authorization.

Both validators return `0` for a valid result, `2` for unreadable or malformed input, and `3` for contract or policy violations. With `--allow-partial`, the metric validator returns `0` but reports `"result": "partial"` and the `partial_allowed` warning; that output is not equivalent to a complete valid snapshot.

## Distribution note

The included MIT notice names the project collective "AI Content Operations contributors." A downstream distributor may replace that notice when its own legal policy requires it.

## Scope

Use replaceable adapters such as `filesystem`, `document_archive`, `object_storage`, `scheduler`, and `platform_metrics`. Keep source, archive, release, and metric evidence separate. Store one declared registry rather than starting a parallel ledger or database.

Platform rules belong in a team's local configuration. This repository intentionally does not prescribe page counts, hashtag counts, account identities, storage mounts, or vendor-specific authorization wording.

`examples/registry.example.json` is deliberately pre-release: it stops at `awaiting_authorization`. `examples/full-lifecycle.example.json` is a separate fictional post-release chain. Its referenced artifacts are included, its release record is `released` with neutral evidence, and only then does measurement begin.
