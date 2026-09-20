# Delivery Evidence Check

“Done” is a claim. This small, offline Skill helps a reviewer ask what actually reached the recipient.

It contains six handoff questions and a dependency-free JSON validator. Unlike a website release gate, it also fits local documents and automation outputs: public access is required only when the packet makes a public delivery claim.

## Run

Requires Python 3.9 or later. No installation, network access or account is needed.

```sh
python3 scripts/validate.py examples/fictional-local.json --now 2026-01-01T13:00:00Z
python3 -m unittest discover -s tests -v
```

Run from this folder. Copy `templates/packet.json` to your existing project evidence area and replace its empty fields with actual observations. The template intentionally returns `blocker`. The fictional example returns `candidate`; it demonstrates the format, not a real delivery. The checker prints JSON and uses exit code 0 for `candidate`/`no_candidate`, 1 for `blocker` (including invalid input).

To use as an agent Skill, place this whole folder in your tool's supported Skill directory; the CLI also works independently. Start with [SKILL.md](SKILL.md), then the [packet contract](references/packet-contract.md).

## Limits

Evidence references are opaque labels: the checker never reads them, opens URLs, executes commands or verifies a claimed observation. Revision matches and timestamps can still be fabricated. A human must inspect the referenced evidence, choose a suitable freshness window and decide acceptance. This is not a security scanner, a deployment system or permission to publish.

## License

This package inherits the containing repository's MIT license, reproduced in [LICENSE](LICENSE) for independent distribution. It includes no third-party assets.
