// Copyright (c) Vector Informatik GmbH. All rights reserved.

#include <stdint.h>

#include "IO.h"

#include "pico/stdlib.h"
#include "hardware/adc.h"

#define TEMPERATURE_SENSOR_1_GPIO_PIN 4
#define TEMPERATURE_SENSOR_2_GPIO_PIN 5
#define TEMPERATURE_SENSOR_3_GPIO_PIN 6
#define HEATER_STATE_DISPLAY_LED_PIN 10

double read_sensor_temperature_celsius(uint16_t sensor_pin)
{
  adc_select_input(sensor_pin);
  const double conversionFactor = 3.3f / (1 << 12);

  double adc = (double)adc_read() * conversionFactor;
  double temperatureC = 27.0f - (adc - 0.7066f) / 0.001721f;

  return temperatureC;
}

void io_set_heater_state(heater_state state)
{
  gpio_put(HEATER_STATE_DISPLAY_LED_PIN, state);
}

void io_initialize(void)
{
  stdio_init_all();

  gpio_init(TEMPERATURE_SENSOR_1_GPIO_PIN),
  gpio_init(TEMPERATURE_SENSOR_2_GPIO_PIN),
  gpio_init(TEMPERATURE_SENSOR_3_GPIO_PIN),
  gpio_set_dir(TEMPERATURE_SENSOR_1_GPIO_PIN, GPIO_IN);
  gpio_set_dir(TEMPERATURE_SENSOR_2_GPIO_PIN, GPIO_IN);
  gpio_set_dir(TEMPERATURE_SENSOR_3_GPIO_PIN, GPIO_IN);

  gpio_init(HEATER_STATE_DISPLAY_LED_PIN),
  gpio_set_dir(HEATER_STATE_DISPLAY_LED_PIN, GPIO_OUT);

  adc_init();
}

double io_read_temperature_sensor1(void)
{
  return read_sensor_temperature_celsius(TEMPERATURE_SENSOR_1_GPIO_PIN);
}

double io_read_temperature_sensor2(void)
{
  return read_sensor_temperature_celsius(TEMPERATURE_SENSOR_2_GPIO_PIN);
}

double io_read_temperature_sensor3(void)
{
  return read_sensor_temperature_celsius(TEMPERATURE_SENSOR_3_GPIO_PIN);
}

void io_shutdown(void)
{
}
