from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


class CLITests(unittest.TestCase):
    def test_extract_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.py"
            path.write_text(
                """
# @associated doc:cli.md
VALUE = 1
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "-m", "pydocs", "extract", str(path)],
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload[0]["attachedToContext"]["qualifiedName"], "VALUE")


if __name__ == "__main__":
    unittest.main()
