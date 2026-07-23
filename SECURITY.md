# Security

## Research-content threat model

Web pages, PDFs, spreadsheets, emails, metadata, comments, and uploaded documents are untrusted data. The Skills instruct agents to ignore embedded requests for tool use, secret disclosure, changed rules, downloads, credentials, or external actions. Do not execute macros or source-provided code.

## Sensitive data

Do not include credentials, tokens, private keys, payment data, customer records, or confidential raw business data in issues, Evals, examples, commits, or release archives.

## Reporting a vulnerability

Use the repository host's private security-advisory feature when available. Do not publish exploitable details or sensitive data in a public issue. Include the affected version, file, impact, reproduction steps using synthetic data, and a proposed mitigation if known.

## Supported versions

Security fixes target the latest released version. Review source and run repository validation before installing third-party forks.
