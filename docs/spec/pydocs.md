# PYDocs Specification

PYDocs is the Python-side metadata contract for AST-driven documentation telemetry.

It is designed for deterministic extraction, not for general prose formatting.

## Purpose

PYDocs exists to let Python source emit stable documentation associations into the shared `AssociationNode` schema.

## Scope

PYDocs covers:

1. Structural docstrings on modules, classes, functions, async functions, methods, and properties.
2. Line-anchored metadata comments for nodes that do not naturally support docstrings.
3. Deterministic attachment resolution in a language worker.

PYDocs does not cover:

1. Runtime introspection.
2. Python typing.
3. General documentation generation.
4. Frontend rendering rules.

## Authoring Forms

### Structural Docstrings

Use docstrings for AST-native structures:

```python
def authenticate(token: str) -> Session:
    """
    Authenticate a session token.

    @associated doc:auth-flow.md
    @see symbol:Session
    """
```

### Metadata Comments

Use line-anchored metadata comments for constants, assignments, and other non-docstring targets:

```python
# @associated doc:auth-config.md
AUTH_TOKEN_TTL = 3600
```

## Canonical Tags

The first stable tag set is intentionally small:

1. `@associated` for primary routing.
2. `@see` for related references.
3. `@deprecated` for deprecation metadata.
4. `@owner` and `@status` for optional stewardship metadata.

## Attachment Semantics

Attachment rules must be explicit and deterministic.

1. A module docstring attaches to the module.
2. A class docstring attaches to the class.
3. A function or async function docstring attaches to that function.
4. A method docstring attaches to that method.
5. A line-anchored comment attaches to the next supported declaration or assignment.
6. Unknown targets are rejected during extraction.

## Extraction Contract

The worker should:

1. Parse Python source with a syntax-aware parser.
2. Preserve source positions.
3. Resolve node kind and qualified name.
4. Normalize tag names and values.
5. Emit `AssociationNode[]`.

## Non-Goals

PYDocs is not a replacement for:

1. Sphinx.
2. pydoc.
3. Docstring style guides.
4. Runtime documentation frameworks.
