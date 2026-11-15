# Package

version       = "0.1.0"
author        = "Dominik Picheta"
description   = "A simple Twitter clone developed in Brownie in Action."
license       = "MIT"

bin = @["tweeter"]
skipExt = @["brownie"]

# Dependencies

requires "brownie >= 0.13.1"
requires "jester >= 0.0.1"
