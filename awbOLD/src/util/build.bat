@ echo off

REM Automates the building of a CSMARTer distutils 
REM installer for Windows.
REM Results in a self-extracting zip file which, when
REM executed, unzips and installs itself in an existing
REM Python\Lib\site-packages directory.


REM First collect the files needed into the correct build directories:

cd \csmarter\CSMARTer
copy c:\csmarter\csmart\src\python\CSMARTer\CSMARTer.bat .

cd \csmarter
call copy-files.bat


REM Now build the installer:

python setup.py bdist_wininst


REM Sock away the installer just created

move/Y C:\csmarter\dist\csmarter*.exe .

REM Cleanup

call clean-dist.bat
