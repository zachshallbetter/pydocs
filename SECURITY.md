# Security Policy

## Reporting a vulnerability

Please report security issues privately through GitHub private vulnerability reporting:
<https://github.com/zachshallbetter/pydocs/security/advisories/new>.
Do not open a public issue for a suspected vulnerability.

Include the PYDocs version, the input that triggers the problem and what an attacker could do.
This is a solo-maintained project: responses are best-effort with no SLA.

## Supported Use

PYDocs is a static extraction library. It should not execute source code during parsing.

## Expectations

- Do not evaluate untrusted code.
- Do not shell out during extraction.
- Keep file parsing bounded and deterministic.

## Supported versions

The project is pre-alpha (0.1.0); only the latest release receives fixes.
