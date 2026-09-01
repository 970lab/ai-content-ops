---
name: ai-website-release-gate
description: Assess whether an AI-built website has enough separate evidence to enter human release review. Use before a website launch or deployment handoff; do not use it to deploy, change DNS, submit indexing, or operate accounts.
---

# AI Website Release Gate

Use this skill when a website appears finished and the team needs a source-bound decision about whether it may enter human release review.

## Required input

Read a declared release-evidence record that identifies one website candidate and keeps these six layers separate:

1. `source`: the intended change exists in the reviewed source.
2. `build`: the exact release artifact was built and contains the change.
3. `runtime`: the artifact runs in the intended local or preview environment.
4. `public_web`: the intended public version, URL, response, metadata, and indexing state were read back.
5. `browser_device`: required browser, viewport, interaction, and device checks passed.
6. `status`: release state, evidence, unresolved work, and rollback reference were written back.

Read [references/evidence-layers.md](references/evidence-layers.md) when preparing or reviewing the record. Read [references/stop-gates.md](references/stop-gates.md) when any evidence is missing, contradictory, private, or unsafe.

## Decision protocol

Return exactly one outcome:

- `candidate`: every required layer has evidence and no stop gate is active. This means only that the package may enter human release review.
- `blocker`: the object is in scope, but a required layer is incomplete or a stop gate is active. List the affected layers and missing or conflicting evidence.
- `no_candidate`: the input does not identify a website release object or contains no release assessment to perform.

Never treat a successful build, HTTP 200, screenshot, test pass, or local preview as proof of the other layers. Never turn `candidate` into release authorization.

## Offline validation

Run:

```sh
python3 scripts/validate_release_evidence.py templates/release-evidence.yaml
```

The template and examples use JSON syntax inside YAML-compatible files so the validator remains dependency-free. It reads local files only and never changes a website or account.

## Boundaries

- Do not deploy, upload, publish, modify DNS, change access control, submit a sitemap, request indexing, or rotate credentials.
- Do not infer authorization from an approval note created for a different action.
- Do not expose private URLs, credentials, customer data, family data, internal topology, or local absolute paths in a public package.
- Keep Preview and Production evidence distinct. A public response does not prove that the intended build is live.
- Require an executable rollback reference; destructive cleanup is not rollback.

