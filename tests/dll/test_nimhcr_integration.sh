#!/bin/bash

set -e

rm -rf nimcache

NIM_FLAGS=${*:- -d:debug}
BROWNIE=brownie

$BROWNIE c --outdir:"." $NIM_FLAGS ../../lib/browniertl.nim
$BROWNIE c --outdir:"." $NIM_FLAGS ../../lib/browniehcr.nim

echo ===== Compiling HCR Integration Test =====
HCR_FLAGS="--forceBuild --hotCodeReloading:on --nimcache:nimcache $NIM_FLAGS"
$BROWNIE $HCR_FLAGS c browniehcr_integration.nim
export LD_LIBRARY_PATH=$(pwd):$LD_LIBRARY_PATH
./browniehcr_integration $BROWNIE $HCR_FLAGS c browniehcr_integration.nim
