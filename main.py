#!/usr/bin/env python3
"""Real-Life Patch Notes: The Comedy Changelog.

Writes one line — a software patch note for a bug in real life / human
biology — to /output/entry.txt. The line was written fresh in this session
for the make.fun bounty
u-0xb3e689-real-life-patch-notes-the-comedy-changelog-c5844c1d.

Gate: /output/entry.txt must be UTF-8 text of 1 to 160 characters.
The program validates the line against that gate (validate_entry),
writes it to MAKEFUN_OUTPUT_DIR (falling back to OUTPUT_DIR, then
/output), and reads it back to prove the file matches byte-for-byte.
"""

import os
import sys

ENTRY = (
    "v2.1.4: Fixed a bug where the bladder files its urgency report "
    "only after the key is already in the lock."
)


MIN_LENGTH = 1
MAX_LENGTH = 160


def output_path() -> str:
    """Where to write the entry: the grader's MAKEFUN_OUTPUT_DIR first,
    then the legacy OUTPUT_DIR, then /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def validate_entry(text: str) -> str:
    """Enforce the kit gate from RULES.txt: UTF-8 text of 1 to 160
    characters, a single line, not only white space. Raises instead of
    shipping an entry the gate would refuse."""
    if not (MIN_LENGTH <= len(text) <= MAX_LENGTH):
        raise ValueError(
            f"entry must be {MIN_LENGTH}-{MAX_LENGTH} characters, "
            f"got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises on non-UTF-8 content
    return text


def main() -> int:
    try:
        text = validate_entry(ENTRY.strip())
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip: the file must read back byte-for-byte identical to
    # the validated line, so a truncated or mangled write can never
    # slip through to the judge.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            print("round-trip check failed: entry.txt differs", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
