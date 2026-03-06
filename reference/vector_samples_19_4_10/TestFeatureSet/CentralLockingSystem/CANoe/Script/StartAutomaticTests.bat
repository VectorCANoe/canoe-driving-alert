@echo off
python "%~dp0AutomaticTest.py" "CentralLockingSystem.cfg" "AutomaticTests.log" 2> "error.log"

rem Output number of errors in tests, but do not signal to Jenkins
if errorlevel 1 (
 	echo %errorlevel% failed test configurations
) else (
	echo all test units successfully executed
)
exit /b 0

