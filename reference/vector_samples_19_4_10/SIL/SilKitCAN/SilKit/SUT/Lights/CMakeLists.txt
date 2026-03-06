add_executable(SUT_Lights SUT_Lights.cpp)

target_include_directories(SUT_Lights PRIVATE ${CMAKE_SOURCE_DIR}/SUT/include)

target_link_libraries(SUT_Lights 
    PRIVATE SilKit::SilKit
    PRIVATE ftxui::screen
    PRIVATE ftxui::component
)


