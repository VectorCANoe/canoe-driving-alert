/*
 * This file contains the C-C++ glue code to access the C++
 * SiL-Adapter from the C application. Needs to be provided by the user.
 */

#pragma once

#ifdef __cplusplus
extern "C"
{
#endif

  enum State
  {
    STATE_OFF,
    STATE_COOLING,
    STATE_HEATING
  };

  // Vector::CANoe::SilAdapter::Connect()
  void ConnectSilAdapter();

  // Vector::CANoe::SilAdapter::Disconnect()
  void DisconnectSilAdapter();

  // RoomTemperatureControl::Sensor1::Temperature
  double RoomTemperatureControl_Sensor1_Temperature_Get();

  // RoomTemperatureControl::Sensor2::Temperature
  double RoomTemperatureControl_Sensor2_Temperature_Get();

  // RoomTemperatureControl::Sensor3::Temperature
  double RoomTemperatureControl_Sensor3_Temperature_Get();

  // RoomTemperatureControl::Heating::HeaterState
  void RoomTemperatureControl_Heating_HeaterState_Set(enum State heaterState);

#ifdef __cplusplus
}
#endif
