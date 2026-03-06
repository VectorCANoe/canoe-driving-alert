/*
 * This file contains functions that access the hardware.
 *
 * These functions represent the functional system interface of the software under test.
 * To establish a communication with CANoe/CANoe4SW the original source code is substituted
 * by calls to the SIL Adapter. Necessary adaptations are marked with "INSTRUMENTATION".
 */

#include "IO.h"

/* Global variable to save detection time (in number of samples) of last detected r-peak*/
unsigned int gLastRPeakDetectionTimeInNumberOfSamplesSinceReset = 0;

/* Sample count since reset*/
unsigned int gSampleCountSinceReset = 0;

/* Array storing the last ten R Peak differences*/
unsigned int gLastRPeakDistancesSinceReset[NUMBER_OF_HEART_RATES_FOR_AVERAGING] = {0};

/* Number of R Peaks since reset*/
unsigned int gNumberOfRPeaksSinceReset = 0;

/* Number of samples since last R Peak detection time*/
unsigned int gSampleCountSinceLastRPeakDetectionTime = 0;

/* Is algorithm reset*/
unsigned int gIsAlgorithmReset = 0;


// ---------- INSTRUMENTATION ----------
#ifdef SIL_TESTING_CONTROLLED_BY_CANOE
#include "TypeLibWrapper.h"
#else
/* Includes of hardware related headers.*/
#endif
// -------------------------------------

void InitializeIO(void)
{
  // ---------- INSTRUMENTATION ----------
  // hw_init();                                                   // original source code
  sil_init();                                                     // call to SIL Adapter
  // -------------------------------------
}

void ShutDownIO(void)
{
  // ---------- INSTRUMENTATION ----------
  // hw_shut_down();                                              // original source code
  sil_shut_down();                                                // call to SIL Adapter
  // -------------------------------------
}

int ReadEcgSample(void)
{
  // ---------- INSTRUMENTATION ----------
  // return hw_read_ecg_sample();                                 // original source code
  return sil_read_ecg_sample();                                   // call to SIL Adapter
  // -------------------------------------
}

void ShowCurrentHeartRateOnDisplay(double current_heart_rate)
{
  // ---------- INSTRUMENTATION ----------
  // hw_show_current_heart_rate_on_display(current_heart_rate);   // original source code
  sil_show_current_heart_rate_on_display(current_heart_rate);     // call to SIL Adapter
  // -------------------------------------
}

void ShowAveragedHeartRateOnDisplay(double averaged_heart_rate)
{
  // ---------- INSTRUMENTATION ----------
  // hw_show_averaged_heart_rate_on_display(averaged_heart_rate); // original source code
  sil_show_averaged_heart_rate_on_display(averaged_heart_rate);   // call to SIL Adapter
  // -------------------------------------
}

void ShowHeartRateAlarmOnDisplay(unsigned int current_heart_rate_alarm)
{
  // ---------- INSTRUMENTATION ----------
  // hw_show_alarm_on_display(current_heart_rate_alarm);          // original source code
  sil_show_alarm_on_display(current_heart_rate_alarm);            // call to SIL Adapter
  // -------------------------------------
}

void SendEcgSampleToECGMonitor(int ecg_sample)
{
  // ---------- INSTRUMENTATION ----------
  // hw_send_ecg_sample_to_ecg_monitor(ecg_sample);               // original source code
  sil_send_ecg_sample_to_ecg_monitor(ecg_sample);                 // call to SIL Adapter
  // -------------------------------------
}

void SendHeartRatesAndAlarmToECGMonitor(double current_heart_rate, double averaged_heart_rate,
                                        unsigned int current_heart_rate_alarm)
{
  // ---------- INSTRUMENTATION ----------
  // hw_send_heart_rates_and_alarm_to_ecg_monitor(current_heart_rate,
  //                                              averaged_heart_rate,
  //                                              current_heart_rate_alarm); // original source code
  sil_send_heart_rates_and_alarm_to_ecg_monitor(current_heart_rate,
                                                averaged_heart_rate,
                                                current_heart_rate_alarm);   // call to SIL Adapter
  // -------------------------------------
}
