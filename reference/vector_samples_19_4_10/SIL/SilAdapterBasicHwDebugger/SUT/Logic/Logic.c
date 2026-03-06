// Copyright (c) Vector Informatik GmbH. All rights reserved.

#include "Logic.h"

#include "IO.h"

#define HEATING_THRESHOLD 18.0
#define COOLING_THRESHOLD 23.0

heater_state calc_heater_state(double temperature)
{
  if (temperature < HEATING_THRESHOLD) return HEATING;

  return (temperature > COOLING_THRESHOLD) ? COOLING : OFF;
}

double calc_average_temperature(double value1, double value2, double value3)
{
  return (value1 + value2 + value3) / 3.0;
}

void control_room_temperature(void)
{
  const double temperature = calc_average_temperature(io_read_temperature_sensor1(),
    io_read_temperature_sensor2(),
    io_read_temperature_sensor3());

  const heater_state heater_state = calc_heater_state(temperature);

  io_set_heater_state(heater_state);
}
