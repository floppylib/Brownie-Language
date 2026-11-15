@echo off
REM COLOR 0A
chcp 65001
SET BROWNIEPATH=%~dp0\..
SET PATH=%BROWNIEPATH%\bin;%BROWNIEPATH%\dist\mingw\bin;%PATH%
cd %BROWNIEPATH%
cmd 


