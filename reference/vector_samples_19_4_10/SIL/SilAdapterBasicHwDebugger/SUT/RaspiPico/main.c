#include "Logic.h"
#include "IO.h"

#ifdef TARGET_PLATFORM_PICO_HW
#include "pico/stdlib.h"
#define HEATER_STATE_HEATING_LED_PIN 20
#define HEATER_STATE_COOLING_LED_PIN 21
#endif

void io_heater_state_display_init()
{
#ifdef TARGET_PLATFORM_PICO_HW
  gpio_init(HEATER_STATE_HEATING_LED_PIN);
  gpio_init(HEATER_STATE_COOLING_LED_PIN);

  gpio_set_dir(HEATER_STATE_HEATING_LED_PIN, GPIO_OUT);
  gpio_set_dir(HEATER_STATE_COOLING_LED_PIN, GPIO_OUT);
#endif
}

void io_heater_state_display_show(heater_state state)
{
#ifdef TARGET_PLATFORM_PICO_HW
  switch (state)
  {
    case HEATING:
      gpio_put(HEATER_STATE_HEATING_LED_PIN, 1);
      gpio_put(HEATER_STATE_COOLING_LED_PIN, 0);
      break;
    case COOLING:
      gpio_put(HEATER_STATE_HEATING_LED_PIN, 0);
      gpio_put(HEATER_STATE_COOLING_LED_PIN, 1);
      break;
    default:
      gpio_put(HEATER_STATE_HEATING_LED_PIN, 0);
      gpio_put(HEATER_STATE_COOLING_LED_PIN, 0);
      break;
  }
#else
  (void)(state);
#endif
}

int main(void)
{
  io_initialize();

  while(1)
  {
#ifdef SIL_TESTING_ENABLED
    /*
    * In case of SIL Testing the SIL Adapter needs to be polled periodically in order to process method calls 
    * that were queued by CANoe as well as queueing method calls that were done during control_room_temperature and that
    * need to be processed by CANoe.
    */
    io_siladapter_poll();
#endif
    control_room_temperature();
  }

  io_shutdown();

  return 0;
}
