# Architecture

PYDocs uses a contract-first layout:

1. `docs/spec/association-node.md` defines the transport schema.
2. `docs/spec/pydocs.md` defines the Python authoring contract.
3. `src/pydocs/extractor.py` turns source into `AssociationNode[]`.
4. `src/pydocs/api.py` exposes stable import paths for other tools.
5. `src/pydocs/cli.py` provides a human-facing command line interface.

## Design Goals

- Deterministic output.
- No runtime execution of user source.
- Stable cross-language transport.
- Small public API surface.

## Parsing Strategy

Python source is parsed with `ast`.
Comment metadata is recovered from source text.
Attachment resolution is based on source position, not heuristics in the UI.

## Output Contract

The extractor emits one normalized `AssociationNode` per attachment region. Each node carries every tag found in that region and can be serialized to JSON without further transformation.
