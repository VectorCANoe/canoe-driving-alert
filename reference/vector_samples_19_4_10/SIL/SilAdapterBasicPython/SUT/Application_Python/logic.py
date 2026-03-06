from iolayer import State, get_sensor_value1, get_sensor_value2, get_sensor_value3, set_heater_state

HEATING_THRESHOLD = 18.0
COOLING_THRESHOLD = 23.0

write_to_console_counter = 0

def get_heater_state(temperature: float) -> State:
    if temperature < HEATING_THRESHOLD:
        return State.Heating
    if temperature > COOLING_THRESHOLD:
        return State.Cooling
    return State.Off

def print_status_to_console(sensor1: float, sensor2: float, sensor3: float, heater_state: State) -> None:
    print("Sensor1: " + str(sensor1) +
          ", Sensor2: " + str(sensor2) +
          ", Sensor3: " + str(sensor3) +
          ", Heater is " + heater_state.name)


def calc_temperature(value1: float, value2: float, value3: float) -> float:
    return (value1 + value2 + value3) / 3


def control_room_temperature():
    global write_to_console_counter

    sensor1 = get_sensor_value1()
    sensor2 = get_sensor_value2()
    sensor3 = get_sensor_value3()

    temperature = calc_temperature(sensor1, sensor2, sensor3)

    heater_state = get_heater_state(temperature)

    set_heater_state(heater_state)

    if write_to_console_counter >= 19:
        print_status_to_console(sensor1, sensor2, sensor3, heater_state)
        write_to_console_counter = 0
    else:
        write_to_console_counter += 1
