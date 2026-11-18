# Contributing

## Development

Python 3.11 or newer.

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest discover
```

CI runs the same install and `python -m unittest discover`.

## Expectations

- Keep the `AssociationNode` schema stable.
- Preserve deterministic ordering.
- Update docs and tests together when the contract changes.

## Conventions

- Commit subjects use conventional prefixes, for example `feat: ...`, `fix(scope): ...`, `ci: ...`, `docs: ...`.
- The repository has no `AGENTS.md`; the specification in `docs/spec/` is the contract the code follows.

## Pull Requests

- Explain the contract change.
- Include test coverage for new attachment behavior.
- Avoid introducing runtime-only behavior into the extraction path.
