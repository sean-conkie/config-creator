@echo off
title Config Creator setup

@REM check for python install
python --version
if %ERRORLEVEL% neq 0 goto PythonCheckError

@REM create a virtual environment in this dir
python -m venv .\venv

@REM launch venv
.\venv\Scripts\activate
if %ERRORLEVEL% neq 0 goto VenvError

@REM install python requirements
python -m pip install -r .\requirements.txt
if %ERRORLEVEL% neq 0 goto LocalDbError

@REM create local db
python .\lib\local_db.py
if %ERRORLEVEL% neq 0 goto LocalDbError

@REM make migrations to db
python .\config_creator\manage.py migrate
if %ERRORLEVEL% neq 0 goto AppSetupError

exit /b 0

:PythonCheckError
echo You must install Python to continue.
pause
exit /b 1

:VenvError
echo Error setting up environment.
pause
exit /b 1

:PipInstallError
echo Error installing requirements.
pause
exit /b 1

:LocalDbError
echo Error creating local database.
pause
exit /b 1

:AppSetupError
echo Error in app setup.
pause
exit /b 1