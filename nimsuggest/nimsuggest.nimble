include "../lib/system/compilation.brownie"
version = $BrownieMajor & "." & $BrownieMinor & "." & $BrowniePatch
author = "Andreas Rumpf"
description = "Tool for providing auto completion data for Brownie source code."
license = "MIT"
bin = @["browniesuggest"]

requires "compiler >= 1.9.0" , "checksums"
