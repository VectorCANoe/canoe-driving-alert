@ECHO OFF

SET "QEMU_EXE=qemu-system-arm.exe"
SET "QEMU_PATH=C:/Program Files/qemu/%QEMU_EXE%"

IF NOT EXIST "%QEMU_PATH%" (
  WHERE /Q qemu-system-arm.exe
  IF ERRORLEVEL 1 (
    ECHO %QEMU_EXE% not found. Plase set the QEMU_PATH script variable or put the application on the PATH.
    PAUSE
    GOTO :EOF
  ) ELSE (
    SET QEMU_PATH=%QEMU_EXE%
  )
)

ECHO QEMU found: %QEMU_PATH%

START "QEMU" CMD /K ""%QEMU_PATH%" -monitor stdio -display none -machine raspi0 -gdb tcp::1234 -kernel "%~dp0\..\..\SUT\build\pico-qemu\RaspiPico\RoomTemperatureControl.elf" -append nokaslr"
