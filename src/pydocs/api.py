"""Public API for PYDocs extraction."""

from __future__ import annotations

from pathlib import Path

from .extractor import extract_associations, extract_associations_json


def extract_text(source: str, *, filename: str = "<string>"):
    """Extract associations from Python source text."""

    return extract_associations(source, filename=filename)


def extract_file(path: str | Path):
    """Extract associations from a Python file."""

    file_path = Path(path)
    return extract_associations(file_path.read_text(encoding="utf-8"), filename=str(file_path))


def extract_json(source: str, *, filename: str = "<string>") -> str:
    """Extract associations and serialize them as JSON."""

    return extract_associations_json(source, filename=filename)
