# Stop gates

The validator returns `blocker` when any active stop gate is true.

- `privacy_or_asset_rights_unknown`: privacy, content ownership, or asset authorization is unresolved.
- `production_identity_unproven`: the public version cannot be tied to the intended release artifact.
- `indexing_policy_conflict`: canonical, robots, sitemap, headers, access state, or the intended indexing decision conflict.
- `unknown_path_returns_200`: an unknown route incorrectly returns successful page content instead of a real not-found response.
- `critical_interaction_failed`: navigation, mobile menu, deep link, form, focus, or another release-critical interaction fails.
- `rollback_unavailable`: there is no executable version or snapshot to restore.
- `authorization_scope_unknown`: the proposed external action lacks a current, scoped human decision.

These gates are intentionally conservative. A team may add stricter project gates, but should not remove a gate silently. If a gate is not applicable, record `false` and explain the scope in evidence rather than omitting the field.

