---
name: ai-content-ops
description: Coordinate deidentified, approval-gated content operations across briefs, editing, review, release evidence, metrics, and feedback without operating accounts or treating drafts as releases.
---

# AI Content Operations

Use this skill to organize a content team's handoffs when several roles contribute to one release and evidence must remain traceable. It creates or audits interoperable artifacts; it does not log in to accounts, upload, publish, scrape private information, or automate platform actions.

The workflow has five modules: source discovery, asset production, platform adaptation, release control, and measurement feedback. A small team may assign one person to several modules; the artifact boundary stays the same so work can move between people or AI sessions without relying on chat history.

## Route the request

- For required artifact shapes and role handoffs, read [references/artifact-contract.md](references/artifact-contract.md).
- For the five-module workflow and its artifact handoffs, read [references/module-map.md](references/module-map.md).
- For lifecycle status or discovery/audit outcomes, read [references/workflow-states.md](references/workflow-states.md).
- For a multi-surface release or a discovery pass, read [references/release-sequence.md](references/release-sequence.md).
- Before any account interaction, upload, or publication, read [references/approval-gates.md](references/approval-gates.md).
- For an integration request, read [references/adapter-contract.md](references/adapter-contract.md). Adapters exchange declared artifacts only; they do not imply connectivity or authority.

## Operating rules

1. Start local-first: make each artifact inspectable before proposing a one-way handoff. Keep synchronization, archival, publication, and measurement as separate evidence layers.
2. Use exactly these artifact types: `content_brief`, `copy_package`, `edit_package`, `release_package`, `metric_snapshot`, and `analysis_brief`.
3. Label statements as `fact`, `observation`, `judgment`, or `hypothesis`. Do not silently promote one kind to another.
4. A discovery or audit concludes only `candidate`, `no_candidate`, or `blocker`; do not create a parallel ledger or database to replace the declared registry.
5. A human must give scoped authorization immediately before any upload, publication, or account interaction. A prepared `release_package` is not proof of release.
6. Collect metrics only after a confirmed published identity and measurement window exist. Record each metric as `observed`, `zero`, `unavailable`, or `immature`; never infer a zero from missing data.
7. Keep organization-specific paths, brand rules, platform limits, topic counts, account names, and approval tokens in local configuration. Do not bake them into the portable workflow contract.
8. When a batch has several public surfaces, declare their order and evidence in a `release_sequence`. `pending` and `awaiting_authorization` are not authorization; an external action is only authorized by a distinct current decision reference, and only confirmed by separate evidence.
9. Discovery inspects only explicitly declared source references. Each has change/checkpoint evidence; `unknown` is a blocker, and the allowlist never expands into a recursive workspace scan.

## Helpers

Run `scripts/audit_pipeline.py` against a declared registry to inspect artifact completeness without contacting a network or changing targets. Run `scripts/validate_metric_snapshot.py` before accepting a metric snapshot; it rejects partial or ambiguous data unless `--allow-partial` is explicit.

Examples are fictional and illustrate formats, not real results or authorization.
