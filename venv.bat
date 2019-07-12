@echo off

set venv=venv

if exist %venv% (
	echo Removing Existing Virtual Environment
	rmdir /s /q %venv%
	echo.
)
echo Creating the venv
python -m venv %venv%
echo.

echo Activating venv
call venv\Scripts\activate.bat
echo.

echo Upgrading pip
python -m pip install --upgrade pip
echo.

echo Installing Packages
pip install -r requirements.txt
echo.

pause