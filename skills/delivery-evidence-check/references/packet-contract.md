# Packet contract v1

The root object has `schema_version: 1`, `claim` (`delivery` or `none`), `project`, `revision`, `audience` (`local` or `public`), and `evidence`.

For a delivery claim, evidence has exactly six rows: `source`, `checks`, `delivery`, `access`, `experience`, `record`. Each row contains the same `project` and `revision` as the root, a timezone-aware ISO 8601 `observed_at`, a nonempty opaque `ref`, and `result` (`observed`, `failed`, `unknown`). `access` additionally contains `surface` matching the root audience. It cannot be waived for a public claim.

`experience` contains `negative_path: observed` and `negative_ref` identifying the relevant safe failure check. When failure-path testing genuinely does not apply, use `negative_path: not-applicable` and a nonempty `negative_reason` (for example a static, noninteractive document). This exception is a reviewer's scoped decision, not a substitute for missing tests. A failed safety check must use `result: failed`, not `observed` merely because the failure was seen.

`record` requires `remaining_issues`, an explicit list of strings. An empty list means none recorded; missing means unknown and is blocked. A nonempty list returns `blocker` so the remaining work is reviewed rather than silently accepted. The tool does not decide whether a known issue can be deferred.

The CLI checks all timestamps against the current UTC time with a default 24-hour freshness window. Set `--max-age-hours` to the review's agreed window. `--now` allows deterministic fixture replay; it must not be used to disguise stale production evidence. Future observations are blocked. The window is a consistency check, not a universal release policy.

For `claim: none`, provide a nonempty `reason` and an empty evidence object; the outcome is `no_candidate`. Other root fields may be omitted. Missing evidence in an actual delivery claim is always a blocker, not `no_candidate`.

This intentionally compact contract does not model every domain. If an agreed review genuinely excludes a question, record that scoped decision in the authoritative handoff and review manually rather than filling fictional proof or weakening the checker. Build identities, device details and rollback checks can be described in the referenced evidence; they are not automatically verified by a matching revision string.
