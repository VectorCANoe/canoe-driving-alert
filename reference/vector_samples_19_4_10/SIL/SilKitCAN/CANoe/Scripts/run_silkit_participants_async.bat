@ECHO OFF

REM NB: 'ECHO(' produces a blank line

SET SILKIT_DIR=%SilKit_InstallDir%

SET SCRIPT_DPATH_WITH_BACKSLASH=%~dp0
SET SCRIPT_DPATH=%SCRIPT_DPATH_WITH_BACKSLASH:~0,-1%

SET STARTED_SIL_KIT_REGISTRY=0
tasklist /fi "ImageName eq sil-kit-registry.exe" /fo csv /nh 2>NUL | find "sil-kit-registry.exe" >NUL 2>NUL
IF NOT  "%ERRORLEVEL%"=="0" (
	ECHO Error: SIL Kit Registry is not running 
	PAUSE
	EXIT 1
)

ECHO(
ECHO Starting SUTs ...

START "sil-kit-participant-engine" "%SCRIPT_DPATH%\..\..\SilKit\bin\SUT_Engine.exe"
START "sil-kit-participant-lights" "%SCRIPT_DPATH%\..\..\SilKit\bin\SUT_Lights.exe"

ECHO(
ECHO ======================================================================
ECHO(
ECHO           Press ENTER to stop all processes
ECHO(
ECHO ======================================================================
ECHO(

PAUSE

ECHO(
ECHO Stopping SUTs ...
ECHO(

taskkill /F /IM SUT_Engine.exe
taskkill /F /IM SUT_Lights.exe
