using System;
using Vector.CANoe.Runtime;

/// <summary>
/// Simulator component that adjusts heater temperature based on the thermostat valve and room temperature based on the heater temperature.
/// </summary>
public class EnvironmentSimulator : MeasurementScript
{
    /// <summary>
    /// Update simulation variables every X milliseconds.
    /// </summary>
    const int TIMER_STEP_MS = 200;
    const double DELTA_TIME = TIMER_STEP_MS / 1000d;

    /// <summary>
    /// The maximum factor of the delta that the simulation lerps per second for temperature adjustments.
    /// </summary>
    const double CHANGE_RATIO = 0.4f;
    const double HEATER_ROOM_AFFECTION = 0.25;
    const double HEATER_DELTA = 10;

    /// <summary>
    /// The outside temperature that influences the simulation if the window is opened
    /// </summary>
    const double TEMP_WINDOWS_OPEN = -5;

    // Address constants. See ModbusApplication.vCDL
    const int WINDOW_STATE_ADDRESS = 0;
    const int ROOM_TEMPERATURE_ADDRESS = 0;
    const int HEATER_VALVE_ADDRESS = 4;

    private double heaterTemperature = 0;

    [OnTimer(TIMER_STEP_MS)]
    public void Update()
    {
        double lerpAmount = DELTA_TIME * CHANGE_RATIO;

        // read window state from server (sent there by window manager)
        bool windowOpen = server.GetCoils.Call(WINDOW_STATE_ADDRESS, 1)[0].ImplValue;
        double roomTemp = BitConverter.ToDouble(server.GetInputRegistersBytes.Call(ROOM_TEMPERATURE_ADDRESS, 8), 0);
        double valveSetting = BitConverter.ToDouble(server.GetInputRegistersBytes.Call(HEATER_VALVE_ADDRESS, 8), 0);

        // adjust room temperature according to natural heat dissipation
        if (windowOpen)
        {
            roomTemp = Lerp(roomTemp, TEMP_WINDOWS_OPEN, lerpAmount);
            heaterTemperature = Lerp(heaterTemperature, TEMP_WINDOWS_OPEN, lerpAmount);
        }
        else
        {
            heaterTemperature += HEATER_DELTA * (valveSetting * 2 - 1) * DELTA_TIME;
            // the heater heats up or cools down depending on the state of the valve
            roomTemp = Lerp(roomTemp, heaterTemperature * HEATER_ROOM_AFFECTION, lerpAmount);
        }

        // write data into the server directly
        server.SetInputRegistersBytes.Call(ROOM_TEMPERATURE_ADDRESS, BitConverter.GetBytes(roomTemp));

        // update signals
        HeaterTemperature.Instance.SetValue(heaterTemperature);
        RoomTemperature.Instance.SetValue(roomTemp);
    }

    private static double Lerp(double val, double target, double amount)
    {
        amount = Math.Max(Math.Min(amount, 1), 0);
        return val + (target - val) * amount;
    }
}