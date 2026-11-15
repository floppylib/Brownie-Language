#!/usr/bin/env python3
"""Replace standalone Nim product-name references in tracked text files.

Deliberately leaves .nim source files, legal notices, upstream provenance,
binary files, and this migration tooling untouched.
"""
from pathlib import Path
import re
import subprocess
import sys

BRANCH = "brownie/rebrand"
SKIP_EXACT = {
    "UPSTREAM.md",
    "copying.txt",
    "scripts/rebrand-to-brownie.py",
    ".github/workflows/brownie-rebrand.yml",
}
LICENSE_PREFIXES = ("LICENSE", "COPYING", "NOTICE", "PATENTS")
PATTERN = re.compile(r"\b(?:nim)\b", re.IGNORECASE)

def tracked_paths():
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    return [Path(p.decode("utf-8", "surrogateescape")) for p in raw.split(b"\0") if p]

def main():
    changed_files = 0
    replacements = 0
    skipped = []
    for path in tracked_paths():
        name = path.as_posix()
        if path.suffix.lower() == ".nim":
            skipped.append((name, "Nim source file"))
            continue
        if name in SKIP_EXACT or path.name.upper().startswith(LICENSE_PREFIXES):
            skipped.append((name, "legal/provenance/migration file"))
            continue
        try:
            original = path.read_bytes()
            text = original.decode("utf-8")
        except (UnicodeDecodeError, OSError):
            skipped.append((name, "binary or unreadable"))
            continue

        updated, count = PATTERN.subn("brownie", text)
        if count:
            path.write_text(updated, encoding="utf-8", newline="")
            changed_files += 1
            replacements += count

    print(f"Updated {changed_files} files; replaced {replacements} standalone occurrences.")
    print(f"Skipped {len(skipped)} files (source, legal/provenance, binary, or tooling).")
    for path, reason in skipped:
        if reason == "Nim source file":
            continue
        print(f"SKIP {path}: {reason}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
