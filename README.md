# AI Content Operations

A practical workflow for turning real work into content with AI assistance and human editorial judgment.

Use it to take one reader question from sources to a complete text draft, or to a coherent title, cover and script with actual media when that format is appropriate. Continue to destination review and recorded release only when requested. You can start with a text editor and an AI tool you already use. Python is optional for the offline checks.

**Creator guide — 2026-10-29:** start with one text draft, then add only the media and destinations you need. This package does not provide automatic account login, uploading, publishing, media generation or analytics collection. External-user onboarding has not yet been validated.

Read [the workflow in ten simple steps](docs/workflow-at-a-glance.md) for the full path from a real story to publication and review.

## Start here

1. Follow [Start with one post](docs/quickstart.md). The default is a complete text draft; no media or code needed.
2. Use the [six-section starter](templates/first-post.md) and [one copy-paste prompt](templates/start-here-prompt.txt).
3. If you want a practice run first, use the [included source note](examples/first-post/source-note.md), then compare the [completed draft](examples/first-post/draft.md).

The repository instructions are in English; the starting prompt can produce content in your chosen language. Understanding the English guide and producing another language are separate usability questions.

You only need one current draft and its source folder. No registry, artifact IDs or historical checkpoints are required for your first manually supplied story. Use the [advanced worksheet](templates/content-worksheet.md) when you actually need media, multiple destinations or team handoffs. Existing teams keep their own lifecycle index; do not create a second ledger.

## What you get

| Need | Included resource |
| --- | --- |
| Keep your own voice and avoid invented experiences | [Editorial guide](docs/editorial-guide.md) |
| Recover from wrong facts, missing footage or unreliable UI interactions | [Lessons and recovery](docs/lessons-and-recovery.md) |
| Choose tools and understand costs | [Tools and boundaries](docs/tools-and-costs.md) |
| Verify someone else can use it | [External trial checklist](docs/external-trial.md) |
| Inspect structured handoffs and lifecycle evidence | [Artifact contract](references/artifact-contract.md), [states](references/workflow-states.md), [module map](references/module-map.md) |
| Declare only the public surfaces actually needed | [Release sequence](references/release-sequence.md) |
| Review a website release or other delivery | [Website release gate](skills/ai-website-release-gate/README.md), [delivery evidence check](skills/delivery-evidence-check/README.md) |

## Five responsibilities, flexible tools

Source discovery → asset production → platform adaptation → release control → measurement feedback.

One person can hold several roles. AI can help extract claims, draft and check consistency; the author owns the experience, angle and final voice. A reviewer checks claims and actual media. An authorized operator handles external actions. These roles do not require multiple paid subscriptions or separate agents.

This workflow was distilled from real content operations. The [lesson notes](docs/lessons-and-recovery.md) paraphrase observed problems without exposing private source material. All sample projects, metrics and release receipts in this repository are **fictional teaching examples**, not evidence of actual publication or audience performance.

## Optional offline checks

From the repository root, with Python 3.10 or newer:

```bash
python3 scripts/audit_pipeline.py examples/registry.example.json --check-refs
python3 scripts/audit_pipeline.py examples/full-lifecycle.example.json --check-refs
python3 scripts/audit_pipeline.py examples/release-sequence.example.json
python3 scripts/validate_metric_snapshot.py examples/metric_snapshot.example.json
```

These scripts use the Python standard library. They do not connect to networks, interact with accounts, upload, publish, collect metrics or modify declared targets. A successful check proves only the checks implemented by that validator, not factual accuracy, creative quality, rights, audience access or live adapter functionality.

Both validators use exit code `0` for a valid result, `2` for unreadable or malformed input, and `3` for contract or policy violations. With `--allow-partial`, the metric validator can return `0` with `result: partial`; inspect the result and warnings.

## Scope and reuse

The core remains usable without a paid service from this project. You bring any necessary model subscriptions, editing tools, storage and platform accounts; their charges and terms are separate. No hosted service or paid support plan is offered by this repository.

Adapters are contracts for replaceable integrations, not shipped account connectors. Keep brand, language, platform constraints, storage locations and authorization preferences in local configuration. The portable package does not require every creator to publish to GitHub, a website and social media.

[MIT](LICENSE) applies to included code and documentation under the existing notice. It does not grant rights to third-party media, private case evidence, personal voices or likenesses. See [security](SECURITY.md) and [candidate changes](CHANGELOG.md).
