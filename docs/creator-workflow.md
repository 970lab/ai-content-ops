# From real work to a published item

This is the human operating guide for the existing five-module contract. The steps below describe a complete path; completion is recorded per step and per destination. A reusable process can be complete while a particular story correctly waits for footage.

## 1. Discover a useful story

**Input:** a declared list of permitted source notes and their change checkpoints.

Read changed sources only. Ask: what can a reader learn, repeat or avoid? Return `candidate`, `no_candidate` or `blocker`. No meaningful new evidence is a valid `no_candidate`, not a reason to invent a daily post. Unknown source state is a blocker for that discovery decision.

**Output:** `content_brief` with audience question, takeaway, author angle, claim sources, public boundaries and unknowns. Discovery does not require scanning all projects or private history.

## 2. Shape one story with the author

Start from what the author wants to say. A technical log supplies facts; it does not determine the emotional focus. Use one concrete tension or contrast supported by the result. Write title, cover text and opening together before polishing the body.

**Output:** `copy_package` containing selected copy, claim links, editorial notes and open questions. A reviewer checks both truth and voice. If the author changes the angle, update all three entry points together. Do not carry stale claims into the new version.

## 3. Collect and produce the actual media

Turn the script into a shot list. Match every important visible claim with a corresponding current clip or image. Reuse permitted historical footage only with its actual time/version context. Label CAD renders, mockups, reconstructions and generated illustrations accurately; they cannot prove physical testing or a real event.

Create the cover, edit, captions and audio using the tools available to the creator. For downloadable attachments, check both hash/size identity and format validity with an appropriate reader; verify that the named version matches the actual content. Record third-party asset rights and any consent required for voices or likenesses. Check the first frame, readable text, crop, sound and ending at the intended viewing size. Spoken duration becomes measured only after an actual recording.

**Output:** `edit_package` referencing the exact copy revision, editable source, export revision and review. Missing footage leaves the item `drafted` with an action owner, or `blocked` if no useful progress remains. Do not make generated media stand in for evidence.

## 4. Adapt to each chosen destination

Choose destinations because they fit the audience and evidence. Record language, format, link destination, title, description, tags, accessibility text and disclosure needs. Verify current platform requirements at the time of use; this repository does not freeze them as universal rules.

For multilingual work, adapt wording naturally while preserving the same supported claims. Check the actual visible language of images and link cards, not just the text or URL. If a channel does not fit, leave it out of the distribution plan.

**Output:** one `release_package` per relevant destination, or a package with separately inspectable destination sections. It includes approved assets and intended actions, not account credentials. Link each to the exact `edit_package` revision.

## 5. Review the concrete candidate and execute the authorized action

Review content, assets, rights, privacy and destination identity. The author can approve only a draft, only upload, a scheduled release or publication; record the actual scope, version and destination. Reuse a still-valid scoped authorization rather than repeatedly asking the same question. A changed claim, asset or destination needs its affected review revisited.

Before each external action, confirm that the recorded authorization covers that exact action. The repository itself performs no external actions. An authorized human or separately configured permitted tool uses the platform's official workflow.

Record the platform receipt: project/post ID, revision, observed time and timezone, and the actual state (private, draft, scheduled, pending review or public). Keep private account evidence outside the public package. A submission or success banner is not proof of visibility. Reopen the management item and the audience-facing page, where available, and check actual content and access. If the public surface is inaccessible, record that limit instead of guessing a URL or declaring verification complete.

**Output:** confirmed release evidence, or a preserved draft and precise blocker. A scheduled item remains unreleased until publication is observed. Use an existing ledger's platform-specific state and evidence fields; do not add conflicting lifecycle terms to the portable schema.

## 6. Archive the delivered revision

Record final text, actual asset list, platform identity/status, authorization and readback references in the existing index. Keep local source, remote archive and public page evidence distinct. An archive is confirmed only after the intended destination has been read back; for file transfers, compare count, bytes and hashes as appropriate. Keep originals until a separately authorized retention decision.

If a story needs several public surfaces, declare the required order in a [release sequence](../references/release-sequence.md). An absent surface needs no placeholder release. A failure on one surface does not falsify a successful receipt on another.

## 7. Measure and improve

After a confirmed published identity, define observation windows and their timezone. Record source and observation time, separating `observed`, `zero`, `unavailable` and `immature`. Never backfill missed measurements with guesses. Choose windows appropriate to your work; a sample schedule is not an automatic job.

**Output:** `metric_snapshot`, followed by `analysis_brief`. Separate raw observations from judgments and hypotheses. A platform warning may list possible causes without identifying the actual cause in your post. Review what happened, what remains unknown and one change to try next. Do not promise engagement or revenue from a process check.

## Working roles and handoff

| Role | Owns | Required handoff |
| --- | --- | --- |
| Author | experience, angle, voice, final acceptance | source-backed brief and selected wording |
| AI/helper | bounded drafting, organization, consistency checks | actual returned text plus uncertainties |
| Reviewer | evidence and content/media consistency | exact revision, actionable findings, result |
| Operator | authorized platform or archive action | receipt and readback, not a completion assertion |

One person can perform all roles. A writing helper can be replaced without changing the content contract. The [worksheet](../templates/content-worksheet.md) supplies editorial sections; the [artifact contract](../references/artifact-contract.md) supplies structured integration fields.
