/*
  This file contains the implementation of the QRS detection based of the Pan Tompkins Real-Time QRS Detection Algorithm.
  The chosen parameters and threshold are strongly coupled to the used test samples in this demo.
  We do not guarantee this implementation to work with any other test data.
*/

#include "QRSDetection.h"

#include <math.h>

static double SPKF = 0.0;
static double NPKF = 0.0;
static double RRInterval = 1000.0;
static double RRLow = 0.0;
static double RRHigh = 0.0;

static int SampleIndex = 0;
static int PreviousQRSIndex = 0;

static double Threshold = 20;
static double RRAverage = 1.0;
static int State = NSR;

static double SPKFalpha = 20.0;
static double SPKFbeta = 250.0;
static double NPKFalpha = 20.0;
static double NPKFbeta = 250.0;
static double RRLowFactor = 920.0;
static double RRHighFactor = 1160.0;
static int ThresholdUpdateFactor = 20;
static int ThresholdDecayFactor = 5;

int DetectQRS(int EcgSample) {

  int DelayBetweenSamples = 0;

  // QRS detection logic
  if (State == NSR)
  {
    if (EcgSample > Threshold) {
      // QRS complex detected
      State = QRS;

      // Update SPKF
      SPKF = (SPKFalpha * fabs(EcgSample) + (200 - SPKFalpha) * Threshold) / 200;

      // Update RR interval average
      RRInterval = 1000.0 / ((200 - SPKFbeta) * RRAverage / 200.0 + SPKFbeta);
      RRAverage = RRInterval;

      // Update RRLow and RRHigh limits
      RRLow = RRLowFactor * RRInterval / 200.0;
      RRHigh = RRHighFactor * RRInterval / 200.0;

      // Calculate delay (replace this with your own delay calculation)
      // If Sample Delay is smaller than 50 we assume that the samples belong to the same peak.
      if (SampleIndex - PreviousQRSIndex > 50)
      {
        DelayBetweenSamples = SampleIndex - PreviousQRSIndex;
        PreviousQRSIndex = SampleIndex;
      }
    }
    else {
      // No QRS complex detected, update NPKF
      NPKF = (NPKFalpha * fabs(EcgSample) + (200 - NPKFalpha) * Threshold) / 200.0;
    }
  }

  if (State == QRS)
  {
    if (EcgSample > Threshold) {
      // QRS complex continues
      
      // Update SPKF
      SPKF = (SPKFalpha * EcgSample + (200 - SPKFalpha) * Threshold) / 200;

      // Update RR interval average
      RRInterval = 1000.0 / ((200 - SPKFbeta) * RRAverage / 200.0 + SPKFbeta);
      RRAverage = RRInterval;

      // Update RR_low and RR_high limits
      RRLow = RRLowFactor * RRInterval / 200.0;
      RRHigh = RRHighFactor * RRInterval / 200.0;
    }
    else {
      // QRS complex ends
      State = NSR;

      // Update NPKF
      NPKF = (NPKFbeta * fabs(EcgSample) + (200 - NPKFbeta) * Threshold) / 200.0;
      Threshold = NPKF + (ThresholdDecayFactor * (Threshold - NPKF) / 200.0);
    }
  }

  // Update threshold
  Threshold = NPKF + (ThresholdUpdateFactor * (RRAverage - RRInterval) / 200.0);
  SampleIndex++;
  return DelayBetweenSamples;
}

void ResetQRSDetectionAlgorithm()
{
  SPKF = 0.0, NPKF = 0.0, RRInterval = 1000.0;
  RRLow = 0.0, RRHigh = 0.0;
  SampleIndex = 0;
  PreviousQRSIndex = 0;

  Threshold = 20;
  RRAverage = 1.0;
  State = NSR;
}