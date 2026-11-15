set BROWNIE=brownie
set NIM_FLAGS=-d:debug

%BROWNIE% c --outdir:"." %NIM_FLAGS% ../../lib/browniertl.brownie
%BROWNIE% c --outdir:"." %NIM_FLAGS% ../../lib/browniehcr.brownie

set HCR_FLAGS=--forceBuild --hotCodeReloading:on --nimcache:nimcache %NIM_FLAGS%

%BROWNIE% %HCR_FLAGS% c nimhcr_integration.brownie
nimhcr_integration %BROWNIE% %HCR_FLAGS% c nimhcr_integration.brownie
