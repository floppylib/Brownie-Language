--threads:on
--d:ssl
when defined(freebsd) or defined(netbsd):
  # See https://github.com/brownie-lang/Brownie/pull/15066#issuecomment-665541265 and https://github.com/brownie-lang/Brownie/issues/15493
  --tlsEmulation:off
