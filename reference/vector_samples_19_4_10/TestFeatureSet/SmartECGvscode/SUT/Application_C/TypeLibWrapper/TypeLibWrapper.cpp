/*
 * This file contains the C-C++ glue code to access the C++
 * SIL Adapter from the C application. Needs to be provided by the user.
 */

#include "TypeLibWrapper.h"
#include "SilAdapter/SilAdapter.hpp"


 // disable warnings about C-enums in C++-Code
#pragma warning (disable: 26812) 

extern "C"
{
  void sil_init() { Vector::CANoe::SilAdapter::Connect();
    SmartECG::SmartECG_IO.ecgAmplitude.RegisterOnUpdateHandler(&ReadAndEvaluateEcgSample);
   }

  void sil_shut_down() { Vector::CANoe::SilAdapter::Disconnect(); }

  int sil_read_ecg_sample() { return SmartECG::SmartECG_IO.ecgAmplitude;}

  void sil_show_current_heart_rate_on_display(double current_heart_rate)
  {
    SmartECG::SmartECG_IO.currentHeartRate = current_heart_rate;
  }

  void sil_show_averaged_heart_rate_on_display(double averaged_heart_rate)
  {
    SmartECG::SmartECG_IO.averagedHeartRate = averaged_heart_rate;
  }

  void sil_show_alarm_on_display(unsigned int current_heart_rate_alarm)
  {
    SmartECG::SmartECG_IO.heartRateAlarmOn = static_cast<bool>(current_heart_rate_alarm);
  }

  void sil_send_ecg_sample_to_ecg_monitor(int ecg_sample)
  {
    SmartECG::ECGMonitor.ecgSample = ecg_sample;
  }

  void sil_send_heart_rates_and_alarm_to_ecg_monitor(double current_heart_rate, double averaged_heart_rate, unsigned int current_heart_rate_alarm)
  {
    SmartECG::ECGMonitor.currentHeartRate = current_heart_rate;
    SmartECG::ECGMonitor.averagedHeartRate = averaged_heart_rate;
    SmartECG::ECGMonitor.heartRateCritical = static_cast<bool>(current_heart_rate_alarm);
  }

}