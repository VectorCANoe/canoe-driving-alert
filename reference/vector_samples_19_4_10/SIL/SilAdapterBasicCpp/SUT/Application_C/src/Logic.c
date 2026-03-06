/*
 * This file contains the actual application logic.
 */

#include <stdio.h>

#include "IO.h"
#include "Logic.h"

#define HEATING_THRESHOLD 18.0
#define COOLING_THRESHOLD 23.0

enum State GetHeaterState(double temperature) {
  if (temperature < HEATING_THRESHOLD)
  {
    return STATE_HEATING;
  }

  if (temperature > COOLING_THRESHOLD)
  {
    return STATE_COOLING;
  }

  return STATE_OFF;
}

const char* GetHeaterStateString(enum State heaterState)
{
  switch (heaterState) {
  case STATE_OFF:
    return "Off";
  case STATE_HEATING:
    return "Heating";
  case STATE_COOLING:
    return "Cooling";
  default:
    return "Unknown State";
  }
}

void PrintStatusToConsole(double sensor1, double sensor2, double sensor3, enum State heaterState)
{
    printf("Sensor1: %.2f, Sensor2: %.2f, Sensor3: %.2f, Heater is %s\r\n",
      sensor1,
      sensor2,
      sensor3,
      GetHeaterStateString(heaterState));
}

double CalcTemperature(double value1, double value2, double value3) { return (value1 + value2 + value3) / 3.0; }

void ControlRoomTemperature()
{
  static int writeToConsoleCounter = 0;

  const double sensor1 = GetSensorValue1();
  const double sensor2 = GetSensorValue2();
  const double sensor3 = GetSensorValue3();

  const double temperature = CalcTemperature(sensor1, sensor2, sensor3);

  const enum State heaterState = GetHeaterState(temperature);

  SetHeaterState(heaterState);

  if (writeToConsoleCounter++ >= 19)
  {
    PrintStatusToConsole(sensor1, sensor2, sensor3, heaterState);
    writeToConsoleCounter = 0;
  }
}
