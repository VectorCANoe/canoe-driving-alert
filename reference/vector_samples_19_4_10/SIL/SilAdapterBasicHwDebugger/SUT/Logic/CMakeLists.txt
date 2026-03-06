add_library(Logic STATIC Logic.c Logic.h)

target_link_libraries(Logic PUBLIC IO)

target_include_directories(Logic PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
