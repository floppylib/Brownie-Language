include "../lib/system/compilation.nim"
version = $NimMajor & "." & $NimMinor & "." & $NimPatch
author = "Andreas Rumpf"
description = "Tool for providing auto completion data for Brownie source code."
license = "MIT"
bin = @["browniesuggest"]

requires "compiler >= 1.9.0" , "checksums"
