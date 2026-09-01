# Security and privacy boundary

This package performs local validation only. It must not contain or request credentials, private URLs, customer or family data, internal network topology, local absolute paths, or organization-specific account configuration.

Do not use the validator to trigger deployment, DNS changes, access-policy changes, indexing submission, credential rotation, or account operations. Record authorization as evidence, but obtain and verify it through the team's existing control process immediately before any external action.

When reporting an issue, use a fictional or minimized record. Do not attach a production evidence file if it contains private infrastructure or personal data.

Before publishing a modified package, review both the current files and the repository history. Secret scanning of the current directory cannot prove that earlier commits are safe.

