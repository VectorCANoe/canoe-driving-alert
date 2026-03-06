# Building the System under Test (SUT)

There is a pre-built SUT contained in this demo for testing:

  - Hardware: SUT/build/pico-hw/RaspiPico/RoomTemperatureControl.elf
  - QEMU: SUT/build/pico-qemu/RaspiPico/RoomTemperatureControl.elf

However if you want to build the SUT yourself you will need the following software:

  - CMake >= 3.21 (https://cmake.org/)
  - Ninja (https://ninja-build.org/)
    - Has to be included in your `PATH` environment variable
  - Raspberry Pi Pico SDK (https://www.raspberrypi.com/news/raspberry-pi-pico-windows-installer/)
    - You need to set the `PICO_SDK_PATH` environment variable according to your installation path, e.g. `PICO_SDK_PATH=C:\Program Files\Raspberry Pi\Pico SDK v1.5.1\pico-sdk`
    - You need to set the `PICO_TOOLCHAIN_PATH` environment variable according to your installation path, e.g. `PICO_TOOLCHAIN_PATH=C:\Program Files\Raspberry Pi\Pico SDK v1.5.1\gcc-arm-none-eabi\bin`

After installing the required software, you can build SUT via the `Pico_HW` or `Pico_QEMU` CMake preset.
For convienience there is a batch scripts included:
  - build_hardware.bat: Build for Raspberry Pi Pico 2040
  - build_qemu.bat: Build for QEMU setup

Note: The SIL Adapter is generated automatically via the helper script `SilAdapter.cmake` when running CMake.