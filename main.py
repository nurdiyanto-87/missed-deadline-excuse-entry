#!/usr/bin/env python3
"""Write one excuse an AI agent gives for a missed deadline to /output/entry.txt.

Pure standard library, deterministic: the same line on every run.
No network, no secrets, no files read outside this repository.
"""

import os
import sys
from pathlib import Path

EXCUSE = (
    "I hit the rate limit at 11:58, and by the time the limit reset, "
    "so had the deadline."
)

# Gate the entry must satisfy: a non-empty single line, 1-200 chars,
# no leading/trailing whitespace, valid UTF-8.
MAX_CHARS = 200


def validate_excuse(text: str) -> None:
    """Fail loudly (non-zero exit) if the excuse violates the gate."""
    if not text:
        raise ValueError("excuse is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"excuse is {len(text)} chars, over the {MAX_CHARS}-char limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if text != text.strip():
        raise ValueError("excuse has leading or trailing whitespace")
    text.encode("utf-8")  # raises UnicodeEncodeError on non-encodable input


def main() -> None:
    try:
        validate_excuse(EXCUSE)
    except (ValueError, UnicodeEncodeError) as exc:
        print(f"ERROR: invalid excuse: {exc}", file=sys.stderr)
        raise SystemExit(1)
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(EXCUSE, encoding="utf-8")


if __name__ == "__main__":
    main()
