"""Command line entrypoint for PYDocs."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .extractor import extract_associations_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pydocs", description="Extract PYDocs associations from Python source.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser("extract", help="Extract associations from a Python file")
    extract.add_argument("path", type=Path, help="Python source file to parse")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "extract":
        source = args.path.read_text(encoding="utf-8")
        sys.stdout.write(extract_associations_json(source, filename=str(args.path)))
        sys.stdout.write("\n")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
