@ echo off

REM Automates the building of a CSMARTer executable and
REM an installer for Windows.
REM Results in a directory that contains an executable
REM file with supporting files; does not require user to
REM have Python, wxPython, or 4Suite installed.


REM First collect the files needed into the correct build 
REM directories:

call copy-files.bat


REM Now build the executable:

cd \csmarter\CSMARTer
python setup2.py py2exe --packages encodings --icon csmarter.ico


REM Sock away the executable directory just created

cd \csmarter
rd /S /Q CS03
move C:\csmarter\CSMARTer\dist\CS03 .


REM Cleanup

call clean-dist.bat
cd C:\csmarter\CS03
mkdir CSMARTer
cd CSMARTer


REM When this script is done, go to C:\csmarter\CS03 using
REM Windows Explorer, copy all files and dirs (except 
REM CSMARTer) into dir CSMARTer.  Then right-click
REM on the CSMARTer dir, and select "Add to CSMARTer.zip".  This
REM creates a zip file named CSMARTer.zip in the C:\csmarter\CS03
REM dir.  This is the file you will distribute.