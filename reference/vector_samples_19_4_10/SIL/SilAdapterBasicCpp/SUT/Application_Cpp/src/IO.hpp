#pragma once

enum class State
{
  Off,
  Cooling,
  Heating
};

/* Initializes the all the IO functionality. */
void InitializeIO();

/* Shuts down all the IO functionality. */
void ShutDownIO();

/* This function reads a value from the 1st sensor. */
double GetSensorValue1();

/* This function reads a value from the 2nd sensor. */
double GetSensorValue2();

/* This function reads a value from the 3rd sensor. */
double GetSensorValue3();

/* This function sets the state of the heater. */
void SetHeaterState(State heaterState);
