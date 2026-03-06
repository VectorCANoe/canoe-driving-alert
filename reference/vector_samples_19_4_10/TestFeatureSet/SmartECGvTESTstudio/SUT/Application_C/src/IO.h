#pragma once

#define NUMBER_OF_HEART_RATES_FOR_AVERAGING 10

#define SDC_SAMPLE_TRANSFER_FRACTION_NUMBER 2

#define SAMPLE_RATE 200

#define NUMBER_OF_SECONDS_BEFORE_SIGNALING_MISSING_DETECTION_OF_HEART_BEATS 10

#define ALARM_AND_HEART_RATE_TRANSFER_FRACTION_NUMBER_IN_CASE_OF_MISSING_HEART_BEAT_DETECTION 100

/* Global variable to save time of last detected r-peak*/
extern unsigned int gLastRPeakDetectionTimeInNumberOfSamplesSinceReset; 

/* Sample count since reset*/
extern unsigned int gSampleCountSinceReset;

/* Array storing the last ten R Peak differences*/
extern unsigned int gLastRPeakDistancesSinceReset[NUMBER_OF_HEART_RATES_FOR_AVERAGING];

/* Number of R Peaks since reset*/
extern unsigned int gNumberOfRPeaksSinceReset;

/* Number of samples since last R Peak detection time*/
extern unsigned int gSampleCountSinceLastRPeakDetectionTime;

/* Is algorithm reset*/
extern unsigned int gIsAlgorithmReset;


/* Initializes the all the IO functionality. */
void InitializeIO(void);

/* Shuts down all the IO functionality. */
void ShutDownIO(void);

/* This function reads a measured ecg sample. */
int ReadEcgSample(void);

/* This function shows the heart rate calculated from the last two R-Peaks locally on the display*/
void ShowCurrentHeartRateOnDisplay(double current_heart_rate);

/* This function shows the averaged heart rate locally on the display*/
void ShowAveragedHeartRateOnDisplay(double averaged_heart_rate);

/* This function shows the current heart rate alarm locally on the display*/
void ShowHeartRateAlarmOnDisplay(unsigned int current_heart_rate_alarm);

/* This function sends an ecg-sample to subscribed SDC consumers*/
void SendEcgSampleToECGMonitor(int ecg_sample);

/* This functions send the current and averaged heart rate and the heart rate alarm to subscribed SDC consumers*/
void SendHeartRatesAndAlarmToECGMonitor(double current_heart_rate, double averaged_heart_rate, unsigned int current_heart_rate_alarm);





