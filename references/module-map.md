# Five-module workflow

The modules describe responsibilities, not fixed job titles or autonomous agents. One person may own several modules, and AI may assist inside a module, but every handoff is represented by an inspectable artifact.

| Module | Accepts | Produces | Must not claim |
| --- | --- | --- | --- |
| Source discovery | approved sources and public-scope rules | `content_brief`, then `copy_package` | that a candidate is approved or published |
| Asset production | approved copy and authorized source assets | `edit_package` | that a render is a platform draft or public release |
| Platform adaptation | frozen copy, approved assets, observed destination constraints | `release_package` | that upload or publication is authorized |
| Release control | reviewed release package and scoped human decision | release evidence and confirmed published identity | that a click, upload, or success message proves public availability |
| Measurement feedback | confirmed published identity and observation window | `metric_snapshot`, then `analysis_brief` | missing data as zero or a hypothesis as a finding |

## Handoff invariants

- A downstream module references the exact upstream artifact ID and version it used.
- Changes to approved claims return to source discovery; visual or platform operators do not silently rewrite them.
- A release package contains destination intent, not credentials or authority.
- Approval evidence and release evidence are separate records.
- Measurement begins only after the published identity is confirmed.
- Observations, judgments, and hypotheses remain distinguishable through the feedback loop.
- A single lifecycle example must not pair an `awaiting_authorization` release package with a `measuring` metric snapshot. Use separate pre-release and post-release examples, or update the release record to `released` with its own evidence reference first.

## Local integration

Keep one organization-owned registry as the lifecycle index. Local adapters may translate an existing ledger, archive, storage system, scheduler, or metric export into this contract without replacing the source system.

Local configuration may define brand rules, platform constraints, account aliases, storage targets, and authorization syntax. Do not commit credentials, private paths, customer data, or private platform identifiers to a public package.
