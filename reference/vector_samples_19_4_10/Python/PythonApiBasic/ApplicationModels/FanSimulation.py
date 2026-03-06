#--------------------------------------------------------------------------
#Copyright (c) by Vector Informatik GmbH
#--------------------------------------------------------------------------

import vector.canoe # Import CANoe-specific functionalities like timers and event handlers
from application_layer.ClimateSimulation import FanSimulation # Import the FanSimulation namespace (defined in vCDL) to access its Distributed Objects (DOs)
from application_layer.ClimateSimulation import TemperatureSimulation # Import the TemperatureSimulation namespace (defined in vCDL) to access its Distributed Objects (DOs)
from AnimationHelper import AnimationHelper # Import helper functions for panel animations

@vector.canoe.measurement_script # This decorator registers the class to be instantiated during initialization of the CANoe measurement.
class FanSimulationApplication:
    """
    Fan Simulation Application for CANoe measurement scripts using the communication concept with Distributed Objects for inter-application data exchange.
    
    This class simulates a cooling fan in a climate control system, providing:
    - Dynamic fan speed control based on average temperature input
    - Configurable temperature threshold for fan activation
    - Interaction with temperature simulation for dynamic reaction to changing average temperature input
    - Interaction with panel controls for visual fan blade animation with speed-dependent timing
    """

    # ========================================================================
    # MEASUREMENT LIFECYCLE METHODS
    # ========================================================================
    
    # Called before measurement start to perform necessary initializations,
    # e.g. to create objects. During measurement, few additional objects
    # should be created to prevent garbage collection runs in time-critical
    # simulations.
    def initialize(self):
        self.MAX_FAN_SPEED_RPM = 6000 # Maximum speed of the fan [RPM - revolutions per minute]
        self.MIN_FAN_SPEED_RPM = 150  # Minimum speed when fan turns on [RPM - revolutions per minute]
        self.DEFAULT_THRESHOLD_TURN_ON_FAN = 25  # Default temperature threshold to turn on the fan [°C]
        self.HELP_TEXT = (
            "**** HELP: Press 'f' to toggle detailed output of fan simulation.         ****\n"
            "**** HELP: Press 'r' to reset fan simulation.                             ****"
        )

        # ***vector.canoe.Timer***
        # creates a timer that executes a callback function after a specified delay.
        # It can be made cyclic by restarting it in the callback function.
        # Static timers (with fixed delay) should be configured once during initialization.
        # However, in this case the specified delay depends on the fan speed and is thus variable.
        # It needs to be reconfigured everytime the fan speed changes.
        self.fan_speed_animation_timer = None
        
        self.last_fan_speed_rpm = 0
        self.detailed_output_enabled = False

    # Notification that the measurement starts.
    def start(self):
        # vector.canoe.write writes a message to the CANoe 'Write' window.
        vector.canoe.write(
            "******************************************************************************\n"
            "**** Starting Fan Simulation Application.                                 ****"
        )
        self._reset_simulation()
    
    # Notification that the measurement ends.
    def stop(self):
        vector.canoe.write("Stopping Fan Simulation Application")
    
    # Cleanup after the measurement. Complement to Initialize. This is not
    # a "Dispose" method; your object should still be usable afterwards.
    def shutdown(self):
        if self.fan_speed_animation_timer:
            self.fan_speed_animation_timer.cancel()


    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================

    # ***vector.canoe.on_key***
    # registers a method as a handler for key press events.
    # The method will be called when the specified key is pressed during the measurement.
    # The decorated method must have a single parameter (additionally to self) to receive the pressed key character.
    # It must be used for methods of the class decorated with measurement_script() only.

    # Toggle detailed output with 'f' key
    @vector.canoe.on_key('f')
    def on_key_f_pressed(self, char: str):
        self._toggle_detailed_output()

    # Reset simulation with 'r' key
    @vector.canoe.on_key('r')
    def on_key_r_pressed(self, char: str):
        vector.canoe.write(
            "******************************************************************************\n"
            "**** Resetting Fan Simulation                                             ****"
        )
        self._reset_simulation()

    # ***vector.canoe.on_change***
    # registers a method as a handler for changes to a Distributed Object (DO).
    # The method will be called when the specified DO changes during the measurement.
    # In contrast to on_update, on_change is only called when the value actually changes (not when it is set to the same value again).
    # To enable change detection for complex members — which may be omitted for performance reasons — add the EnableChangeInfo attribute in the vCDL.
    # The decorated method should not have any parameters (except self).
    # It must be used for methods of the class decorated with measurement_script() only.

    # React to changes in thresholdTurnOnFan: Call calculateFanSpeed with the current average temperature to adapt fan speed if necessary.
    @vector.canoe.on_change(FanSimulation.fanProvidedDO.thresholdTurnOnFan)
    def on_threshold_changed(self):
        self._write_detailed_output(f"Threshold changed, recalculating fan speed")
        FanSimulation.fanConsumedDO.calculateFanSpeed.call_async(TemperatureSimulation.temperatureControlConsumedDO.averageTemperature.copy())

    # ***vector.canoe.on_call***
    # registers a method as a handler for calls to a Distributed Object (DO).
    # The method will be called when the specified DO is called during the measurement.
    # The decorated method should take the same parameters as the function prototype
    # (additionally to self) and have the same return type.
    # It must be used for methods of the class decorated with measurement_script() only.

    # Handle fan speed calculation calls: Calculate and set fan speed based on the given temperature.
    @vector.canoe.on_call(FanSimulation.fanProvidedDO.calculateFanSpeed)
    def on_calculate_fan_speed_called(self, temperature: int):
        self._calculate_fan_speed(temperature)


    # ========================================================================
    # INTERNAL METHODS
    # ========================================================================
    
    # Write detailed output if enabled
    def _write_detailed_output(self, message: str):
        if self.detailed_output_enabled:
            vector.canoe.write(message)

    # Toggle detailed output state
    def _toggle_detailed_output(self):
        self.detailed_output_enabled = not self.detailed_output_enabled
        status = "ON" if self.detailed_output_enabled else "OFF"
        vector.canoe.write(f"Fan Simulation Output: {status}")

    # Reset simulation state and variables
    def _reset_simulation(self):
        FanSimulation.fanProvidedDO.fanSpeed = 0
        FanSimulation.fanProvidedDO.thresholdTurnOnFan = self.DEFAULT_THRESHOLD_TURN_ON_FAN

        self.fan_speed_animation_timer = None    
        self.last_fan_speed_rpm = 0
        self.detailed_output_enabled = False
        
        AnimationHelper.reset_fan_animation()
        self._configure_fan_speed_animation_timer()

        vector.canoe.write(self.HELP_TEXT)

    # Calculate and set fan speed based on the given temperature
    def _calculate_fan_speed(self, temperature):
        threshold = FanSimulation.fanProvidedDO.thresholdTurnOnFan.copy()
        
        self._write_detailed_output(f"Fan speed calculation: temperature={temperature}°C, threshold={threshold}°C")

        if temperature >= threshold:
            temperature_excess = temperature - threshold
            target_fan_speed_rpm = temperature_excess * self.MIN_FAN_SPEED_RPM        
            target_fan_speed_rpm = max(self.MIN_FAN_SPEED_RPM, min(target_fan_speed_rpm, self.MAX_FAN_SPEED_RPM))

            FanSimulation.fanProvidedDO.fanSpeed = target_fan_speed_rpm
            self._write_detailed_output(f"Fan ON: speed={target_fan_speed_rpm} RPM")
        else:
            FanSimulation.fanProvidedDO.fanSpeed = 0
            self._write_detailed_output("Fan OFF: temperature below threshold")

        self._configure_fan_speed_animation_timer()

    # Configure or reconfigure the fan speed animation timer based on current fan speed
    def _configure_fan_speed_animation_timer(self):
        current_fan_speed_rpm = FanSimulation.fanProvidedDO.fanSpeed.copy()
        
        if current_fan_speed_rpm == 0:
            if self.fan_speed_animation_timer:
                self._write_detailed_output("Stopping fan animation timer")
                self.fan_speed_animation_timer.cancel()
                self.fan_speed_animation_timer = None
        else:
            time_interval_seconds = 60 / current_fan_speed_rpm

            # Only reconfigure timer if fan speed changed
            if self.last_fan_speed_rpm != current_fan_speed_rpm:
                if self.fan_speed_animation_timer:
                    self.fan_speed_animation_timer.cancel()

                self._write_detailed_output(f"Fan speed changed: Reconfiguring fan animation timer with interval {time_interval_seconds:.4f} seconds")
            self.fan_speed_animation_timer = vector.canoe.Timer(time_interval_seconds, self._animate_fan_rotation)
            self.fan_speed_animation_timer.start()
        
        self.last_fan_speed_rpm = current_fan_speed_rpm

    # Advance fan animation based on current fan speed
    def _animate_fan_rotation(self):
        current_fan_speed_rpm = FanSimulation.fanProvidedDO.fanSpeed.copy()
        
        if current_fan_speed_rpm > 0:
            AnimationHelper.advance_fan_animation()
            
            if self.fan_speed_animation_timer:
                self.fan_speed_animation_timer.start()
        else:
            self._write_detailed_output("Fan speed became 0, stopping animation")
            if self.fan_speed_animation_timer:
                self.fan_speed_animation_timer.cancel()
                self.fan_speed_animation_timer = None