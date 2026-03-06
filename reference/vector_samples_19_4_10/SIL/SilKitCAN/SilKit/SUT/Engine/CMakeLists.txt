add_executable(SUT_Engine SUT_Engine.cpp)

target_include_directories(SUT_Engine PRIVATE ${CMAKE_SOURCE_DIR}/SUT/include)

target_link_libraries(SUT_Engine 
    PRIVATE SilKit::SilKit
    PRIVATE ftxui::screen
    PRIVATE ftxui::component
)

