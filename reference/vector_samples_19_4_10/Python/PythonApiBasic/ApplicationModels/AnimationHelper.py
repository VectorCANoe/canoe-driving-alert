#--------------------------------------------------------------------------
#Copyright (c) by Vector Informatik GmbH
#--------------------------------------------------------------------------

"""
Animation Helper Module

This module provides centralized animation utilities for both FanSimulation and TemperatureSimulation.
It handles all PanelAnimation namespace operations to keep animation logic separate from simulation logic.
"""

from application_layer import PanelAnimation


class AnimationHelper:
    """Helper class for managing panel animations"""
    
    @staticmethod
    def reset_fan_animation():
        """Reset fan animation to stopped position"""
        PanelAnimation.system_variables.fanState.impl_value = PanelAnimation.FanState.BLADE_POSITION_0
    
    @staticmethod
    def reset_all_temperature_animations():
        """Reset all temperature animations to initial state"""
        AnimationHelper.stop_all_temperature_publications()
        AnimationHelper._reset_all_temperature_states_to_cold()
    
    @staticmethod
    def set_temperature_animation_state(temperature, temperature_state_sysvar, temperature_publication_sysvar, warm_temperature_range_min, warm_temperature_range_max):
        """
        Set temperature animation state based on temperature value
        
        Args:
            temperature: Current temperature value
            temperature_state_sysvar: Temperature state system variable (e.g., PanelAnimation.system_variables.stateOfTemperature1)
            temperature_publication_sysvar: Temperature publication system variable (e.g., PanelAnimation.system_variables.publicationOfTemperature1)
            warm_temperature_range_min: Minimum temperature for WARM state
            warm_temperature_range_max: Maximum temperature for WARM state
        """

        temperature_state = AnimationHelper._get_temperature_state(temperature, warm_temperature_range_min, warm_temperature_range_max)
        temperature_state_sysvar.impl_value = temperature_state
        temperature_publication_sysvar.impl_value = PanelAnimation.TemperaturePublication.ON
    
    @staticmethod
    def _get_temperature_state(temperature, warm_temperature_range_min=21, warm_temperature_range_max=30):
        if warm_temperature_range_min <= temperature <= warm_temperature_range_max:
            return PanelAnimation.TemperatureState.WARM
        elif temperature > warm_temperature_range_max:
            return PanelAnimation.TemperatureState.HOT 
        else:
            return PanelAnimation.TemperatureState.COLD

    @staticmethod
    def stop_all_temperature_publications():
        """Stop all temperature publication animations"""
        PanelAnimation.system_variables.publicationOfTemperature1.impl_value = PanelAnimation.TemperaturePublication.OFF
        PanelAnimation.system_variables.publicationOfTemperature2.impl_value = PanelAnimation.TemperaturePublication.OFF
        PanelAnimation.system_variables.publicationOfTemperature3.impl_value = PanelAnimation.TemperaturePublication.OFF
        PanelAnimation.system_variables.publicationOfTemperature4.impl_value = PanelAnimation.TemperaturePublication.OFF

    @staticmethod
    def _reset_all_temperature_states_to_cold():
        """Reset temperature states to COLD (for initial temperature of 20°C)"""
        PanelAnimation.system_variables.stateOfTemperature1.impl_value = PanelAnimation.TemperatureState.COLD
        PanelAnimation.system_variables.stateOfTemperature2.impl_value = PanelAnimation.TemperatureState.COLD
        PanelAnimation.system_variables.stateOfTemperature3.impl_value = PanelAnimation.TemperatureState.COLD
        PanelAnimation.system_variables.stateOfTemperature4.impl_value = PanelAnimation.TemperatureState.COLD

    @staticmethod
    def advance_fan_animation():
        """
        Advance fan animation to next blade position
        Returns the new state value
        """
        current_state = PanelAnimation.system_variables.fanState.impl_value
        new_state = current_state + 1
        if new_state > PanelAnimation.FanState.BLADE_POSITION_5:
            new_state = PanelAnimation.FanState.BLADE_POSITION_0
        PanelAnimation.system_variables.fanState.impl_value = new_state
        return new_state
