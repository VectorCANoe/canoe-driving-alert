/*
 * This file contains functions that access the hardware.
 * 
 * These functions represent the functional system interface of the software under test.
 * To establish a communication with CANoe, the original source code is substituted
 * by calls to the SIL Adapter. Necessary adaptations are marked with "INSTRUMENTATION".
 */

#include "IO.h"

// ---------- INSTRUMENTATION ----------
#include "SilAdapterWrapper.h"
// -------------------------------------

void InitializeIO(void)
{
    // ---------- INSTRUMENTATION ----------
    // hw_init();        // original source code
    ConnectSilAdapter(); // call to SIL Adapter
    // -------------------------------------
}

void ShutDownIO(void)
{
    // ---------- INSTRUMENTATION ----------
    // hw_shut_down();      // original source code
    DisconnectSilAdapter(); // call to SIL Adapter
    // -------------------------------------
}

double GetSensorValue1(void)
{
    // ---------- INSTRUMENTATION ----------
    // return hw_read_sensor_value1();                          // original source code
    return RoomTemperatureControl_Sensor1_Temperature_Get();    // call to SIL Adapter
    // -------------------------------------
}

double GetSensorValue2(void)
{
    // ---------- INSTRUMENTATION ----------
    // return hw_read_sensor_value2();                          // original source code
    return RoomTemperatureControl_Sensor2_Temperature_Get();    // call to SIL Adapter
    // -------------------------------------
}

double GetSensorValue3(void)
{
    // ---------- INSTRUMENTATION ----------
    // return hw_read_sensor_value3();                          // original source code
    return RoomTemperatureControl_Sensor3_Temperature_Get();    // call to SIL Adapter
    // -------------------------------------
}

void SetHeaterState(enum State heaterState)
{
    // ---------- INSTRUMENTATION ----------
    // hw_write_switch_heater_state(heaterState);                 // original source code
    RoomTemperatureControl_Heating_HeaterState_Set(heaterState);  // call to SIL Adapter
    // -------------------------------------
}
