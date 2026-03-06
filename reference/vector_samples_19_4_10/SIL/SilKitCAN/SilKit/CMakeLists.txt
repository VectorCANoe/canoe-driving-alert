# Copyright (c) Vector Informatik GmbH. All rights reserved.
cmake_minimum_required(VERSION 3.5)

#######################################################################################################################
# Project definition
#######################################################################################################################
project("SilKit-CANoe-Demo-CAN_easy" LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 14)

#######################################################################################################################
# Dependencies
#######################################################################################################################

# SIL Kit is part of the CANoe installation. find_package will detect it.
find_package(SilKit REQUIRED)
message(STATUS "${PROJECT_NAME}: Searching SilKit package in ${SilKit_DIR}")

if(NOT TARGET SilKit::SilKit)
    message(FATAL_ERROR "Could not find SilKit package in ${SILKIT_DIRECTORY}")
endif()

# Install ftxui
include(FetchContent)
FetchContent_Declare(ftxui
  GIT_REPOSITORY https://github.com/ArthurSonzogni/ftxui
  GIT_TAG v5.0.0
)
FetchContent_GetProperties(ftxui)
if(NOT ftxui_POPULATED)
  FetchContent_Populate(ftxui)
  set(FTXUI_BUILD_EXAMPLES OFF)
  set(FTXUI_BUILD_DOCS OFF)
  set(FTXUI_BUILD_DOCS OFF)
  set(FTXUI_QUIET ON)
  add_subdirectory(${ftxui_SOURCE_DIR} ${ftxui_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

#######################################################################################################################
# Set directories
#######################################################################################################################

set(_DEMO_OUTPUT_DIR "${CMAKE_CURRENT_LIST_DIR}/bin")

get_target_property(impLocRelease SilKit::SilKit IMPORTED_LOCATION_RELEASE)
get_target_property(impLocDebug SilKit::SilKit IMPORTED_LOCATION_DEBUG)
file(COPY ${impLocRelease} ${impLocDebug} DESTINATION ${_DEMO_OUTPUT_DIR})

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${_DEMO_OUTPUT_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${_DEMO_OUTPUT_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${_DEMO_OUTPUT_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${_DEMO_OUTPUT_DIR})

#######################################################################################################################
# Add the actual demo projects
#######################################################################################################################
add_subdirectory(SUT/Engine)
add_subdirectory(SUT/Lights)

file(COPY ${impLocRelease} ${impLocDebug} DESTINATION ${CMAKE_BINARY_DIR})
