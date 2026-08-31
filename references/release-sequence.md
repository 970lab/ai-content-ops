# Release sequence and declared discovery

Use this optional registry section when one batch crosses more than one public surface or when a discovery pass is requested. Its names are team-defined configuration, so this package does not encode repository hosts, site domains, social platforms, account identities, or approval-token syntax.

## Ordered public surfaces

`release_sequence.required_stages` is the only allowed order for the batch. Each item in `release_sequence.stages` has the same `name`, in the same order, and a state of `pending`, `awaiting_authorization`, `authorized`, `confirmed`, or `blocked`.

- `pending` and `awaiting_authorization` explicitly have no authorization decision. Do not add an `authorization_ref` until a human has decided.
- `authorized` is only for an external action with a neutral relative `authorization_ref`; it records the decision, not the completed action.
- A `confirmed` stage requires a neutral relative `evidence_ref`. If it is an external action, it also requires the distinct `authorization_ref` that permitted it.
- Every stage declares `external_action`. Confirmed local registration, measurement, or review may set it to `false`; their evidence remains separate from an external publication's evidence.
- Once a stage is not confirmed, every later stage must remain unconfirmed. A scoped approval never repairs missing upstream evidence.
- Put registration after the confirmed distribution identity, then measurement, then review when those stages are in scope. Each stage records its own evidence; the sequence is a gate report, not a second ledger.

A typical local configuration might name stages `source_publication`, `site_publication`, `distribution`, `registration`, `measurement`, and `review`. Teams may use different neutral names when their workflow requires them.

## Explicit discovery allowlist

When `discovery` is present, set `mode` to `allowlist`, list only the source references that may be inspected, and record the single outcome: `candidate`, `no_candidate`, or `blocker`.

Each source has a stable `source_id`, neutral relative `source_ref`, `change_state` (`changed`, `unchanged`, or `unknown`), and a neutral relative `change_evidence_ref`. The allowlist is not a path prefix and does not authorize recursive discovery. The caller decides how to check an allowlisted source for change; this package only validates the declared boundary.

An `unknown` source state forces the discovery outcome to `blocker`. A `candidate` requires at least one `changed` source. When every allowlisted source is `unchanged`, `no_candidate` is the normal result.
