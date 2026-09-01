# AI Website Release Gate

An offline, evidence-based release review gate for websites built with AI assistance.

The package addresses a common failure mode: a page can build, open, or return HTTP 200 while the intended public version, mobile behavior, indexing policy, rollback path, or release record is still unproven. It keeps six evidence layers separate and returns one of three outcomes:

- `candidate`: ready to enter human release review;
- `blocker`: a required layer is incomplete or a stop gate is active;
- `no_candidate`: the input is not a website release assessment.

`candidate` is not permission to deploy or publish.

## Package contents

- `SKILL.md`: decision protocol and operating boundaries.
- `references/evidence-layers.md`: the six evidence layers and environment distinctions.
- `references/stop-gates.md`: conditions that stop release review.
- `templates/release-evidence.yaml`: a complete fictional record.
- `examples/`: fictional blocker and out-of-scope records.
- `scripts/validate_release_evidence.py`: dependency-free local validator.
- `tests/`: behavior tests for the three outcomes and evidence separation.

The `.yaml` fixtures use JSON syntax, which is valid YAML 1.2, so the validator can rely only on Python's standard library.

## Run locally

```sh
python3 scripts/validate_release_evidence.py templates/release-evidence.yaml
python3 scripts/validate_release_evidence.py examples/fictional-preview-indexing-blocker.yaml
python3 scripts/validate_release_evidence.py examples/fictional-no-rollback-blocker.yaml
python3 scripts/validate_release_evidence.py examples/fictional-no-candidate.yaml
python3 -m unittest discover -s tests -v
```

The validator reads one declared local record and writes a JSON decision to stdout. It makes no network requests and does not modify the input or any website.

## Integration

Use this as one bounded Skill inside a wider content or release-operations repository. Keep organization-specific domains, repository paths, account details, authorization wording, and platform configuration outside the portable package.

Before external distribution, apply the parent repository's license and security policy and review the complete Git history and staged diff. A clean package directory alone does not prove that a repository is safe to publish.

