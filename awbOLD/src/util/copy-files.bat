@ echo off

REM Assembles CSMARTer files into build directories in
REM preparation for building a distribution installer
REM or an executable.

cd \csmarter\CSMARTer
copy c:\csmarter\csmart\src\python\CSMARTer\_*.py .
copy c:\csmarter\csmart\src\python\CSMARTer\a*.py .
copy c:\csmarter\csmart\src\python\CSMARTer\c*.py .
copy c:\csmarter\csmart\src\python\CSMARTer\e*.py .
copy c:\csmarter\csmart\src\python\CSMARTer\g*.py .
copy c:\csmarter\csmart\src\python\CSMARTer\i*.py .
copy c:\csmarter\csmart\src\python\CSMARTer\s*.py .
copy c:\csmarter\csmart\src\python\CSMARTer\bitmaps\csmarter.ico .

cd ACMEPy
copy c:\csmarter\csmart\src\python\ACMEPy\_*.py .
copy c:\csmarter\csmart\src\python\ACMEPy\a*.py .
copy c:\csmarter\csmart\src\python\ACMEPy\c*.py .
copy c:\csmarter\csmart\src\python\ACMEPy\f*.py .
copy c:\csmarter\csmart\src\python\ACMEPy\h*.py .
copy c:\csmarter\csmart\src\python\ACMEPy\n*.py .
copy c:\csmarter\csmart\src\python\ACMEPy\p*.py .
copy c:\csmarter\csmart\src\python\ACMEPy\r*.py .
copy c:\csmarter\csmart\src\python\ACMEPy\society.py .
copy c:\csmarter\csmart\src\python\ACMEPy\society_factory2.py .

cd ..\bitmaps
copy c:\csmarter\csmart\src\python\CSMARTer\bitmaps\ACME2003.gif .

cd ..\data
copy C:\csmarter\csmart\src\python\CSMARTer\data\*tips* .
copy c:\csmarter\csmart\src\python\ACMEPy\tiny.xml .
copy c:\csmarter\csmart\src\python\ACMEPy\tiny_laydownTest.xml .

cd ..\docs
copy C:\csmarter\csmart\src\python\README.txt .
copy C:\csmarter\csmart\src\python\ReleaseNotes .

cd ..\Sample-Rules
copy C:\csmarter\csmart\src\python\CSMARTer\Sample-Rules\ruleblaah.rul .
copy C:\csmarter\csmart\src\python\CSMARTer\Sample-Rules\args.rul .
copy C:\csmarter\csmart\src\python\CSMARTer\Sample-Rules\Override.rul .
copy C:\csmarter\csmart\src\python\CSMARTer\Sample-Rules\rule1.rul .

cd \csmarter
