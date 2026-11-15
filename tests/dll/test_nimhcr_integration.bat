set BROWNIE=brownie
set NIM_FLAGS=-d:debug

%BROWNIE% c --outdir:"." %NIM_FLAGS% ../../lib/browniertl.nim
%BROWNIE% c --outdir:"." %NIM_FLAGS% ../../lib/browniehcr.nim

set HCR_FLAGS=--forceBuild --hotCodeReloading:on --nimcache:nimcache %NIM_FLAGS%

%BROWNIE% %HCR_FLAGS% c browniehcr_integration.nim
browniehcr_integration %BROWNIE% %HCR_FLAGS% c browniehcr_integration.nim
