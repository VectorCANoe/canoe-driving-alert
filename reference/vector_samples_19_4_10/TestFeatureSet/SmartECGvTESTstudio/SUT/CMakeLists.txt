cmake_minimum_required(VERSION 3.10)

project(Smart_ECG DESCRIPTION "C Application Smart ECG that uses SIL Adapter" LANGUAGES C CXX)

# Add SilAdapter Dependency
include(SilAdapter.cmake)
add_siladapter(
        INPUT_VCDLS "${CMAKE_CURRENT_SOURCE_DIR}/../CANoe/Datasources/SmartECG.vCDL"
        )
        
# Add Applications
add_subdirectory(Application_C)