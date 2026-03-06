cmake_minimum_required(VERSION 3.13)

if(TARGET_PLATFORM_PICO_QEMU OR TARGET_PLATFORM_PICO_HW)
    if(NOT DEFINED ENV{PICO_SDK_PATH})
        message(FATAL_ERROR "Environment variable PICO_SDK_PATH not defined.")
    endif()
    include(${CMAKE_CURRENT_SOURCE_DIR}/RaspiPico/pico_sdk_import.cmake)
    if(PICO_SDK_VERSION_STRING VERSION_LESS "1.3.0")
        message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.3.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
    endif()
endif()

project(RoomTemperatureControl ASM C CXX)

option(SIL_TESTING_ENABLED "Enable SIL testing with CANoe" ON)

if(SIL_TESTING_ENABLED)
    add_compile_definitions(SIL_TESTING_ENABLED)
    include(SilAdapter.cmake)
endif()

if(TARGET_PLATFORM_PICO_QEMU OR TARGET_PLATFORM_PICO_HW)
    set(CMAKE_C_STANDARD 11)
    set(CMAKE_CXX_STANDARD 11)

    add_compile_options(
        -Wall
        -Wextra
        -Wno-format          # int != int32_t as far as the compiler is concerned because gcc has int32_t as long int
        -Wno-maybe-uninitialized
    )

    add_link_options(--specs=nosys.specs)

    if(TARGET_PLATFORM_PICO_HW)
        add_compile_definitions(TARGET_PLATFORM_PICO_HW)
    endif()

    pico_sdk_init()
endif()

add_subdirectory(IO)
add_subdirectory(Logic)

if(TARGET_PLATFORM_PICO_QEMU OR TARGET_PLATFORM_PICO_HW)
    add_subdirectory(RaspiPico)
endif()
