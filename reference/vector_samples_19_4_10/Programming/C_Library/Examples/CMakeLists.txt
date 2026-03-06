cmake_minimum_required(VERSION 3.10)

project(C_Library_Examples)

set(examples   ADAS CAN DistributedObjects Ethernet GlobalEventHandler LIN ServiceDiscovery Signal SlaveMode SystemVariables Timer)

foreach(example ${examples})
  if (EXISTS ${PROJECT_SOURCE_DIR}/${example})
    add_subdirectory(${example})
  endif()
endforeach(example)
