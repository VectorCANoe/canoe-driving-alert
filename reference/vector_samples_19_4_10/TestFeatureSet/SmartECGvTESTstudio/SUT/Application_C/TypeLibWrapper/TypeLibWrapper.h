/*
 * This file contains the C-C++ glue code to access the C++
 * SiL-Adapter from the C application. Needs to be provided by the user.
 */

#pragma once


#ifdef __cplusplus
extern "C"
{
#endif

  void ReadAndEvaluateEcgSample();

  void sil_init();

  void sil_shut_down();

  int sil_read_ecg_sample();

  void sil_show_current_heart_rate_on_display(double current_heart_rate);

  void sil_show_averaged_heart_rate_on_display(double averaged_heart_rate);

  void sil_show_alarm_on_display(unsigned int current_heart_rate_alarm);

  void sil_send_ecg_sample_to_ecg_monitor(int ecg_sample);

  void sil_send_heart_rates_and_alarm_to_ecg_monitor(double current_heart_rate, double averaged_heart_rate, unsigned int current_heart_rate_alarm);

#ifdef __cplusplus
}
#endif
