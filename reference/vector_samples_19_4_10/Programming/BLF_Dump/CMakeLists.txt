project(BlfDump)
cmake_minimum_required(VERSION 3.6 FATAL_ERROR)
#Specify the c++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

#Configure the build output directories and the install directory
set(CMAKE_INSTALL_PREFIX ${PROJECT_SOURCE_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/build)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Debug)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Release)

if(NOT CMAKE_BUILD_TYPE STREQUAL "Release")
  set(CMAKE_BUILD_TYPE "Debug")  
endif()

# Configure binlog Library according to chosen platform
if(UNIX)
  # Set RPath of executable to $ORIGIN if Linux, so that libbinlog.so can be found in same directory
  set(CMAKE_INSTALL_RPATH "$ORIGIN")
  set(LIB_DIRECTORY "Libs/Linux")
  set(INSTALL_PATH "Linux_${CMAKE_BUILD_TYPE}")
else()
  set(LIB_DIRECTORY "Libs/Win64")
  set(INSTALL_PATH "Win64_${CMAKE_BUILD_TYPE}")
endif()

find_library(BINLOG 
  NAMES binlog 
  HINTS ${LIB_DIRECTORY}
)
find_file(BINLOG_BINARY
  NAMES binlog.dll libbinlog.so
  HINTS ${LIB_DIRECTORY}
)

add_executable(BlfDump
  Source/BlfDump.cpp
  Source/CANDumpFunctions.cpp
  Source/SystemDumpFunctions.cpp
)

file(COPY ${BINLOG_BINARY} DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${CMAKE_BUILD_TYPE})

target_include_directories(BlfDump PRIVATE Include)  
target_link_libraries(BlfDump PUBLIC ${BINLOG})
# Set compiler flags -Wall and -Werror if the used compile is Clang or GNU
target_compile_options(BlfDump PRIVATE $<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:GNU>>:-Wall -Werror>)

install(TARGETS BlfDump DESTINATION bin/${INSTALL_PATH})
install(FILES ${BINLOG_BINARY} DESTINATION bin/${INSTALL_PATH})