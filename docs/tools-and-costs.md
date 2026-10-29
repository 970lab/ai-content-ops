# Tools, costs and integration boundaries

## Minimal setup

- A local folder and text editor for sources, the worksheet and selected drafts.
- An AI writing tool you are already permitted to use, if desired. The manual workflow also works without one.
- A phone or screen recorder for real evidence when the story requires it.
- An editor appropriate to the chosen image, audio or video format.
- A platform account only when an authorized upload/publication is needed.

Python 3.10+ is needed only for the optional offline validators. No packages, model keys, paid APIs or platform accounts are required to run those checks.

## What is implemented here

The repository supplies instructions, artifact contracts, sample records and offline validation scripts. It does not supply live browser connectors, an editor, voice synthesis, a scheduler daemon, cloud storage synchronization or automatic metric scraping. Declaring an adapter does not install one. The [`adapter-contract`](../references/adapter-contract.md) defines the boundary for your own integration.

Use neutral roles so one assistant or several tools can implement the same process. Start with manual handoff of a bounded brief and an inspectable return. Add an integration only after you can verify which inputs it reads, which outputs it writes and what external actions it may perform. Preserve raw returns privately and record subsequent edits; never claim a tool returned text that was actually composed elsewhere.

## Costs to record

Free repository access does not make third-party services free. Before starting a new paid feature, identify who pays and the allowed spend. Do not assume a subscription includes API usage, voice cloning, exports or stock assets.

For a trial, record author/editor time, number of revision rounds, tool usage shown by the provider, whether usage is included or metered, and any actual billed amount/currency. Write `unknown` when unavailable. Do not convert credits to money without a verified applicable rate. Separate one-time setup from per-item costs and failed attempts from the successful attempt.

The project offers no paid plan in this candidate. Potential future setup, training or maintenance services would have a separately described scope; the core workflow should remain independently usable.

## Rights and private configuration

Keep accounts, credentials, customer/family information, voice profiles, private paths and unpublished original media outside public examples. Use safe aliases in portable artifacts and keep their private mapping separately. A source file's existence is not permission to publish it or send it to a cloud model.

The existing [MIT license](../LICENSE) covers included repository code and documentation. Third-party media, trademarks, likenesses and platform rules have their own requirements. Do not relicense someone else's assets by placing them in a template folder.
