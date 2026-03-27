# AssociationNode Canonical Schema

`AssociationNode` is the shared transport shape emitted by language workers and consumed by the editor UI.

## Purpose

The schema is language-agnostic. Authoring dialects can vary, but the transport shape must remain stable.

## Schema

```ts
export interface AssociationContext {
  kind: string;
  name?: string;
  qualifiedName?: string;
}

export interface AssociationTag {
  tag: string;
  value: string;
  normalizedValue?: string;
}

export interface AssociationNode {
  line: number;
  endLine: number;
  kind: "jsdoc" | "pydoc";
  tags: AssociationTag[];
  attachedToContext: AssociationContext;
}
```

## Required Behavior

1. `line` and `endLine` are 1-indexed UI positions.
2. `kind` identifies the authoring dialect.
3. `tags` stores normalized tag data.
4. `attachedToContext` is structural metadata, not display text.

## Semantics

1. `@associated` is a primary routing tag.
2. `@see` is a secondary reference tag.
3. `normalizedValue` stores canonicalized tag payloads.
4. Unknown attachment targets must fail extraction instead of being guessed in the UI.
