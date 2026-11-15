discard """
  cmd: "brownie e $file"
"""

import mscriptcompiletime

macro foo =
  doAssert bar == 2
foo()
