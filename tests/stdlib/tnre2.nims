# std/nre2 requires brownie-regex and it requires brownie-unicodedb
exec("nimble --nimbleDir:build/deps install unicodedb@#head")
exec("nimble --nimbleDir:build/deps install regex@#head")
