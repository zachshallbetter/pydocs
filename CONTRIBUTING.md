# Contributing

## Development

```bash
python -m pip install -e .
python -m unittest discover
```

## Expectations

- Keep the `AssociationNode` schema stable.
- Preserve deterministic ordering.
- Update docs and tests together when the contract changes.

## Pull Requests

- Explain the contract change.
- Include test coverage for new attachment behavior.
- Avoid introducing runtime-only behavior into the extraction path.
