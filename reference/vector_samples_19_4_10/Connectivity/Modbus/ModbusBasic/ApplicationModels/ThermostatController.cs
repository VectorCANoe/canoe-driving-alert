using System;
using Vector.CANoe.Runtime;

/// <summary>
/// "Smart" thermostat controller that gets the state of the window and thermostat setting and adjusts the valve accordingly.
/// </summary>
public class ThermostatController : MeasurementScript
{
    /// <summary>
    /// Update simulation variables every X milliseconds.
    /// </summary>
    const int TIMER_STEP_MS = 200;
    const double DELTA_TIME = TIMER_STEP_MS / 1000d;

    const int WINDOW_STATE_ADDRESS = 0; // coil
    const int ROOM_TEMPERATURE_ADDRESS = 0; // input register
    const int HEATER_VALVE_ADDRESS = 4; // input register
    const int THERMOSTAT_SETTING = 0; // holding register


    [OnTimer(TIMER_STEP_MS)]
    public void Update()
    {
        double roomTemp = BitConverter.ToDouble(server.GetInputRegistersBytes.Call(ROOM_TEMPERATURE_ADDRESS, 8), 0);
        double thermostatSetting = BitConverter.ToDouble(server.GetHoldingRegistersBytes.Call(THERMOSTAT_SETTING, 8), 0);
        bool windowOpen = server.GetCoils.Call(WINDOW_STATE_ADDRESS, 1)[0].ImplValue;

        double valveSetting = 0;

        if (!windowOpen)
        {
            // the valve adjusts itself according to the delta between the temperature its set to and the actual room temperature
            double delta = thermostatSetting - roomTemp;
            valveSetting = ActivationFunction(delta * DELTA_TIME);
        }

        server.SetInputRegistersBytes.Call(HEATER_VALVE_ADDRESS, BitConverter.GetBytes(valveSetting));
        ThermostatValve.Instance.SetValue(valveSetting);
    }

    private static double ActivationFunction(double delta)
    {
        // logarithmic sigmoid (-inf;inf) -> (0;1)
        double k = Math.Exp(-delta);
        return 1 / (k + 1);
    }
}