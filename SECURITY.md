# Security Policy

## Supported Use

PYDocs is a static extraction library. It should not execute source code during parsing.

## Reporting Issues

Report security issues privately to the repository maintainers.

## Expectations

- Do not evaluate untrusted code.
- Do not shell out during extraction.
- Keep file parsing bounded and deterministic.
