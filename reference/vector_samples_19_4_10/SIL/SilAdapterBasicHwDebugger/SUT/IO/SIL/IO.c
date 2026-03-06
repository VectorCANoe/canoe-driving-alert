/*
 * This file contains functions that represent the functional system interface of the software under test.
 * To establish a communication with CANoe/CANoe4SW the original source code (IO/HW), that accesses the
 * real hardware, is substituted by calls to the SIL Adapter (IO/SIL).
 */

#include "IO.h"

#include "SilAdapter/siladapter.h"

 /*
  * The following global variables represent and hold the current sensor values that are set from CANoe.
  */
static double g_sensor1_temperature = 0;
static double g_sensor2_temperature = 0;
static double g_sensor3_temperature = 0;

/*
 * The following global variables are used to store the last set heater state.
 * This information is used to only set the heater state on change.
 */
static heater_state g_heater_state = RoomTemperatureControl_State_OFF;
static int g_heater_state_initialized = 0;

static uint8_t g_show_heater_state_on_led = 0;

void io_siladapter_poll(void)
{
  SilAdapter_poll();
}

void RoomTemperatureControl_Sensor1_SetTemperature(double temperature)
{
  g_sensor1_temperature = temperature;
}

void RoomTemperatureControl_Sensor2_SetTemperature(double temperature)
{
  g_sensor2_temperature = temperature;
}

void RoomTemperatureControl_Sensor3_SetTemperature(double temperature)
{
  g_sensor3_temperature = temperature;
}

void Configuration_Application_SetShowHeaterStateOnLED(uint8_t showHeaterStateOnLED)
{
  io_heater_state_display_show(OFF);

  g_show_heater_state_on_led = showHeaterStateOnLED;
}

void io_set_heater_state(heater_state state)
{
  if (g_show_heater_state_on_led)
  {
    io_heater_state_display_show(state);
  }

  if (g_heater_state != state || !g_heater_state_initialized)
  {
    RoomTemperatureControl_Heater_SetHeaterState_call_async((RoomTemperatureControl_State)state);
    g_heater_state = state;
    g_heater_state_initialized = 1;
  }
}

void io_initialize(void)
{
  SilAdapter_connect();
  g_heater_state_initialized = 0;

  io_heater_state_display_init();
}

double io_read_temperature_sensor1(void)
{
  return g_sensor1_temperature;
}

double io_read_temperature_sensor2(void)
{
  return g_sensor2_temperature;
}

double io_read_temperature_sensor3(void)
{
  return g_sensor3_temperature;
}

void io_shutdown(void)
{
  SilAdapter_disconnect();
}
