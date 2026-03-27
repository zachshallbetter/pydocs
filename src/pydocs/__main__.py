"""Module entrypoint for `python -m pydocs`."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
