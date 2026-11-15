@echo off
for %%i in (brownie.exe) do (set BROWNIE_BIN=%%~dp$PATH:i)

for %%i in ("%BROWNIE_BIN%\..\") do (set BROWNIE_ROOT=%%~fi)

set @GDB_PYTHON_MODULE_PATH=%BROWNIE_ROOT%\tools\debug\brownie-gdb.py
set @BROWNIE_GDB=gdb.exe

@echo source %@GDB_PYTHON_MODULE_PATH%> wingdbcommand.txt
%@BROWNIE_GDB% --command="wingdbcommand.txt" %*
del wingdbcommand.txt /f /q

EXIT /B %ERRORLEVEL%
@echo on
