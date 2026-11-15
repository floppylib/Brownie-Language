@echo off
for %%i in (brownie.exe) do (set NIM_BIN=%%~dp$PATH:i)

for %%i in ("%NIM_BIN%\..\") do (set NIM_ROOT=%%~fi)

set @GDB_PYTHON_MODULE_PATH=%NIM_ROOT%\tools\debug\brownie-gdb.py
set @BROWNIE_GDB=gdb.exe

@echo source %@GDB_PYTHON_MODULE_PATH%> wingdbcommand.txt
%@BROWNIE_GDB% --command="wingdbcommand.txt" %*
del wingdbcommand.txt /f /q

EXIT /B %ERRORLEVEL%
@echo on
