

#include "CCL/CCL.h"
#include <stdio.h> 
#include <stdlib.h> 


extern void OnMeasurementPreStart();
extern void OnMeasurementStart();
extern void OnTimer1(int64_t time, int32_t timerID);
extern void OnTimer2(int64_t time, int32_t timerID);


int32_t gTimerID1;


void cclOnDllLoad()
{
  cclSetMeasurementPreStartHandler(&OnMeasurementPreStart);
  cclSetMeasurementStartHandler(&OnMeasurementStart);
}


void OnMeasurementPreStart()
{
  gTimerID1 = cclTimerCreate(&OnTimer1);
}


void OnMeasurementStart()
{
  cclTimerSet(gTimerID1, cclTimeMilliseconds(100));
}

void loadAndSendGpbOSI3Data()
{
  size_t total_file_size = 0;
  size_t remaining_file_size = 0;
  size_t byte_offset = 0;
  uint8_t protobufData[4096]; //Adjust array size to open files that are larger than 4kB

  FILE* infile;

#if defined(_MSC_VER)
  fopen_s(&infile, "GPBData.dat", "rb");
#else
  infile = fopen("GPBData.dat", "rb");
#endif

  if (infile != NULL)
  {
    fseek(infile, 0, SEEK_END);
    total_file_size = ftell(infile);
    fseek(infile, 0, SEEK_SET);


    remaining_file_size = total_file_size;
    while (remaining_file_size) {
      size_t byte_read = fread(&protobufData + byte_offset, 1, remaining_file_size, infile);
      byte_offset += byte_read;
      remaining_file_size -= byte_read;
      if (feof(infile) || ferror(infile)) break;
    }

    if (cclSetGpbOSI3Data(protobufData, (int32_t)total_file_size) == CCL_SUCCESS)
    {
      cclWrite("C Library Example: Setting GPB OSI3 Sensor Data was successful");
    }
    else
    {
      cclWrite("C Library Example: Setting GPB OSI3 Sensor Data failed");
    }

    fclose(infile);
  }
}

void OnTimer1(int64_t time, int32_t timerID)
{
  cclWrite("C Library Example: ADAS Update Timer");
  cclTimerSet(gTimerID1, cclTimeMilliseconds(100));
  loadAndSendGpbOSI3Data();
 
}





