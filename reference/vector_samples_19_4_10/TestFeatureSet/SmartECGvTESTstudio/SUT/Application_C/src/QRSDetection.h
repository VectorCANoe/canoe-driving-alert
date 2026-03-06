#pragma once

#define NSR 0
#define NOISE 1
#define QRS 2

/* Function determines if a QRS complex was detected.
  * param EcgSample. EcgSample represents one data point in the signal.
  * returns Number of samples between detected qrs complex and the previous detected qrs complex. */
int DetectQRS(int EcgSample);

/* Function resets QRS complex detection algorithm.*/
void ResetQRSDetectionAlgorithm();