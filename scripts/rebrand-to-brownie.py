#!/usr/bin/env python3
"""Rebrand Nim product references in all non-.nim tracked files.

The compiler's .nim implementation sources and legal/upstream provenance are
intentionally preserved. Compatibility-critical ABI/config identifiers and
the external Nimble package manager are not product labels and remain intact.
"""
from pathlib import Path
import ast
import re
import subprocess
import sys

SKIP_EXACT = {
    "UPSTREAM.md",
    "copying.txt",
    "scripts/rebrand-to-brownie.py",
    "compiler/installer.ini",
    "build_all.sh",
    "build_all.bat",
    "ci/funs.sh",
    "compiler/nim.cfg",
    "config/nim.cfg",
    "drnim/nim.cfg",
    "lib/nimbase.h",
    "lib/nimhcr.nim.cfg",
    "lib/nimrtl.nim.cfg",
    "lib/pure/coro.nimcfg",
    "lib/std/nre2.nims",
    "nimsuggest/nimsuggest.nim.cfg",
    "tests/config.nims",
    "tools/debug/brownie-gdb.py",
    "tools/debug/nimlldb.py",
    "tools/debug/brownie-lldb.py",
    "lib/genode_cpp/signals.h",
    "lib/deps.txt",
    "tests/dll/nimhcr_compile.c",
    "tests/dll/nimhcr_compile.h",
    "tests/dll/nimhcr_unit.nim.cfg",
    "tests/dll/test_nimhcr_integration.bat",
    "tests/dll/test_nimhcr_integration.sh",
    "lib/system/yrc_opt_proof.lean",
    "lib/system/yrc_proof.lean",
    "lib/system/yrc_proof.tla",
    "lib/system/yrc_tarjan_proof.lean",
    "tests/template/sunset.nimf",
}
SKIP_PREFIXES = (".github/workflows/",)
LICENSE_PREFIXES = ("LICENSE", "COPYING", "NOTICE", "PATENTS")

# These names are real compiler interfaces / runtime ABI, not user-facing
# branding. Changing them without changing the .nim implementation would break
# bootstrapping or generated-code compatibility.
TECHNICAL = (
    "nimble", "nimcache", "nimversion", "nimcall", "nimPreview",
    "nimHas", "nimUse", "nimStrict", "nimCompiler", "nimMain",
    "nimNode", "nimVM", "nimType", "nimBool", "nimIteration",
    "nimTitle", "nimgrp", "nimout", "NIM_", "NimMain",
    "NimNode", "NimVM", "NimType", "NIM_BOOL", "Nimony",
    "NimMajor", "NimMinor", "NimPatch",
)

COMPOUNDS = [
    (re.compile(r"\bNimrod\b", re.IGNORECASE), "Brownie"),
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
    (re.compile(r"\bnimgrab\b", re.IGNORECASE), "browniegrab"),
    (re.compile(r"\bnimgrind\b", re.IGNORECASE), "browniegrind"),
    (re.compile(r"\bnim-gdb\b", re.IGNORECASE), "brownie-gdb"),
    (re.compile(r"\bnim-lldb\b", re.IGNORECASE), "brownie-lldb"),
    (re.compile(r"\bc2nim\b", re.IGNORECASE), "c2brownie"),
    (re.compile(r"\bNIM_SYSROOT\b"), "BROWNIE_SYSROOT"),
    (re.compile(r"\bNIM_GDB\b"), "BROWNIE_GDB"),
    (re.compile(r"\bNIM_BIN\b"), "BROWNIE_BIN"),
    (re.compile(r"\bNIM_ROOT\b"), "BROWNIE_ROOT"),
]

def replace_branding(text):
    for pattern, replacement in COMPOUNDS:
        text = pattern.sub(replacement, text)

    # Replace the standalone language name, not the .nim source extension.
    text = re.sub(
        r"(?<![A-Za-z0-9_.])Nim(?![A-Za-z0-9_.])",
        lambda m: "BROWNIE" if m.group(0).isupper()
        else ("Brownie" if m.group(0)[:1].isupper() else "brownie"),
        text, flags=re.IGNORECASE
    )

    # Replace the remaining Nim-prefix identifiers used as product/tool names.
    # Keep compiler ABI/feature names and the external Nimble package manager.
    def prefix_repl(match):
        token = match.group(0)
        suffix = token[3:]
        if any(token.lower().startswith(x.lower()) for x in TECHNICAL):
            return token
        if suffix.lower().startswith("ble"):
            return token
        if token.isupper():
            return "BROWNIE" + token[3:]
        if token[:1].isupper():
            return "Brownie" + token[3:]
        return "brownie" + token[3:]

    text = re.sub(
        r"(?<![A-Za-z0-9_.])nim(?=[A-Za-z0-9_-])[A-Za-z0-9_-]*",
        prefix_repl, text, flags=re.IGNORECASE
    )

    # Camel-case product fragments such as MyLibNimTools or TNimDoc.
    def camel_repl(match):
        token = match.group(0)
        if any(token.lower().endswith(x.lower()) for x in ("nimble",)):
            return token
        if token.isupper():
            return token[:-3] + "BROWNIE"
        return token[:-3] + ("Brownie" if token[-3:-2].isupper() else "brownie")

    text = re.sub(r"(?<=[A-Za-z0-9])Nim(?=[A-Z])", "Brownie", text)
    text = re.sub(r"(?i)(?<=c2)nim\b", "brownie", text)
    return text

def tracked_paths():
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    return [Path(p.decode("utf-8", "surrogateescape")) for p in raw.split(b"\0") if p]

def should_skip(path):
    name = path.as_posix()
    if path.suffix.lower() == ".nim":
        return "Nim source file"
    if name in SKIP_EXACT:
        return "migration/provenance/bootstrap contract"
    if any(name.startswith(prefix) for prefix in SKIP_PREFIXES):
        return "workflow file"
    if path.name.upper().startswith(LICENSE_PREFIXES):
        return "license/copyright notice"
    return None

def main():
    changed_files = 0
    changed_occurrences = 0
    for path in tracked_paths():
        if should_skip(path):
            continue
        try:
            original = path.read_bytes()
            text = original.decode("utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = replace_branding(text)
        if updated != text:
            changed_files += 1
            changed_occurrences += sum(
                text.lower().count(term) - updated.lower().count(term)
                for term in ("nimdoc", "drnim", "nimgrep", "nimsuggest", "nimpretty", "c2nim")
            )
            path.write_text(updated, encoding="utf-8", newline="")

    # User-facing filenames and assets. Do not rename paths used as required
    # compiler config/header names or directories referenced by .nim sources.
    path_renames = {
        "doc/nimdoc.css": "doc/browniedoc.css",
        "doc/nimdoc.cls": "doc/browniedoc.cls",
        "tools/debug/nimlldb.py": "tools/debug/brownie-lldb.py",
        "icons/nim.ico": "icons/brownie.ico",
        "icons/nim.rc": "icons/brownie.rc",
        "icons/nim.res": "icons/brownie.res",
        "icons/nim-amd64-windows-vcc.res": "icons/brownie-amd64-windows-vcc.res",
        "icons/nim-i386-windows-vcc.res": "icons/brownie-i386-windows-vcc.res",
        "icons/nim_icon.o": "icons/brownie_icon.o",
        "nim.nimble": "brownie.nimble",
    }
    for old, new in path_renames.items():
        old_path, new_path = Path(old), Path(new)
        if old_path.exists() and not new_path.exists():
            subprocess.check_call(["git", "mv", str(old_path), str(new_path)])

    # References to renamed documentation stylesheets/classes.
    for path in tracked_paths():
        if should_skip(path):
            continue
        try:
            original = path.read_bytes()
            text = original.decode("utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = text.replace("nimdoc.css", "browniedoc.css").replace(
            "nimdoc.cls", "browniedoc.cls"
        )
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="")

    # Sanity checks for shell/Python tooling and installer assets.
    for shell_file in (
        "build_all.sh", "ci/funs.sh", "bin/brownie-gdb",
        "tools/brownie.bash-completion", "tools/browniegrep.bash-completion",
        "tools/browniepretty.bash-completion", "tools/browniesuggest.bash-completion",
    ):
        if Path(shell_file).exists():
            subprocess.check_call(["bash", "-n", shell_file])
    for debug_helper in (
        Path("tools/debug/brownie-gdb.py"),
        Path("tools/debug/brownie-lldb.py"),
    ):
        if debug_helper.exists():
            ast.parse(debug_helper.read_text(encoding="utf-8"), filename=str(debug_helper))

    print(f"Updated {changed_files} non-.nim text files.")
    print(f"Rebrand pass completed; {changed_occurrences} legacy tool-name occurrences replaced.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
