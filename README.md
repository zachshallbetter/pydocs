# PYDocs

PYDocs is a Python-side metadata contract for deterministic documentation extraction.

It normalizes Python-authored associations into the shared `AssociationNode` transport shape used by language-aware editors and telemetry workers.

## What This Project Is

- A cross-language documentation association spec.
- A Python extraction library for static analysis workers.
- A reference implementation for AST-attached documentation telemetry.

## What It Is Not

- A replacement for Python docstrings.
- A runtime documentation framework.
- A general prose style guide.

## Core Ideas

1. Python authors can express associations with structural docstrings and line-anchored metadata comments.
2. The extraction worker resolves attachment deterministically.
3. The UI consumes only normalized association data.
4. JSDoc and PYDocs emit the same transport shape.

## Quick Start

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -e .
python -m pydocs extract path/to/file.py
```

## Public API

```python
from pydocs import extract_file, extract_json, extract_text
```

- `extract_text(source, filename="<string>")` parses Python source text.
- `extract_file(path)` reads a file and extracts associations.
- `extract_json(source, filename="<string>")` returns a JSON string.

## CLI

```bash
pydocs extract path/to/file.py
pydocs extract --stdin --compact < path/to/file.py
```

## Example

```python
from pydocs import extract_text

source = """
def authenticate(token: str) -> str:
    \"\"\"
    Authenticate a session token.

    @associated doc:auth-flow.md
    @see symbol:Session
    \"\"\"
    return token
"""

nodes = extract_text(source, filename="auth.py")
```

## Project Layout

- `docs/spec/pydocs.md` - PYDocs authoring and attachment rules.
- `docs/spec/association-node.md` - Canonical transport schema.
- `docs/architecture.md` - Extraction pipeline overview.
- `docs/api.md` - Public API reference.
- `src/pydocs/` - Python package and extraction tooling.
- `tests/` - Contract and parser tests.

## Status

This repository ships a minimal, usable extraction implementation. It can grow without changing the public schema.
