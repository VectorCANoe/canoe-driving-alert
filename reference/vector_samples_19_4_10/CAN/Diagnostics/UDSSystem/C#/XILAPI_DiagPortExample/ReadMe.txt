XIL API Diag Port Example
=========================

This example is based both on XIL API V2.1.0 and V2.2.0. The Visual Studio solution allows to build for the appropriate XIL API version by selecting the corresponding configuration (Debug_XIL_API_2_1_0, Debug_XIL_API_2_2_0, Release_XIL_API_2_1_0 and Release_XIL_API_2_2_0) with the desired bitness (x86 = 32bit, x64 = 64bit).

In order to run this example with CANoe, you need to enable the corresponding XIL API Server port in CANoe (checkbox under "CANoe Options | Extensions | XIL API & FDX Protocol | XIL API Settings"). Additionally, you need to install the additional components for the ASAM XIL API. The corresponding installer is located in the installation directory of your CANoe installation under "Installer Additional Components\XILAPI".