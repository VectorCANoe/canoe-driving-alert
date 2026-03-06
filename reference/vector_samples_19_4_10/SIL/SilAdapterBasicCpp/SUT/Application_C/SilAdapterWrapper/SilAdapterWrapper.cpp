/*
 * This file contains the C-C++ glue code to access the C++
 * SIL Adapter from the C application. Needs to be provided by the user.
 */

#include "SilAdapterWrapper.h"
#include "SilAdapter/SilAdapter.hpp"

 // disable warnings about C-enums in C++-Code
#pragma warning (disable: 26812) 

extern "C"
{
  void ConnectSilAdapter() { Vector::CANoe::SilAdapter::Connect(); }

  void DisconnectSilAdapter() { Vector::CANoe::SilAdapter::Disconnect(); }

  double RoomTemperatureControl_Sensor1_Temperature_Get() { return RoomTemperatureControl::Sensor1.Temperature; }

  double RoomTemperatureControl_Sensor2_Temperature_Get() { return RoomTemperatureControl::Sensor2.Temperature; }

  double RoomTemperatureControl_Sensor3_Temperature_Get() { return RoomTemperatureControl::Sensor3.Temperature; }

  void RoomTemperatureControl_Heating_HeaterState_Set(enum State heaterState)
  {
    RoomTemperatureControl::Heating.HeaterState = static_cast<RoomTemperatureControl::State>(heaterState);
  }
}