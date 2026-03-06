/*
 * This file contains the application's entry point.
 */
#include <stdio.h>

#include "Logic.h"
#include "IO.h"

#ifdef _MSC_VER
#include <windows.h>
#else
#include <unistd.h>
#define Sleep(x) usleep((x)*1000)
#endif

#define LOOP_SLEEP Sleep((unsigned long)(1.0/SAMPLE_RATE)*1000);

int main()
{
  printf("Smart ECG Application, version 1.0\r\n\r\n");

  ResetDetectionAlgorithm();

  /* Register callback to read ECG input every 5 ms. */
  InitializeIO();

  for (;;)
  {
    /* Loop to keep device alive while reading ECG input. */
    LOOP_SLEEP
  }

  ShutDownIO();

  return 0;
}
