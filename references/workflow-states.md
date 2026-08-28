# Workflow states

Use the declared registry as the lifecycle index. A state describes the artifact in hand, not a remote account or audience-visible result.

| State | Meaning | Evidence required to enter |
| --- | --- | --- |
| `planned` | brief exists and scope is clear | content brief |
| `drafted` | copy or edit candidate exists | copy or edit package |
| `in_review` | reviewer has a bounded candidate | review request and candidate version |
| `changes_requested` | reviewer supplied actionable changes | review record |
| `approved_for_release` | candidate passed content review | scoped approval record |
| `awaiting_authorization` | account action needs a human decision | destination intent and requested scope |
| `released` | a human recorded a completed release | confirmed published identity and release evidence |
| `measuring` | release identity and window are confirmed | measurement plan |
| `analyzed` | findings are separated from raw observations | analysis brief |
| `blocked` | progress cannot continue safely | blocker description and owner |

## Discovery and audit outcomes

A discovery or audit must end with one of:

- `candidate`: usable input exists but has not been accepted as a release decision.
- `no_candidate`: nothing met the stated criteria.
- `blocker`: an unmet requirement, missing authority, or ambiguous evidence prevents a sound result.

These outcomes do not alter release status and must not create a competing ledger.
