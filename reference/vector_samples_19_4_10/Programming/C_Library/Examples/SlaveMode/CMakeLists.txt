cmake_minimum_required(VERSION 3.10)

project(SlaveMode)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

if ( (WIN32) AND (MINGW) AND (CMAKE_SIZEOF_VOID_P EQUAL 4) )
  set( defFile ../../CCL/CCL_Mingw_x86.def)
elseif ( (WIN32) AND (MSVC) AND (CMAKE_SIZEOF_VOID_P EQUAL 4) )
  set( defFile ../../CCL/CCL_VC_x86.def)
endif ()

set(COMP_NAME SlaveMode)
add_library(${COMP_NAME} SHARED ${defFile}
            ./SlaveMode.cpp
            ../../CCL/CCL.cpp)

        target_include_directories(${COMP_NAME} PUBLIC ../..)

if (WIN32)
  # Do not use the library file name prefix 'lib' on windows platforms (x86 and x64).
  set_target_properties(${COMP_NAME} PROPERTIES PREFIX "")
elseif (UNIX)
  # Do not export all functions by default
  target_compile_options(${COMP_NAME} PUBLIC "-fvisibility=hidden")
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

install ( TARGETS ${COMP_NAME}
          RUNTIME DESTINATION ${PROJECT_SOURCE_DIR}/Configuration/Modules/${vModuleArchitecture}
          LIBRARY DESTINATION ${PROJECT_SOURCE_DIR}/Configuration/Modules/${vModuleArchitecture} )

# Additional executable only for Windows (to trigger the two events)
if (WIN32)
  # Build sample executable to trigger an event
  add_executable(TriggerCANoe ./TriggerCANoe/TriggerCANoe.cpp)
  if (CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(TARGET_INSTALL_DIR "Exec64")
  else ()
    set(TARGET_INSTALL_DIR "Exec32")
  endif ()
  install ( TARGETS TriggerCANoe
            RUNTIME DESTINATION ${PROJECT_SOURCE_DIR}/Configuration/${TARGET_INSTALL_DIR}$<$<CONFIG:Debug>:_Debug> )

endif(WIN32)
