# Define Executable
add_executable(Application_C
	src/Logic.h
	src/Logic.c
  src/IO.h
  src/IO.c
  src/main.c
  src/QRSDetection.h
  src/QRSDetection.c
)

add_compile_definitions(SIL_TESTING_CONTROLLED_BY_CANOE)

# Link SilAdapter with Executable
target_sources(Application_C
    PRIVATE
        TypeLibWrapper/TypeLibWrapper.h
        TypeLibWrapper/TypeLibWrapper.cpp
)
target_include_directories(Application_C
    PRIVATE
        TypeLibWrapper
)
                                
target_link_libraries(Application_C
    PRIVATE TypeLib
)
