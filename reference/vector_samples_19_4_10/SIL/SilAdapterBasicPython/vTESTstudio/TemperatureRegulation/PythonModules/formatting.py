def get_heater_state_string(heater_state: int):
  if heater_state == 0:
    return "Off"
  if heater_state == 1:
    return "Cooling"
  if heater_state == 2:
    return "Heating"