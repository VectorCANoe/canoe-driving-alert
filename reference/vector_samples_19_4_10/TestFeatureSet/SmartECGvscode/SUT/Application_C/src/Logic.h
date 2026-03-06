#pragma once

/* Reads and evaluates an ecg sample. */
void ReadAndEvaluateEcgSample();

/* Function is called when ecg sample value is measured. */
void EvaluateEcgSample(int ecg_sample);

/* Function is called to reset the beat detection algorithm. */
void ResetDetectionAlgorithm();