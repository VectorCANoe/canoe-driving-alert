using Vector.CANoe.Threading;
using Vector.CANoe.TFS;
using HwDebuggerBinding;

[TestClass]
public class RoomTemperatureControlTests
{
    private static readonly int MaxConnectTimeInMs = 20000; // Initial Connect
    private static readonly int MaxReactionTimeInMs = 3000;

    [Export]
    [TestFunction]
    public static void WaitForOnline()
    {
        if (Execution.Wait(Configuration.Debugger.State, DebuggerState.Online, MaxConnectTimeInMs) == Execution.WAIT_TIMEOUT)
        {
            Report.TestStepFail("Timeout. Expected connection to SIL Adapter to be in state 'Online'.");
        }
    }

    [Export]
    [TestCase]
    public static void TestTemperatureControl(int temperatureSensor1, int temperatureSensor2, int temperatureSensor3, int expectedHeaterState)
    {
        // Check if CANoe is still connected to SIL Adapter
        if (Configuration.Debugger.State.SymbValue != DebuggerState.Online)
        {
            Report.TestStepFail("Expected connection to SIL Adapter to be in state 'Online'.");
        }

        // Do reset of sensor values because each test should contain a change of the heater state. Otherwise there could
        // be timing problems with this test design, caused by the delay between setting the values and receiving the new heater state.
        // If the default would result in the same as the expected heater state of the test, reset to non-default values.
        // Alternative: Wait a fix time between setting the temperature values and checking the new heater state.
        var expectedInitialHeaterState = (RoomTemperatureControl.State)expectedHeaterState == RoomTemperatureControl.State.OFF
                                       ? RoomTemperatureControl.State.HEATING
                                       : RoomTemperatureControl.State.OFF;
        var initialSensorValue = (RoomTemperatureControl.State)expectedHeaterState == RoomTemperatureControl.State.OFF ? 15 : 22;

        RoomTemperatureControl.Sensor1.Temperature.Value = initialSensorValue;
        RoomTemperatureControl.Sensor2.Temperature.Value = initialSensorValue;
        RoomTemperatureControl.Sensor3.Temperature.Value = initialSensorValue;

        if (Execution.Wait(RoomTemperatureControl.Heater.HeaterState, expectedInitialHeaterState, MaxReactionTimeInMs) == Execution.WAIT_TIMEOUT)
        {
            var heaterState = (RoomTemperatureControl.State)RoomTemperatureControl.Heater.HeaterState.Value;
            Report.TestStepFail($"Timeout. Expected Heater State to be initially '{expectedInitialHeaterState}' but was '{heaterState}'");
        }

        // Set temperature values which shall be tested
        RoomTemperatureControl.Sensor1.Temperature.Value = temperatureSensor1;
        RoomTemperatureControl.Sensor2.Temperature.Value = temperatureSensor2;
        RoomTemperatureControl.Sensor3.Temperature.Value = temperatureSensor3;

        if (Execution.Wait(RoomTemperatureControl.Heater.HeaterState, expectedHeaterState, MaxReactionTimeInMs) == Execution.WAIT_TIMEOUT)
        {
            var heaterState = (RoomTemperatureControl.State)RoomTemperatureControl.Heater.HeaterState.Value;
            Report.TestStepFail($"Timeout. Expected Heater State to be '{expectedHeaterState}' but was '{heaterState}'");
        }
        else
        {
            Report.TestStepPass("Success");
        }
    }
}