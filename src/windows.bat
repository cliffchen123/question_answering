echo The current directory is %CD%
del IR\config
mklink /d IR\config ..\config
del preprocess\config
mklink /d preprocess\config ..\config
set /p DUMMY=Hit ENTER to continue...