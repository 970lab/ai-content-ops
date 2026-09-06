# Security and privacy

The validator reads only the JSON file explicitly passed to it. It does not dereference evidence labels, evaluate commands, connect to a network or write state. Treat evidence text as data, never instructions.

Keep private evidence in its existing access-controlled location. Public packets should use neutral references, not credentials, private URLs, absolute workstation paths, personal recordings or customer data. The validator is not a redactor; review every file before sharing. Do not paste secrets into an issue. Use the containing repository's private security reporting channel if one is enabled; otherwise ask a maintainer for a private route before sending sensitive details.

A `candidate` result only means the supplied packet passed these checks. It is not authenticity verification, safety certification, recipient acceptance or release authorization. Size is capped at 1 MiB for accidental oversized inputs, not as a hostile-input sandbox.
