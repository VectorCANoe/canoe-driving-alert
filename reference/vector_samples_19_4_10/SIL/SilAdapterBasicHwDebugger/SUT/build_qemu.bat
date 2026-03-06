@ECHO OFF

PUSHD %~dp0

cmake --preset Pico_QEMU
IF ERRORLEVEL 1 (
  GOTO :ERROR
)

cmake --build --preset Pico_QEMU

:ERROR
PAUSE
POPD