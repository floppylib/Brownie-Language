#!/usr/bin/env python3
"""Rebrand user-facing Nim/Koch labels in non-.nim files.

This intentionally does not rewrite .nim source files, legal notices,
upstream-provenance records, or GitHub workflow definitions.
"""
from pathlib import Path
import re
import subprocess
import sys

SKIP_EXACT = {
    "UPSTREAM.md",
    "copying.txt",
    "scripts/rebrand-to-brownie.py",
}
SKIP_PREFIXES = (
    ".github/workflows/",
)
LICENSE_PREFIXES = ("LICENSE", "COPYING", "NOTICE", "PATENTS")

# Specific inherited tool names. Match whole identifiers so ordinary English
# words such as "minimum" are never changed.
COMPOUNDS = [
    (re.compile(r"\bdrnim\b", re.IGNORECASE), "drbrownie"),
    (re.compile(r"\bnimdoc\b", re.IGNORECASE), "browniedoc"),
    (re.compile(r"\bnimscript\b", re.IGNORECASE), "browniescript"),
    (re.compile(r"\bnimgrep\b", re.IGNORECASE), "browniegrep"),
    (re.compile(r"\bniminst\b", re.IGNORECASE), "brownieinst"),
    (re.compile(r"\bnimsuggest\b", re.IGNORECASE), "browniesuggest"),
    (re.compile(r"\bnimpretty\b", re.IGNORECASE), "browniepretty"),
    (re.compile(r"\bnimprof\b", re.IGNORECASE), "brownieprof"),
    (re.compile(r"\bnimhcr\b", re.IGNORECASE), "browniehcr"),
    (re.compile(r"\bnimrtl\b", re.IGNORECASE), "browniertl"),
    (re.compile(r"\bnim-gdb\b", re.IGNORECASE), "brownie-gdb"),
    (re.compile(r"\bnim-lldb\b", re.IGNORECASE), "brownie-lldb"),
    (re.compile(r"\bnim_bool_expression\b", re.IGNORECASE), "brownie_bool_expression"),
    (re.compile(r"\bnim_iteration_expression\b", re.IGNORECASE), "brownie_iteration_expression"),
    (re.compile(r"\bNIM_SYSROOT\b"), "BROWNIE_SYSROOT"),
    (re.compile(r"\bNIM_GDB\b"), "BROWNIE_GDB"),
]

def replace_branding(text):
    for pattern, replacement in COMPOUNDS:
        text = pattern.sub(replacement, text)

    # Standalone language/compiler name. Preserve title/upper case styling.
    def replace_nim(match):
        value = match.group(0)
        if value.isupper():
            return "BROWNIE"
        if value[:1].isupper():
            return "Brownie"
        return "brownie"

    text = re.sub(r"\bNim\b", replace_nim, text, flags=re.IGNORECASE)

    # Koch is the old build-tool name; the public-facing name is now Kitten.
    def replace_koch(match):
        value = match.group(0)
        if value.isupper():
            return "KITTEN"
        if value[:1].isupper():
            return "Kitten"
        return "kitten"

    return re.sub(r"\bkoch\b", replace_koch, text, flags=re.IGNORECASE)

def tracked_paths():
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    return [Path(p.decode("utf-8", "surrogateescape")) for p in raw.split(b"\0") if p]

def should_skip(path):
    name = path.as_posix()
    if path.suffix.lower() == ".nim":
        return "Nim source file"
    if name in SKIP_EXACT:
        return "migration/provenance file"
    if any(name.startswith(prefix) for prefix in SKIP_PREFIXES):
        return "workflow file (GitHub App lacks workflow-write permission)"
    if path.name.upper().startswith(LICENSE_PREFIXES):
        return "license/copyright notice"
    return None

def main():
    changed_files = 0
    replacements = 0
    residuals = []

    for path in tracked_paths():
        reason = should_skip(path)
        if reason:
            continue
        try:
            original = path.read_bytes()
            text = original.decode("utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        updated = replace_branding(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="")
            changed_files += 1
            replacements += 1

    # Rename the documentation file too; its .md extension is not source code.
    old_doc = Path("doc/drnim.md")
    new_doc = Path("doc/drbrownie.md")
    if old_doc.exists() and not new_doc.exists():
        subprocess.check_call(["git", "mv", str(old_doc), str(new_doc)])

    # Report remaining Nim-like references for a follow-up, carefully reviewed
    # pass. This is an audit list, not an instruction to rewrite compiler ABI.
    token = re.compile(r"\b[A-Za-z0-9_.-]*nim[A-Za-z0-9_.-]*\b", re.IGNORECASE)
    for path in tracked_paths():
        reason = should_skip(path)
        if reason:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        found = sorted(set(token.findall(text)))
        if found:
            residuals.append((path.as_posix(), found[:12]))

    print(f"Updated {changed_files} text files ({replacements} files contained branding changes).")
    print(f"Remaining non-.nim references in {len(residuals)} files need technical review:")
    for name, words in residuals[:100]:
        print(f"REVIEW {name}: {', '.join(words)}")
    if len(residuals) > 100:
        print(f"... and {len(residuals) - 100} more files.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
