"""Command line entrypoint for PYDocs."""

from __future__ import annotations

import argparse
import json
import sys

from .api import extract_file, extract_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pydocs", description="Extract PYDocs associations from Python source.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser("extract", help="Extract associations from a Python file")
    extract.add_argument("path", nargs="?", help="Python source file to parse")
    extract.add_argument("--stdin", action="store_true", help="Read source from stdin instead of a file path")
    extract.add_argument("--compact", action="store_true", help="Emit compact JSON")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "extract":
        if args.stdin:
            source = sys.stdin.read()
            payload = [node.to_dict() for node in extract_text(source, filename="<stdin>")]
        else:
            if args.path is None:
                parser.error("path is required unless --stdin is set")
            payload = [node.to_dict() for node in extract_file(args.path)]

        if args.compact:
            sys.stdout.write(json.dumps(payload, separators=(",", ":")))
        else:
            sys.stdout.write(json.dumps(payload, indent=2))
        sys.stdout.write("\n")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
