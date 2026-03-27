"""PYDocs extraction logic."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Iterable

from .models import AssociationContext, AssociationNode, AssociationTag

SUPPORTED_NODE_TYPES = (
    ast.ClassDef,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.Assign,
    ast.AnnAssign,
)


def normalize_tag_value(tag: str, raw_value: str) -> str:
    value = raw_value.strip()
    if tag in {"associated", "see"}:
        if value.startswith("{@link ") and value.endswith("}"):
            inner = value[len("{@link ") : -1].strip()
            if inner:
                return inner
        if value.startswith("doc:"):
            return value
    return value


def _docstring_node(node: ast.AST) -> ast.AST | None:
    body = getattr(node, "body", None)
    if not body:
        return None
    first = body[0]
    if (
        isinstance(first, ast.Expr)
        and isinstance(getattr(first, "value", None), ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return first
    return None


def _node_kind(node: ast.AST) -> str:
    if isinstance(node, ast.ClassDef):
        return "class"
    if isinstance(node, ast.AsyncFunctionDef):
        return "async_function"
    if isinstance(node, ast.FunctionDef):
        if any(_decorator_is_property(decorator) for decorator in node.decorator_list):
            return "property"
        return "function"
    if isinstance(node, ast.Assign):
        return "assignment"
    if isinstance(node, ast.AnnAssign):
        return "assignment"
    return "unknown"


def _decorator_is_property(node: ast.expr) -> bool:
    return isinstance(node, ast.Name) and node.id == "property"


def _node_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.ClassDef):
        return node.name
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return node.name
    if isinstance(node, ast.Assign):
        target = node.targets[0] if node.targets else None
        if isinstance(target, ast.Name):
            return target.id
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return node.target.id
    return None


def _anchor_line(node: ast.AST) -> int:
    decorators = getattr(node, "decorator_list", None) or []
    if decorators:
        decorator_lines = [getattr(decorator, "lineno", getattr(node, "lineno", 1)) for decorator in decorators]
        return min(decorator_lines)
    return getattr(node, "lineno", 1)


def _end_line(node: ast.AST) -> int:
    return getattr(node, "end_lineno", getattr(node, "lineno", 1))


def _qualified_name(parts: list[str], node_name: str | None) -> str | None:
    if node_name is None:
        return None
    if not parts:
        return node_name
    return ".".join([*parts, node_name])


def _parse_tag_lines(text: str) -> list[tuple[str, str]]:
    tags: list[tuple[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("@"):
            continue
        head, _, tail = stripped[1:].partition(" ")
        tags.append((head.strip(), tail.strip()))
    return tags


def _build_context(node: ast.AST, stack: list[str]) -> AssociationContext:
    kind = _node_kind(node)
    name = _node_name(node)
    qualified_name = _qualified_name(stack, name)
    return AssociationContext(kind=kind, name=name, qualifiedName=qualified_name)


def _comment_tags_for_node(source: str, node_start: int) -> list[tuple[int, str]]:
    lines = source.splitlines()
    idx = node_start - 2
    if idx < 0:
        return []

    block: list[tuple[int, str]] = []
    while idx >= 0:
        line = lines[idx].rstrip()
        if not line.strip():
            break
        if line.lstrip().startswith("#"):
            block.append((idx + 1, line.lstrip()[1:].strip()))
            idx -= 1
            continue
        break

    block.reverse()
    return block


def _emit_nodes(
    *,
    node_kind: str,
    start_line: int,
    end_line: int,
    context: AssociationContext,
    raw_tags: Iterable[tuple[int, str, str]],
) -> list[AssociationNode]:
    nodes: list[AssociationNode] = []
    for line_no, tag, value in raw_tags:
        nodes.append(
            AssociationNode(
                line=line_no,
                endLine=end_line if node_kind != "assignment" else line_no,
                kind="pydoc",
                tags=(
                    AssociationTag(
                        tag=tag,
                        value=value,
                        normalizedValue=normalize_tag_value(tag, value),
                    ),
                ),
                attachedToContext=context,
            )
        )
    return nodes


def extract_associations(source: str, *, filename: str = "<string>") -> list[AssociationNode]:
    """Extract PYDocs associations from Python source."""

    tree = ast.parse(source, filename=filename)
    nodes: list[AssociationNode] = []

    def visit(node: ast.AST, stack: list[str]) -> None:
        if isinstance(node, ast.Module):
            doc_node = _docstring_node(node)
            if doc_node is not None:
                context = AssociationContext(kind="module", qualifiedName=Path(filename).stem)
                start = getattr(doc_node, "lineno", 1)
                end = getattr(doc_node, "end_lineno", start)
                raw_doc = ast.get_docstring(node, clean=False) or ""
                nodes.extend(
                    _emit_nodes(
                        node_kind="module",
                        start_line=start,
                        end_line=end,
                        context=context,
                        raw_tags=((start, tag, value) for tag, value in _parse_tag_lines(raw_doc)),
                    )
                )

            for child in node.body:
                visit(child, stack)
            return

        if not isinstance(node, SUPPORTED_NODE_TYPES):
            for child in ast.iter_child_nodes(node):
                visit(child, stack)
            return

        node_name = _node_name(node)
        context = _build_context(node, stack)
        start = _anchor_line(node)
        end = _end_line(node)

        doc_node = _docstring_node(node)
        if doc_node is not None:
            raw_doc = ast.get_docstring(node, clean=False) or ""
            doc_start = getattr(doc_node, "lineno", start)
            doc_end = getattr(doc_node, "end_lineno", doc_start)
            nodes.extend(
                _emit_nodes(
                    node_kind=context.kind,
                    start_line=doc_start,
                    end_line=doc_end,
                    context=context,
                    raw_tags=((doc_start, tag, value) for tag, value in _parse_tag_lines(raw_doc)),
                )
            )

        comment_block = _comment_tags_for_node(source, start)
        if comment_block:
            raw_tags = []
            for line_no, text in comment_block:
                for tag, value in _parse_tag_lines(text):
                    raw_tags.append((line_no, tag, value))
            nodes.extend(
                _emit_nodes(
                    node_kind=context.kind,
                    start_line=start,
                    end_line=end,
                    context=context,
                    raw_tags=raw_tags,
                )
            )

        next_stack = stack + ([node_name] if node_name else [])
        for child in ast.iter_child_nodes(node):
            visit(child, next_stack)

    visit(tree, [])
    nodes.sort(key=lambda item: (item.line, item.endLine, item.kind, item.attachedToContext.qualifiedName or ""))
    return nodes


def extract_associations_json(source: str, *, filename: str = "<string>") -> str:
    """Extract PYDocs associations and serialize them as JSON."""

    return json.dumps([node.to_dict() for node in extract_associations(source, filename=filename)], indent=2)
