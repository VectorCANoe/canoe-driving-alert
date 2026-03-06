#--------------------------------------------------------------------------
#Copyright (c) by Vector Informatik GmbH
#--------------------------------------------------------------------------

import vector.canoe # Import CANoe-specific functionalities like timers and event handlers.
from application_layer.ClimateSimulation import TemperatureSimulation # Import the TemperatureSimulation namespace (defined in vCDL) to access its Distributed Objects (DOs).
from application_layer.ClimateSimulation import FanSimulation # Import the FanSimulation namespace (defined in vCDL) to access its Distributed Objects (DOs).
from application_layer import PanelAnimation # Import the PanelAnimation namespace (defined in vCDL) to access its system variables.
from AnimationHelper import AnimationHelper # Import helper functions for panel animations.

import random

@vector.canoe.measurement_script # This decorator registers the class to be instantiated during initialization of the CANoe measurement.
class TemperatureSimulationApplication:
    """
    Temperature Simulation Application for CANoe measurement scripts using the communication concept with Distributed Objects for inter-application data exchange.
    
    This class simulates temperature sensors in a climate control system, providing:
    - Four independent temperature sensors with individual temperature control
    - Automatic mode for random temperature adjustments
    - Interaction with fan simulation for fan speed adjustments based on average temperature
    - Interaction with panel controls for visual animation
    """

    # ========================================================================
    # MEASUREMENT LIFECYCLE METHODS
    # ========================================================================
    
    # Called before measurement start to perform necessary initializations,
    # e.g. to create objects. During measurement, few additional objects
    # should be created to prevent garbage collection runs in time-critical
    # simulations.
    def initialize(self):
        self.INITIAL_TEMPERATURE = 20 # Initial temperature for all sensors [°C]
        self.WARM_TEMPERATURE_RANGE_MIN = 21 # Minimum temperature for WARM state [°C] (yellow). Sensor will be animated green below this value.
        self.WARM_TEMPERATURE_RANGE_MAX = 30 # Maximum temperature for WARM state [°C] (yellow). Sensor will be animated red above this value.
        self.HELP_TEXT = (
            "**** HELP: Press 'a' to toggle automatic mode.                            ****\n"
            "**** HELP: Press 't' to toggle detailed output of temperature simulation. ****\n"
            "**** HELP: Press 'r' to reset temperature simulation.                     ****"
        )

        # ***vector.canoe.Timer***
        # creates a timer that executes a callback function after a specified delay.
        # It can be made cyclic by restarting it in the callback function.
        # Static timers (with fixed delay) should be configured once during initialization.
        self.temperature_publication_animation_timer = vector.canoe.Timer(0.5, self._stop_temperature_publication_animation) # Stops temperature publication animation after 0.5s
        self.automatic_mode_timer = vector.canoe.Timer(1.0, self._randomly_adjust_temperature) # Adjusts temperatures every 1s in automatic mode
        
        self.detailed_output_enabled = False
        self.random_temp_generator = random.Random(33) # Initialize random generator with seed for reproducibility

    # Notification that the measurement starts.
    def start(self):
        # vector.canoe.write writes a message to the CANoe 'Write' window.
        vector.canoe.write(
            "******************************************************************************\n"
            "**** Starting Temperature Simulation Application.                         ****"
        )
        self._reset_simulation()

    # Notification that the measurement ends.
    def stop(self):
        vector.canoe.write("Stopping Temperature Simulation Application")

    # Cleanup after the measurement. Complement to Initialize. This is not
    # a "Dispose" method; your object should still be usable afterwards.
    def shutdown(self):
        if self.temperature_publication_animation_timer:
            self.temperature_publication_animation_timer.cancel()
        if self.automatic_mode_timer:
            self.automatic_mode_timer.cancel()


    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================
    

    # ***vector.canoe.on_key***
    # registers a method as a handler for key press events.
    # The method will be called when the specified key is pressed during the measurement.
    # The decorated method must have a single parameter (additionally to self) to receive the pressed key character.
    # It must be used for methods of the class decorated with measurement_script() only.

    # Toggle automatic mode with 'a' key
    @vector.canoe.on_key('a')
    def key_a_pressed(self, char: str):
        self._toggle_automatic_mode_active()

    # Toggle detailed output with 't' key
    @vector.canoe.on_key('t')
    def key_t_pressed(self, char: str):
        self._toggle_detailed_output()

    # Reset simulation with 'r' key
    @vector.canoe.on_key('r')
    def on_key_r_pressed(self, char: str):
        vector.canoe.write(
            "******************************************************************************\n"
            "**** Resetting Temperature Simulation                                     ****"
        )
        self._reset_simulation()

    # ***vector.canoe.on_update***
    # registers a method as a handler for updates to a Distributed Object (DO).
    # The decorated method should not have any parameters (except self).
    # It must be used for methods of the class decorated with measurement_script() only.

    # React to temperature changes of Sensor1
    @vector.canoe.on_update(TemperatureSimulation.temperatureControlProvidedDO.temperature1)
    def on_temperature1_updated(self):
        temperature = TemperatureSimulation.temperatureControlConsumedDO.temperature1.copy()
        self._write_detailed_output(f"Temperature 1 updated: {temperature}°C")
        self._start_temperature_publication_animation(
            temperature, 
            PanelAnimation.system_variables.stateOfTemperature1,
            PanelAnimation.system_variables.publicationOfTemperature1
        )
        self._calculate_average_temperature()
        FanSimulation.fanConsumedDO.calculateFanSpeed.call_async(TemperatureSimulation.temperatureControlProvidedDO.averageTemperature.copy())

    # React to temperature changes of Sensor2
    @vector.canoe.on_update(TemperatureSimulation.temperatureControlProvidedDO.temperature2)
    def on_temperature2_updated(self):
        temperature = TemperatureSimulation.temperatureControlConsumedDO.temperature2.copy()
        self._write_detailed_output(f"Temperature 2 updated: {temperature}°C")
        self._start_temperature_publication_animation(temperature, 
            PanelAnimation.system_variables.stateOfTemperature2,
            PanelAnimation.system_variables.publicationOfTemperature2
        )
        self._calculate_average_temperature()
        FanSimulation.fanConsumedDO.calculateFanSpeed.call_async(TemperatureSimulation.temperatureControlProvidedDO.averageTemperature.copy())

    # React to temperature changes of Sensor3
    @vector.canoe.on_update(TemperatureSimulation.temperatureControlProvidedDO.temperature3)
    def on_temperature3_updated(self):
        temperature = TemperatureSimulation.temperatureControlConsumedDO.temperature3.copy()
        self._write_detailed_output(f"Temperature 3 updated: {temperature}°C")
        self._start_temperature_publication_animation(
            temperature, 
            PanelAnimation.system_variables.stateOfTemperature3,
            PanelAnimation.system_variables.publicationOfTemperature3
        )
        self._calculate_average_temperature()
        FanSimulation.fanConsumedDO.calculateFanSpeed.call_async(TemperatureSimulation.temperatureControlProvidedDO.averageTemperature.copy())

    # React to temperature changes of Sensor4
    @vector.canoe.on_update(TemperatureSimulation.temperatureControlProvidedDO.temperature4)
    def on_temperature4_updated(self):
        temperature = TemperatureSimulation.temperatureControlConsumedDO.temperature4.copy()
        self._write_detailed_output(f"Temperature 4 updated: {temperature}°C")
        self._start_temperature_publication_animation(
            temperature, 
            PanelAnimation.system_variables.stateOfTemperature4,
            PanelAnimation.system_variables.publicationOfTemperature4
        )
        self._calculate_average_temperature()
        FanSimulation.fanConsumedDO.calculateFanSpeed.call_async(TemperatureSimulation.temperatureControlProvidedDO.averageTemperature.copy())

    # ***vector.canoe.on_change***
    # registers a method as a handler for changes to a Distributed Object (DO).
    # The method will be called when the specified DO changes during the measurement.
    # In contrast to on_update, on_change is only called when the value actually changes (not when it is set to the same value again).
    # To enable change detection for complex members — which may be omitted for performance reasons — add the EnableChangeInfo attribute in the vCDL.
    # The decorated method should not have any parameters (except self).
    # It must be used for methods of the class decorated with measurement_script() only.

    # React to changes in automaticModeActive: Start or stop the automatic temperature adjustment timer.
    @vector.canoe.on_change(TemperatureSimulation.temperatureControlProvidedDO.automaticModeActive)
    def on_automatic_mode_changed(self):
        automatic_mode = TemperatureSimulation.temperatureControlProvidedDO.automaticModeActive.copy()
        if automatic_mode:
            self._write_detailed_output("Starting automatic temperature mode")
            self.automatic_mode_timer.start()
        else:
            self._write_detailed_output("Stopping automatic temperature mode")
            if self.automatic_mode_timer:
                self.automatic_mode_timer.cancel()

    # ========================================================================
    # INTERNAL METHODS
    # ========================================================================
    
    # Write detailed output if enabled
    def _write_detailed_output(self, message: str):
        """Write output only if output is enabled"""
        if self.detailed_output_enabled:
            vector.canoe.write(message)

    # Toggle detailed output state
    def _toggle_detailed_output(self):
        self.detailed_output_enabled = not self.detailed_output_enabled
        status = "ON" if self.detailed_output_enabled else "OFF"
        vector.canoe.write(f"Temperature Simulation Output: {status}")

    # Toggle automatic mode state
    def _toggle_automatic_mode_active(self):
        current_mode = TemperatureSimulation.temperatureControlProvidedDO.automaticModeActive.copy()
        new_mode = not current_mode
        TemperatureSimulation.temperatureControlProvidedDO.automaticModeActive = new_mode
        status = "ON" if new_mode else "OFF"
        vector.canoe.write(f"Automatic Temperature Mode: {status}")

    # Reset simulation state and variables
    def _reset_simulation(self):
        TemperatureSimulation.temperatureControlProvidedDO.automaticModeActive = False

        if self.automatic_mode_timer:
            self.automatic_mode_timer.cancel()
        if self.temperature_publication_animation_timer:
            self.temperature_publication_animation_timer.cancel()
        
        AnimationHelper.reset_all_temperature_animations()
        self._reset_all_temperatures_to_initial()
        self.detailed_output_enabled = False
        self.random_temp_generator = random.Random(33) # Reinitialize random generator with seed for reproducibility

        vector.canoe.write(self.HELP_TEXT)

    # Reset all temperature sensors to the initial temperature
    def _reset_all_temperatures_to_initial(self):
        for sensor_number in range(1, 5):
            temperature_do = self._get_temperature_do_member(sensor_number)
            temperature_do.set_value(self.INITIAL_TEMPERATURE) # Use set_value instead of '=' (which is a name binding operation), to avoid Python Interpreter generating a local variable instead of setting the DO member.

        TemperatureSimulation.temperatureControlProvidedDO.averageTemperature = self.INITIAL_TEMPERATURE

    # Calculate and set the average temperature based on all four sensors
    def _calculate_average_temperature(self):
        average_temperature = (
            TemperatureSimulation.temperatureControlConsumedDO.temperature1.copy() +
            TemperatureSimulation.temperatureControlConsumedDO.temperature2.copy() +
            TemperatureSimulation.temperatureControlConsumedDO.temperature3.copy() +
            TemperatureSimulation.temperatureControlConsumedDO.temperature4.copy()
        ) / 4
        TemperatureSimulation.temperatureControlProvidedDO.averageTemperature = round(average_temperature)

    # Start temperature publication animation for a specific sensor:
    # i.e., light up the line to the sensor and adapt the color of the sensor based on the given temperature.
    def _start_temperature_publication_animation(self, temperature, temperature_state_sysvar, temperature_publication_sysvar):
        AnimationHelper.set_temperature_animation_state(
            temperature, # Temperature value of the current sensor
            temperature_state_sysvar, # For animation of the sensor color
            temperature_publication_sysvar, # For animation of the line to the sensor
            self.WARM_TEMPERATURE_RANGE_MIN,
            self.WARM_TEMPERATURE_RANGE_MAX
        )
        
        self.temperature_publication_animation_timer.start() # Restart timer to stop the animation after the defined interval.

    # Stop all temperature publication animations
    def _stop_temperature_publication_animation(self):
        AnimationHelper.stop_all_temperature_publications()

    # Randomly adjust temperature of one sensor every second in automatic mode
    def _randomly_adjust_temperature(self): 
        # Randomly select a sensor to adjust (1-4)
        sensor_to_adjust = self.random_temp_generator.randint(1, 4)
        
        self._adjust_temperature_for_sensor(sensor_to_adjust)

        # Continue the timer if automatic mode is still active
        if TemperatureSimulation.temperatureControlProvidedDO.automaticModeActive.copy():
            self.automatic_mode_timer.start()

    # Adjust temperature for a specific sensor
    def _adjust_temperature_for_sensor(self, sensor_number):
        temperature_do = self._get_temperature_do_member(sensor_number)
        current_temperature = temperature_do.copy()
        threshold = FanSimulation.fanProvidedDO.thresholdTurnOnFan.copy()

        if current_temperature < threshold:
            # Below threshold: increase temperature
            new_temperature = current_temperature + self.random_temp_generator.randint(4, 7)
        else:
            # At or above threshold: decrease temperature
            new_temperature = current_temperature - self.random_temp_generator.randint(1, 3)
        
        temperature_do.set_value(new_temperature) # Use set_value instead of '=' (which is a name binding operation), to avoid Python Interpreter generating a local variable instead of setting the DO member.

    # Get the appropriate temperature Distributed Object (DO) member based on sensor number
    def _get_temperature_do_member(self, sensor_number):
        if sensor_number == 1:
            return TemperatureSimulation.temperatureControlProvidedDO.temperature1
        elif sensor_number == 2:
            return TemperatureSimulation.temperatureControlProvidedDO.temperature2
        elif sensor_number == 3:
            return TemperatureSimulation.temperatureControlProvidedDO.temperature3
        elif sensor_number == 4:
            return TemperatureSimulation.temperatureControlProvidedDO.temperature4
        else:
            raise ValueError(f"Invalid sensor number: {sensor_number}. Must be 1-4.")