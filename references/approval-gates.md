# Approval gates

Approval is a human decision tied to a precise action. A prior review approval does not authorize a later account action.

## Required gates

1. **Content review:** approve the exact candidate version, including claims, rights notes, and edits.
2. **Account action:** obtain human authorization immediately before login, upload, scheduling, publication, or other account interaction. State the intended destination, artifact version, and action scope.
3. **Release evidence:** after the human action, record the confirmed published identity separately from the authorization.
4. **Measurement:** collect metrics only when the published identity and observation window are confirmed. Record unavailable and immature data explicitly rather than guessing.

## Stop conditions

Stop and return `blocker` when scope, rights, identity, destination, window, or authorization is missing or ambiguous. Never work around a gate with stored credentials, browser state, automated uploads, or inferred permission.

## Minimum approval record

Record the approver role, candidate version, permitted action, destination description, decision time, and any limits. Exclude secrets and personal data. A release record must separately capture the observed identity and time after the action.
