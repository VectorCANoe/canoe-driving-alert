// CoordinateConversion.c

#include "../CoordinateConversion.h"

ConvertedCoordinates ConvertSystem(const double longitude, const double latitude, const double altitude) {

  // Implement the conversion logic here.
  // The following is an illustrative example:

  ConvertedCoordinates result;

  // Dummy transformation for demonstration purposes
  result.longitude = longitude + 0.0003; // Adjust longitude
  result.latitude = latitude + 0.0003;   // Adjust latitude
  result.altitude = altitude + 0.0003;   // Adjust altitude
  return result;
}

ConvertedCoordinates ConvertSystemInverse(const double longitude, const double latitude, const double altitude) {

  // Implement the inverse conversion logic here.
  // The following is an illustrative example:

  ConvertedCoordinates result;

  // Dummy transformation for demonstration purposes
  result.longitude = longitude - 0.0003; // Adjust longitude
  result.latitude = latitude - 0.0003;   // Adjust latitude
  result.altitude = altitude - 0.0003;   // Adjust altitude
  return result;
}

// Example implementation of display name function
const char* GetDisplayName() {
  return "Example Target System"; // Replace with actual system name, e.g., "GCJ-02" or "BD-09"
}
