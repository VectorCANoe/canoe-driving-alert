@ECHO OFF

IF NOT DEFINED PICO_SDK_PATH (
  ECHO Environment variable PICO_SDK_PATH not defined.
  PAUSE
  GOTO :EOF
)

ECHO Using Pico SDK at %PICO_SDK_PATH%

SET "OPENOCD_DIR=%PICO_SDK_PATH%\..\openocd"
SET "OPENOCD_PATH=%OPENOCD_DIR%\openocd.exe"
SET "SCRIPTS_DIR=%OPENOCD_DIR%\scripts"

IF NOT EXIST "%OPENOCD_PATH%" (
  ECHO %OPENOCD_PATH% not found!
  PAUSE
  GOTO :EOF
)

SET "BINARY_PATH=%~dp0\..\..\SUT\build\pico-hw\RaspiPico\RoomTemperatureControl.elf"
IF NOT EXIST "%BINARY_PATH%" (
  ECHO %BINARY_PATH% not found!
  PAUSE
  GOTO :EOF
)

REM Normalize paths
SET "SCRIPTS_DIR=%SCRIPTS_DIR:\=/%"
SET "BINARY_PATH=%BINARY_PATH:\=/%"

START "OpenOCD" CMD /K ""%OPENOCD_PATH%" -s "%SCRIPTS_DIR%" -f "interface/cmsis-dap.cfg" -f "target/rp2040.cfg" -c "adapter speed 5000" -c "gdb_port 1234" -c "program \"%BINARY_PATH%\" verify reset""
