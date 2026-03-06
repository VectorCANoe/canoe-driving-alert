add_library(IO STATIC IO.h)

target_include_directories(IO PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}")

if(SIL_TESTING_ENABLED)
    # Provided by SilAdapter.cmake script - Generates the SIL Adapter if it doesn't exist or the vCDL file were modified
    add_siladapter(
        INPUT_VCDLS "${CMAKE_CURRENT_SOURCE_DIR}/../../CANoe/DataSources/RoomTemperatureControl.vcdl"
        LANGUAGE "c"
        #SIL_ADAPTER_BUILDER_DIR <sil-adapter-builder.exe directory (e.g., the Exec64 directory of Test Unit Runner or CANoe installation)>
    )

    target_sources(IO PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/SIL/IO.c")
    target_link_libraries(IO PRIVATE SilAdapter)

    if(TARGET_PLATFORM_PICO_HW)
        # In case of SIL testing on a real Raspberry Pi Pico, we also use the IO pins to control
        # an LED for demonstration purposes. If you replace all your IO signals by calls to the
        # SIL Adapter, you only need to link against the SilAdapter target.
        target_link_libraries(IO PRIVATE pico_stdlib)
    endif()
else()
    target_sources(IO PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/HW/IO.c")
    target_link_libraries(IO PRIVATE pico_stdlib hardware_adc)
endif()
