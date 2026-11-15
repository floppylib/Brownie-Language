#!/bin/bash

set -e

rm -rf nimcache

NIM_FLAGS=${*:- -d:debug}
BROWNIE=brownie

$BROWNIE c --outdir:"." $NIM_FLAGS ../../lib/browniertl.brownie
$BROWNIE c --outdir:"." $NIM_FLAGS ../../lib/browniehcr.brownie

echo ===== Compiling HCR Integration Test =====
HCR_FLAGS="--forceBuild --hotCodeReloading:on --nimcache:nimcache $NIM_FLAGS"
$BROWNIE $HCR_FLAGS c nimhcr_integration.brownie
export LD_LIBRARY_PATH=$(pwd):$LD_LIBRARY_PATH
./nimhcr_integration $BROWNIE $HCR_FLAGS c nimhcr_integration.brownie
