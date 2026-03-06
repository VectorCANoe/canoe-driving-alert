cmake_minimum_required(VERSION 3.10)

project(GlobalEventHandler)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

if ( (WIN32) AND (MINGW) AND (CMAKE_SIZEOF_VOID_P EQUAL 4) )
  set( defFile ../../CCL/CCL_Mingw_x86.def)
elseif ( (WIN32) AND (MSVC) AND (CMAKE_SIZEOF_VOID_P EQUAL 4) )
  set( defFile ../../CCL/CCL_VC_x86.def)
endif ()

add_library(GlobalEventHandler SHARED ${defFile}
            ./GlobalEventHandler.c
            ../../CCL/CCL.cpp)

target_include_directories(GlobalEventHandler PUBLIC ../..)

if (WIN32)
  # Do not use the library file name prefix 'lib' on windows platforms (x86 and x64).
  set_target_properties(GlobalEventHandler PROPERTIES PREFIX "")
elseif (UNIX)
  # Do not export all functions by default
  target_compile_options(GlobalEventHandler PUBLIC "-fvisibility=hidden")
endif()


# Install the Library to the Modules folder of the CANoe configuration.

if ( (WIN32) AND (CMAKE_SIZEOF_VOID_P EQUAL 8) )
  set( vModuleArchitecture "Windows-x64" )
elseif ( (WIN32) AND (CMAKE_SIZEOF_VOID_P EQUAL 4) )
  set( vModuleArchitecture "Windows-x86" )
elseif ( (UNIX) AND (CMAKE_SIZEOF_VOID_P EQUAL 8)) 
  set( vModuleArchitecture "Linux-x64" )
else ()
  set( vModuleArchitecture "Architecture-Unknown" )
endif ()

install ( TARGETS GlobalEventHandler
          RUNTIME DESTINATION ${PROJECT_SOURCE_DIR}/Configuration/Modules/${vModuleArchitecture}
          LIBRARY DESTINATION ${PROJECT_SOURCE_DIR}/Configuration/Modules/${vModuleArchitecture} )
