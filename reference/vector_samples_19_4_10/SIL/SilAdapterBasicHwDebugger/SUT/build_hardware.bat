@ECHO OFF

PUSHD %~dp0

cmake --preset Pico_HW
IF ERRORLEVEL 1 (
  GOTO :ERROR
)

cmake --build --preset Pico_HW

:ERROR
PAUSE
POPD