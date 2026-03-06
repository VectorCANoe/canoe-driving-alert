// Timer.cpp : Example of a CANalyzer/CANoe C Library
//
// This sample file demonstrates the usage timers in a 
// CANalyzer/CANoe C Library.
//

#include "CCL/CCL.h"


extern void OnMeasurementPreStart();
extern void OnMeasurementStart();
extern void OnTimer1(int64_t time, int32_t timerID);
extern void OnTimer2(int64_t time, int32_t timerID);


int32_t gTimerID1;
int32_t gTimerID2;


void cclOnDllLoad()
{
  cclSetMeasurementPreStartHandler(&OnMeasurementPreStart);
  cclSetMeasurementStartHandler(&OnMeasurementStart);
}


void OnMeasurementPreStart()
{
  gTimerID1 = cclTimerCreate(&OnTimer1);
  gTimerID2 = cclTimerCreate(&OnTimer2);
}


void OnMeasurementStart()
{
  cclTimerSet(gTimerID1, cclTimeMilliseconds(300) );
  cclTimerSet(gTimerID2, cclTimeSeconds(2) );
}


void OnTimer1(int64_t time, int32_t timerID)
{
  cclWrite("C Library Example: OnTimer1");

  cclTimerSet(gTimerID1, cclTimeMicroseconds(251050) );
}


void OnTimer2(int64_t time, int32_t timerID)
{
  cclWrite("C Library Example: OnTimer2");

  cclTimerCancel(gTimerID1);
}