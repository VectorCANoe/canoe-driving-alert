********************************************************************
*                          BLF Dump                                *
********************************************************************

This is an example on how to use the binlog library on Windows or 
Linux to read a BLF log file and output its contents to the standard 
output. 

The provided example is written in C++11 and uses the build tool 
CMake. In order to build the example, the 64 bit system with the 
following tools installed is required:

	-CMake (version >= 3.6)
	-Visual Studio >=2013 (only on Windows Systems)
	-gcc or clang compiler (only on Linux Systems)

The example provides the necessary binlog header files in the 
folder Programming/BLF_Dump/Include, as well as the binlog 
library binaries (binlog.dll/binlog.lib for Windows and binlog.so 
for Linux) in the folder Programming/BLF_Dump/Libs.
The source code demonstrating the usage of the binlog library  
is located in the folder Programming/BLF_Dump/Source. 

Building the BlfDump executable on Windows and Linux requires the 
following steps to be executed:

1. Open a command line and navigate to the BLF_Dump folder containing 
this example, e.g using following command:

	cd C:/(...)/Programming/BLF_Dump 
	
2. Navigate to the "build" directory located inside the sample using:

	cd build
	
NOTE: Before executing the following build steps, please check that 
the "build" folder is empty and does not contain any leftover files 
from previous build executions. This step is recommended to prevent 
problems during the build process.
	  
3.	
a) How to build the "Debug" variant of BlfDump:
	Execute the following commands (according to the current
	platform):

	On Windows using Visual Studio >= 2013 as CMake Generator:
		cmake .. -A x64	
		cmake --build . --target install

	On Linux using Unix Makefiles as CMake Generator:
		cmake ..
		cmake --build . --target install

	The built executable for the "Debug" variant will either be 
	located in the folder Programming/BLF_Dump/bin/Win64_Debug on 
	Windows	or in Programming/BLF_Dump/bin/Linux_Debug on Linux 
	depending on the used platform.

b) How to build the "Release" variant of BlfDump:
	Execute following commands (according to the current
	platform):
	
	On Windows using Visual Studio >= 2013 as CMake Generator:
		cmake .. -A x64 -DCMAKE_BUILD_TYPE:STRING=Release	
		cmake --build . --config Release --target install
	
	On Linux using Unix Makefiles as CMake Generator:
		cmake .. -DCMAKE_BUILD_TYPE:STRING=Release
		cmake --build . --config Release --target install

	The built executable for the "Release" variant will either be
	located in the folder Programming/BLF_Dump/bin/Win64_Release on
	Windows	or Programming/BLF_Dump/bin/Linux_Release on Linux
	depending on the used platform.

********************************************************************
A detailed description and additional information can be found in 
the online help (see section "Sample configurations").
********************************************************************
--------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH
--------------------------------------------------------------------
