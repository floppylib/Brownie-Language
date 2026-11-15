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
    "compiler/installer.ini",
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
    (re.compile(r"\bNIM_BIN\b"), "BROWNIE_BIN"),
    (re.compile(r"\bNIM_ROOT\b"), "BROWNIE_ROOT"),
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

    # Avoid rewriting file extensions (.nim) and technical config names.
    text = re.sub(r"(?<![A-Za-z0-9_.])Nim(?![A-Za-z0-9_.])", replace_nim, text, flags=re.IGNORECASE)

    # Koch is the old build-tool name; the public-facing name is now Kitten.
    def replace_koch(match):
        value = match.group(0)
        if value.isupper():
            return "KITTEN"
        if value[:1].isupper():
            return "Kitten"
        return "kitten"

    text = re.sub(r"(?<![A-Za-z0-9_.])koch(?!\.nim\b)(?![A-Za-z0-9_])", replace_koch, text, flags=re.IGNORECASE)
    text = re.sub(r"(?i)\bdrnim\b", lambda m: "DrBrownie" if m.group(0)[:1].isupper() else "drbrownie", text)
    # Public-facing helper names and generated documentation targets.
    path_terms = {
        "nimc.html": "brownie-compiler.html",
        "nimc.md": "brownie-compiler.md",
        "nimgrep.html": "brownie-grep.html",
        "nimgrep.md": "brownie-grep.md",
        "nimgrep_cmdline.txt": "brownie-grep_cmdline.txt",
        "niminst.html": "brownie-installer.html",
        "niminst.md": "brownie-installer.md",
        "nims.html": "brownie-script.html",
        "nims.md": "brownie-script.md",
        "nimsuggest.html": "brownie-suggest.html",
        "nimsuggest.md": "brownie-suggest.md",
        "koch.html": "kitten.html",
    }
    for old, new in path_terms.items():
        text = re.sub(re.escape(old), new, text, flags=re.IGNORECASE)

    # Undo source-path corruption produced by the first overly broad pass.
    text = re.sub(r"\.brownie\b", ".nim", text, flags=re.IGNORECASE)
    source_paths = {
        "tools/browniegrep.nim": "tools/nimgrep.nim",
        "tools/browniepretty.nim": "tools/nimpretty.nim",
        "drbrownie/drbrownie.nim": "drnim/drnim.nim",
        "compiler/brownie.nim": "compiler/nim.nim",
        "testament/tester.brownie": "testament/tester.nim",
    }
    for old, new in source_paths.items():
        text = text.replace(old, new)
    return text

def tracked_paths():
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    return [Path(p.decode("utf-8", "surrogateescape")) for p in raw.split(b"\0") if p]

def should_skip(path):
    name = path.as_posix()
    if path.suffix.lower() == ".nim":
        return "Nim source file"
    if path.suffix.lower() in {".nims", ".nimf", ".nimble"}:
        return "NimScript/template/package metadata (preserved for build compatibility)"
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

    # Rename documentation and command-completion assets, never .nim source files.
    path_renames = {
        "doc/nimc.md": "doc/brownie-compiler.md",
        "doc/nimgrep.md": "doc/brownie-grep.md",
        "doc/nimgrep_cmdline.txt": "doc/brownie-grep_cmdline.txt",
        "doc/niminst.md": "doc/brownie-installer.md",
        "doc/nims.md": "doc/brownie-script.md",
        "doc/nimsuggest.md": "doc/brownie-suggest.md",
        "doc/koch.md": "doc/kitten.md",
        "tools/nim.bash-completion": "tools/brownie.bash-completion",
        "tools/nim.zsh-completion": "tools/brownie.zsh-completion",
        "tools/nimgrep.bash-completion": "tools/browniegrep.bash-completion",
        "tools/nimpretty.bash-completion": "tools/browniepretty.bash-completion",
        "tools/nimsuggest.bash-completion": "tools/browniesuggest.bash-completion",
        "bin/nim-gdb": "bin/brownie-gdb",
        "bin/nim-gdb.bat": "bin/brownie-gdb.bat",
        "tools/debug/nim-gdb.py": "tools/debug/brownie-gdb.py",
        "doc/drnim.md": "doc/drbrownie.md",
    }
    for old, new in path_renames.items():
        old_path, new_path = Path(old), Path(new)
        if old_path.exists() and not new_path.exists():
            subprocess.check_call(["git", "mv", str(old_path), str(new_path)])

    # Validate the renamed shell helpers before allowing this sweep to commit.
    for shell_file in [
        "build_all.sh", "ci/funs.sh", "bin/brownie-gdb",
        "tools/brownie.bash-completion", "tools/browniegrep.bash-completion",
        "tools/browniepretty.bash-completion", "tools/browniesuggest.bash-completion",
    ]:
        if Path(shell_file).exists():
            subprocess.check_call(["bash", "-n", shell_file])

    # Parse the Python debugger helper without importing the GDB runtime.
    debug_helper = Path("tools/debug/brownie-gdb.py")
    if debug_helper.exists():
        import ast
        ast.parse(debug_helper.read_text(encoding="utf-8"), filename=str(debug_helper))

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
