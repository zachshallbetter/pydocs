"""Canonical data models for PYDocs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class AssociationContext:
    kind: str
    name: str | None = None
    qualifiedName: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AssociationTag:
    tag: str
    value: str
    normalizedValue: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AssociationNode:
    line: int
    endLine: int
    kind: str
    tags: tuple[AssociationTag, ...] = field(default_factory=tuple)
    attachedToContext: AssociationContext = field(default_factory=lambda: AssociationContext(kind="unknown"))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tags"] = [tag.to_dict() for tag in self.tags]
        payload["attachedToContext"] = self.attachedToContext.to_dict()
        return payload
