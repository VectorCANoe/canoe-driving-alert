@ECHO OFF
SETLOCAL EnableDelayedExpansion

:: Call the Start.bat script based on the selected default debugger in the vhwdebugger-binding.yaml
FOR /f "tokens=2 delims=:" %%a IN ('FINDSTR /R "default-debugger: *([-_a-zA-Z])*" "%~dp0vhwdebugger-binding.yaml"') DO (
  SET "CONFIG=%%a"
  SET "CONFIG=!CONFIG: =!"
)

ECHO Selected test environment: %CONFIG%
SET SCRIPT="%~dp0%CONFIG%\Start.bat"

ECHO Calling %SCRIPT%
IF EXIST %SCRIPT% (
  CALL %SCRIPT%
) ELSE (
  ECHO %SCRIPT% not found!
)
