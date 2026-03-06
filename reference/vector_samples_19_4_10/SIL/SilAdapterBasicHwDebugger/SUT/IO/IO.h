// Copyright (c) Vector Informatik GmbH. All rights reserved.

#ifndef IO_SIL_H
#define IO_SIL_H

typedef enum heater_state
{
  OFF,
  COOLING,
  HEATING
} heater_state;

#ifdef SIL_TESTING_ENABLED
void io_siladapter_poll(void);
#endif

void io_initialize(void);
void io_shutdown(void);
void io_set_heater_state(heater_state state);
double io_read_temperature_sensor1(void);
double io_read_temperature_sensor2(void);
double io_read_temperature_sensor3(void);

// The 'display heater-state' functionality was moved to the target-specific
// files to make the IO implementation target-agnostic. For the Pico, you can
// find their implementations in the `main.c` file.

extern void io_heater_state_display_init();
extern void io_heater_state_display_show(heater_state state);

#endif
