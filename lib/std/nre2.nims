import std/os

if getCommand() == "doc":
  # std/nre2 requires brownie-regex and it requires brownie-unicodedb.
  # when build documentation on CI, git clone them as nimble is not available

  const PkgDir = "build/deps"
  const Pkgs = ["brownie-regex", "brownie-unicodedb"]

  for n in Pkgs:
    if not dirExists(PkgDir / n):
      exec("git clone -q https://github.com/nitely/" & n & " " & (PkgDir / n))

    switch("path", "$brownie" / PkgDir / n / "src")
