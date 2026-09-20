# Evidence layers

Each required layer has `required`, `state`, and `evidence_refs`. A required layer passes only when `state` is `passed` and at least one neutral evidence reference is present.

| Layer | What it proves | What it does not prove |
| --- | --- | --- |
| `source` | The reviewed source contains the intended change. | A deployable artifact exists. |
| `build` | The exact release artifact was produced and inspected. | The artifact runs or is public. |
| `runtime` | That artifact operates in a declared local or preview runtime. | Production serves the same artifact. |
| `public_web` | The formal URL and public response were read back with the expected version and environment policy. | Mobile interactions and device behavior pass. |
| `browser_device` | Declared browsers, viewports, interactions, and required devices were checked. | Status records and rollback are current. |
| `status` | The release record names the version, time, evidence, open items, and rollback reference. | A human authorized the external action. |

Evidence references should be inspectable but portable, such as a commit identifier, artifact digest, test report, public URL, screenshot manifest, device report, or release record. Public examples must be fictional and must not contain local paths or private infrastructure.

## Environment identity

The `public_web` layer should show which environment was read back and how it was tied to the intended artifact. Keep these states distinct:

- local or development;
- private Preview;
- public Preview with indexing disabled;
- Production with indexing disabled by an explicit decision;
- Production open to indexing by an explicit decision.

Robots rules, canonical URLs, sitemap contents, access policy, and the declared environment must agree. An HTTP 200 alone is insufficient.

