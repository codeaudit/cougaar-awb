@echo off

REM Cleanup directories left over after building
REM our distribution installer or executable.

rmdir /S /Q C:\csmarter\dist
rmdir /S /Q C:\csmarter\build
rmdir /S /Q C:\csmarter\CSMARTer\dist
rmdir /S /Q C:\csmarter\CSMARTer\build
