@echo off
python "%~dp0AutomaticTest.py" "CentralLockingSystem.cfg" "AutomaticTests.log" 2> "error.log"

rem Output number of errors, and signal success/failure to Jenkins
if errorlevel 1 (
	echo %errorlevel% failed test configurations
	exit /b %errorlevel%
) else (
	echo all test units successfully executed
)
