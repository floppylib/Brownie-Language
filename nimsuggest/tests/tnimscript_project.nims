# a .nims project is checked as browniescript: the browniescript API resolves, and importing a
# module doesn't crash browniesuggest
from std/strutils import strip

switch("hints", "off")
let home = get#[!]#Env("HOME", "/")
echo home.strip

discard """
$browniesuggest --tester $file
>def $1
def;;skProc;;system.getEnv;;proc (key: string, default: string): string{.noSideEffect, gcsafe, raises: <inferred> [].};;$lib/system/browniescript.nim;;114;;5;;"Retrieves the environment variable of name `key`.";;100
"""
