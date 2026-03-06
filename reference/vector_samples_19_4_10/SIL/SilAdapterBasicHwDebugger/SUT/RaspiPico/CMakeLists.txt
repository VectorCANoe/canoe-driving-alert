add_executable(RoomTemperatureControl main.c)

target_link_libraries(RoomTemperatureControl PRIVATE Logic)
if(TARGET_PLATFORM_PICO_HW)
  target_link_libraries(RoomTemperatureControl PRIVATE pico_stdlib)
  pico_add_extra_outputs(RoomTemperatureControl)
endif()
