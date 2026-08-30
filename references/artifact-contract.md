# Artifact contract

Each artifact is a portable, human-readable record. Store it in the team's declared source location and reference it from one registry; do not create a second ledger or database for the same lifecycle. A downstream artifact must name the exact upstream artifact IDs and versions it used, so an audit can detect a release/measurement chain that skips a required gate.

The registry is a lifecycle index, not a copy of each artifact. Each registry entry contains only its identity, current lifecycle state, and a safe relative `artifact_ref` to the complete artifact. The referenced artifact remains the source of truth for its full fields and evidence.

Every artifact includes:

- `artifact_type`, `artifact_id`, `version`, `owner_role`, and `status`.
- `created_at` and `updated_at` in an unambiguous timestamp format.
- `sources`, each with a provenance label: `fact`, `observation`, `judgment`, or `hypothesis`.
- `handoff_to` and a declared adapter target when a handoff is requested.
- `approval_refs` when a gate applies. A reference records an authorization decision; it is not a substitute for the decision itself.

Every registry summary includes `upstream_artifact_ids` and a matching `upstream_artifact_versions` map. A `content_brief` is the root of its chain, so both fields must be empty; it cannot cite a predecessor. A `release_package` that is `released` also includes a neutral `release_evidence_ref`; a package still waiting for the account-action decision remains `awaiting_authorization` and cannot be an upstream input to measurement.

The registry also holds adapter declarations for requested handoffs. See [adapter-contract.md](adapter-contract.md) for their required shape.

## Artifact types and role handoffs

| Type | Primary role | Minimum purpose | Typical next role |
| --- | --- | --- | --- |
| `content_brief` | planner | audience, objective, constraints, source distinctions | writer |
| `copy_package` | writer | proposed copy plus source-backed claims and open questions | editor |
| `edit_package` | editor | editable assets, edit notes, and quality checks | reviewer |
| `release_package` | release coordinator | approved candidate assets, destination intent, and gate references | authorized human |
| `metric_snapshot` | analyst | confirmed identity, time window, metric states, and provenance | analyst |
| `analysis_brief` | analyst | observations, judgments, hypotheses, and next experiments | planner |

## Statement discipline

- A `fact` is supported by a named source or approved record.
- An `observation` records what a person or permitted adapter saw, with its time and scope.
- A `judgment` is an evaluation and names its criteria.
- A `hypothesis` is testable but unproven and must name what evidence could change it.

Keep unresolved questions explicit. Do not encode passwords, session material, private personal data, or hidden account information in an artifact.
