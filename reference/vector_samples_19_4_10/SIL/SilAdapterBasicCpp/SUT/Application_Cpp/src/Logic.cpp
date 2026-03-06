/*
 * This file contains the actual application logic.
 */

#include <iomanip>
#include <iostream>

#include "IO.hpp"
#include "Logic.hpp"

static constexpr double gHeatingThreshold = 18.0;
static constexpr double gCoolingThreshold = 23.0;


State GetHeaterState(double temperature) {
  if (temperature < gHeatingThreshold)
  {
    return State::Heating;
  }

  if (temperature > gCoolingThreshold)
  {
    return State::Cooling;
  }

  return State::Off;
}

void PrintStatusToConsole(double sensor1, double sensor2, double sensor3, State heaterState)
{
  auto heaterStateText = "";
  switch (heaterState)
  {
  case State::Off:
    heaterStateText = "Off";
    break;
  case State::Heating:
    heaterStateText = "Heating";
    break;
  case State::Cooling:
    heaterStateText = "Cooling";
  }
  std::cout << std::fixed << std::setprecision(2) << "Sensor1: " << sensor1 << ", Sensor2: " << sensor2
    << ", Sensor3: " << sensor3 << ", Heater is " << heaterStateText << std::endl;
}

double CalcTemperature(double value1, double value2, double value3) { return (value1 + value2 + value3) / 3; }

void ControlRoomTemperature()
{
  static int writeToConsoleCounter = 0;

  const auto sensor1 = GetSensorValue1();
  const auto sensor2 = GetSensorValue2();
  const auto sensor3 = GetSensorValue3();

  const auto temperature = CalcTemperature(sensor1, sensor2, sensor3);

  const auto heaterState = GetHeaterState(temperature);

  SetHeaterState(heaterState);

  if (writeToConsoleCounter++ >= 19)
  {
    PrintStatusToConsole(sensor1, sensor2, sensor3, heaterState);
    writeToConsoleCounter = 0;
  }
}
