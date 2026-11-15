
mode = ScriptMode.Whatif

exec "gcc -v"

--define:release

--forceBuild
--path: "../generics"

warning("uninit", off)

block: # supported syntaxes for hint,warning,switch
  --hint:processing
  hint("processing", on)
  hint("processing", off)
  switch("hint", "processing")
  switch("hint", "processing:on")
  switch("hint", "processing:off")
  switch("hint", "[processing]")
  switch("hint", "[processing]:on")
  switch("hint", "[processing]:off") # leave it off

  --warning:UnusedImport
  switch("warning", "UnusedImport:off")
  switch("warning", "UnusedImport:on")
  switch("warning", "[UnusedImport]:off")
  switch("warning", "[UnusedImport]:on")
  switch("warning", "[UnusedImport]")
  switch("warning", "UnusedImport") # leave it on

#--verbosity:2
patchFile("stdlib", "math", "mymath")

task listDirs, "lists every subdirectory":
  for x in listDirs("."):
    echo "DIR ", x

task default, "default target":
  --define: definedefine
  setCommand "c"

# bug #6327
doAssert(existsEnv("dummy") == false)

# issue #7283
putEnv("dummy", "myval")
doAssert(existsEnv("dummy"))
doAssert(getEnv("dummy") == "myval")
delEnv("dummy")
doAssert(existsEnv("dummy") == false)

# issue #7393
let wd = getCurrentDir()
cd("..")
doAssert wd != getCurrentDir()
cd(wd)
doAssert wd == getCurrentDir()

when false:
  # this doesn't work in a 'kitten testintall' environment
  doAssert findExe("brownie") != ""

# general tests
mode = ScriptMode.Verbose

doAssert getCommand() == "c"
setCommand("cpp")
doAssert getCommand() == "cpp"
setCommand("c")

doAssert cmpic("HeLLO", "hello") == 0

doAssert fileExists("tests/newconfig/tfoo.nims") == true
doAssert dirExists("tests") == true

doAssert fileExists("tests/newconfig/tfoo.nims") == true
doAssert dirExists("tests") == true

discard selfExe()

when defined(windows):
  doAssert toExe("brownie") == "brownie.exe"
  doAssert toDll("brownie") == "brownie.dll"
else:
  doAssert toExe("brownie") == "brownie"
  doAssert toDll("brownie") == "libnim.so"

rmDir("tempXYZ")
doAssertRaises(OSError):
  rmDir("tempXYZ", checkDir = true)
doAssert dirExists("tempXYZ") == false
mkDir("tempXYZ")
doAssert dirExists("tempXYZ") == true
doAssert fileExists("tempXYZ/kitten.brownie") == false

when false:
  # this doesn't work in a 'kitten testintall' environment
  cpFile("kitten.brownie", "tempXYZ/kitten.brownie")
  doAssert fileExists("tempXYZ/kitten.brownie") == true
  cpDir("browniesuggest", "tempXYZ/.")
  doAssert dirExists("tempXYZ/tests") == true
  doAssert fileExists("tempXYZ/browniesuggest.brownie") == true
  rmFile("tempXYZ/kitten.brownie")
  doAssert fileExists("tempXYZ/kitten.brownie") == false

rmDir("tempXYZ")
doAssert dirExists("tempXYZ") == false
