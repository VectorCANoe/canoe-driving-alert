########################################################################################################################
#    Model Element   : CMake project file
#    Component       : CANoe FDX Example (easy client)
#    Copyright       : Copyright (c) 2024, Vector Informatik GmbH.
#    File Name       : CMakeLists.txt
########################################################################################################################

cmake_minimum_required(VERSION 3.14)

project(
  EasyClient
  LANGUAGES CXX
  VERSION "19.0.0"
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (WIN32)
  set (Boost_USE_STATIC_LIBS ON)
  find_package(Boost 1.67.0 REQUIRED COMPONENTS system)
elseif (UNIX)
  find_package(Boost 1.67.0 REQUIRED COMPONENTS system thread)
endif()

include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})


add_executable( EasyClient
  Main.cpp
  EasyLogic.cpp
  EasyLogic.h
  CANoeFDX.h
  FDXDatagram.cpp
  FDXDatagram.h
  FDXDispatcher.cpp
  FDXDispatcher.h
  FDXSocket.cpp
  FDXSocket.h
)

target_link_libraries(EasyClient ${Boost_LIBRARIES} )

if (WIN32)
  target_compile_definitions(EasyClient PUBLIC _WIN32_WINNT=0x0A00) # minimum system requirement: Windows 10 (0x0A00)
endif()
