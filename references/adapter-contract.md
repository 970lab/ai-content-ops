# Adapter contract

Adapters are replaceable boundaries for moving or observing declared artifacts. They do not grant access, retain credentials, or turn an intent into a completed action.

Supported adapter names are `filesystem`, `document_archive`, `object_storage`, `scheduler`, and `platform_metrics`. Teams may add a neutral adapter name only when its direction, inputs, outputs, and authorization boundary are documented.

Every adapter declaration contains:

- `adapter`: the adapter name.
- `direction`: `export`, `import`, or `observe`.
- `source_artifact_ids`: declared artifact identifiers.
- `target_ref`: a non-secret target description controlled by the team.
- `external_action`: boolean; set `true` for account interaction, upload, scheduling, publication, or other external mutation.
- `authorization_ref`: required when `external_action` is `true`.
- `evidence_ref`: required for `observe` and whenever `operation_claimed_complete` is `true`.
- `operation_claimed_complete`: boolean; use only when a completed operation is being asserted.

References must be neutral relative identifiers. Do not use absolute paths, URLs, traversal segments, secrets, or credentials.

## Boundary rules

- `filesystem`, `document_archive`, and `object_storage` may represent one-way artifact handoffs; they are not a synchronization claim.
- `scheduler` may represent a requested reminder or job definition, not an autonomous authorization to release.
- `platform_metrics` is observation-only and may run only after the published identity and window are confirmed.
- A release-facing adapter must stop before account interaction unless the current, scoped human authorization is present.
- Preserve source, archive, release, and metric evidence as distinct records.
