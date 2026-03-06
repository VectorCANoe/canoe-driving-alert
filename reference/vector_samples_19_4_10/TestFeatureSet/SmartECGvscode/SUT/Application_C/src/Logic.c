/*
 * This file contains the actual application logic.
 */

#include <stdio.h>

#include "IO.h"
#include "Logic.h"
#include "limits.h"
#include "QRSDetection.h"

 /* Critical limits for heart rate. */
#define LOWER_HEART_RATE_LIMIT_BPM 60.0
#define UPPER_HEART_RATE_LIMIT_BPM 100.0

/* Calculate heart rate from r peaks. */
struct heart_rate {
  double heart_rate;
  unsigned int is_valid;
};

struct heart_rates {
  struct heart_rate current_heart_rate;
  struct heart_rate averaged_heart_rate;
};


struct heart_rates CalculateHeartRates(unsigned int delay_in_samples) {

  struct heart_rates heart_rates_obj = { {0.0,0},{0.0,0} };

  /* Calculation of heart rate from latest 2 R-Peaks. */
  if (gLastRPeakDetectionTimeInNumberOfSamplesSinceReset != 0) {
    const unsigned int NewRWaveDetectionTimeInNumberOfSamplesSinceReset = gSampleCountSinceReset - delay_in_samples;
    const unsigned int samples_between_r_peaks = NewRWaveDetectionTimeInNumberOfSamplesSinceReset - gLastRPeakDetectionTimeInNumberOfSamplesSinceReset;

    heart_rates_obj.current_heart_rate.heart_rate = (SAMPLE_RATE / ((double)samples_between_r_peaks)) * 60.0;
    heart_rates_obj.current_heart_rate.is_valid = 1;

    gLastRPeakDetectionTimeInNumberOfSamplesSinceReset = NewRWaveDetectionTimeInNumberOfSamplesSinceReset;
    if (gNumberOfRPeaksSinceReset > 1) {
      gLastRPeakDistancesSinceReset[(gNumberOfRPeaksSinceReset - 2) % NUMBER_OF_HEART_RATES_FOR_AVERAGING] = samples_between_r_peaks;
    }

  }
  else {
    gLastRPeakDetectionTimeInNumberOfSamplesSinceReset = gSampleCountSinceReset - delay_in_samples;
  }

  /* Calculation of average heart rate */
  if (gNumberOfRPeaksSinceReset >= NUMBER_OF_HEART_RATES_FOR_AVERAGING + 1) {
    double sum_of_heart_rates = 0;
    for (int i = 0; i < NUMBER_OF_HEART_RATES_FOR_AVERAGING; ++i) {
      sum_of_heart_rates += (SAMPLE_RATE / ((double)gLastRPeakDistancesSinceReset[i])) * 60.0;
    }
    heart_rates_obj.averaged_heart_rate.heart_rate = sum_of_heart_rates / ((double)NUMBER_OF_HEART_RATES_FOR_AVERAGING);
    heart_rates_obj.averaged_heart_rate.is_valid = 1;
  }
  else {
    if (gNumberOfRPeaksSinceReset > 1) {
      double sum_of_heart_rates = 0;
      for (unsigned int i = 0; i < (gNumberOfRPeaksSinceReset - 1); ++i) {
        sum_of_heart_rates += (SAMPLE_RATE / ((double)gLastRPeakDistancesSinceReset[i])) * 60.0;
      }
      heart_rates_obj.averaged_heart_rate.heart_rate = sum_of_heart_rates / ((double)(gNumberOfRPeaksSinceReset - 1));
      heart_rates_obj.averaged_heart_rate.is_valid = 1;
    }
  }


  return heart_rates_obj;

}

/* Determine if alarm if necessary for given heart rate*/
unsigned int GetHeartRateAlarm(double averaged_heart_rate) {
  if (averaged_heart_rate > UPPER_HEART_RATE_LIMIT_BPM || averaged_heart_rate < LOWER_HEART_RATE_LIMIT_BPM) {
    return 1;
  }
return 0;
}


/* This function reads an Ecg-Sample and hands it
 * over to the function for evaluation and analysis,
 * which afterwards it shows the results locally and
 * sends them via SDC. */
void ReadAndEvaluateEcgSample(void)
{
  /* Read sample and feed it to evaluation function. */
  const int ecg_sample = ReadEcgSample();

  EvaluateEcgSample(ecg_sample);
}


/* This function is called when an ecg-sample was measured
 * and hands it over to algorithms for analysis .Afterwards it shows
 * the results locally and send them via SDC. */
void EvaluateEcgSample(int ecg_sample)
{
  int delay_in_samples = 0;
  unsigned int current_heart_rate_alarm = 0;

  /* ECG sample read, increase sample counter. */
  ++gSampleCountSinceReset;
  /* Feed ecg sample to QRS detection algorithm. */
  delay_in_samples = DetectQRS(ecg_sample);

  /* If R Peak/Beat was detected, perform calculation
   * of delay to current ecg sample, r-peak position,
   * heart rates, and alarms and show them locally and
   * send them via SDC. */
  if (delay_in_samples != 0) {
    /* R Peak detected, increase R Peak counter
     * and set algorithm to not reset any more */
    ++gNumberOfRPeaksSinceReset;
    gIsAlgorithmReset = 0;

    /* Reset number of samples since last R Peak detection time. */
    gSampleCountSinceLastRPeakDetectionTime = 0;

    struct heart_rates heart_rates_obj = { {0.0,0},{0.0,0} };

    heart_rates_obj = CalculateHeartRates(delay_in_samples);

    if (heart_rates_obj.averaged_heart_rate.is_valid > 0)
    {
      current_heart_rate_alarm = GetHeartRateAlarm(heart_rates_obj.averaged_heart_rate.heart_rate);
      ShowAveragedHeartRateOnDisplay(heart_rates_obj.averaged_heart_rate.heart_rate);
      ShowHeartRateAlarmOnDisplay(current_heart_rate_alarm);
    }

    if (heart_rates_obj.current_heart_rate.is_valid > 0)
    {
      ShowCurrentHeartRateOnDisplay(heart_rates_obj.current_heart_rate.heart_rate);
    }


    /* Send heart rates + heart rate alarm via SDC to ECG Monitor. */
    if (heart_rates_obj.averaged_heart_rate.is_valid && heart_rates_obj.current_heart_rate.is_valid) {
      SendHeartRatesAndAlarmToECGMonitor(heart_rates_obj.current_heart_rate.heart_rate, heart_rates_obj.averaged_heart_rate.heart_rate, current_heart_rate_alarm);
    }

    printf("Heart beat was detected!\n");
  }
  else {
    /* Increase Sample Count since last R Peak detection time*/
    ++gSampleCountSinceLastRPeakDetectionTime;

    /* Check if ECG pads are disconnected/broken or heart stopped beating */
    if ((gSampleCountSinceLastRPeakDetectionTime / SAMPLE_RATE) >= NUMBER_OF_SECONDS_BEFORE_SIGNALING_MISSING_DETECTION_OF_HEART_BEATS) {
      if (gIsAlgorithmReset == 0) {
        ResetDetectionAlgorithm();
      }

      /* Show and send notification that ECG pads are disconnected/broken or heart stopped beating every 100 samples*/
      if ((gSampleCountSinceLastRPeakDetectionTime % ALARM_AND_HEART_RATE_TRANSFER_FRACTION_NUMBER_IN_CASE_OF_MISSING_HEART_BEAT_DETECTION) == 0) {
        ShowAveragedHeartRateOnDisplay(0);
        ShowHeartRateAlarmOnDisplay(1);
        ShowCurrentHeartRateOnDisplay(0);
        SendHeartRatesAndAlarmToECGMonitor(0, 0, 1);
      }
    }
  }


  /* Send (fraction of) ecg-samples via SDC. */
  if (((gSampleCountSinceReset - 1) % SDC_SAMPLE_TRANSFER_FRACTION_NUMBER) == 0)
  {
    SendEcgSampleToECGMonitor(ecg_sample);
  }

  /* Reset global variables if they reach the data type range (gSampleCountSinceReset will reach it first). */
  if (gSampleCountSinceReset == (UINT_MAX)) {
    ResetDetectionAlgorithm();
  }
}

void ResetDetectionAlgorithm() {
  gLastRPeakDetectionTimeInNumberOfSamplesSinceReset = 0;
  gSampleCountSinceReset = 0;
  gNumberOfRPeaksSinceReset = 0;
  gIsAlgorithmReset = 1;
  for (int i = 0; i < NUMBER_OF_HEART_RATES_FOR_AVERAGING; ++i) {
    gLastRPeakDistancesSinceReset[i] = 0;
  }
  ResetQRSDetectionAlgorithm();
}
