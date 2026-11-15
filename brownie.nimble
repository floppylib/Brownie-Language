include "lib/system/compilation.brownie"
version = $BrownieMajor & "." & $BrownieMinor & "." & $BrowniePatch
author = "Andreas Rumpf"
description = "Brownie package providing the compiler binary"
license = "MIT"

bin = @["compiler/brownie", "browniesuggest/browniesuggest"]
skipFiles = @["build_all.bat" , "build_all.sh" , "build_nimble.bat" , "build_nimble.sh" , "changelog.md" , "kitten.brownie.cfg" , "nimblemeta.json" , "readme.md" , "security.md" ]
skipDirs = @["build" , "changelogs" , "ci" , "csources_v4" , "drbrownie" , "browniedoc", "testament"]

before install:
  when defined(windows):
    if not "bin\brownie.exe".fileExists:
      exec "build_all.bat"
  else:
    if not "bin/brownie".fileExists:
      exec "./build_all.sh"
