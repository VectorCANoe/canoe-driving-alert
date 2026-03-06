#pragma once

#define DLL_EXPORT __declspec(dllexport)

#ifdef __cplusplus
extern "C" {
#endif

  struct ConvertedCoordinates
  {
    double longitude;
    double latitude;
    double altitude;
  };

  // Function to convert WGS84 coordinates to the target system
  DLL_EXPORT ConvertedCoordinates ConvertSystem(double longitude, double latitude, double altitude);

  // Function to convert coordinates from the target system to WGS84
  DLL_EXPORT ConvertedCoordinates ConvertSystemInverse(double longitude, double latitude, double altitude);

  // Function to get the display name of the coordinate system
  DLL_EXPORT const char* GetDisplayName();

#ifdef __cplusplus
}
#endif
