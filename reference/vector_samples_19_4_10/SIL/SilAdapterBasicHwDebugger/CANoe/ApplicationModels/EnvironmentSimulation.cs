using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class EnvironmentSimulation : MeasurementScript
{
    /// <summary>
    /// Called before measurement start to perform necessary initializations,
    /// e.g. to create objects. During measurement, few additional objects
    /// should be created to prevent garbage collection runs in time-critical
    /// simulations.
    /// </summary>
    public override void Initialize()
    {
    }

    /// <summary>Notification that the measurement starts.</summary>
    public override void Start()
    {
        RoomTemperatureControl.Sensor1.Temperature.Value = 23;
        RoomTemperatureControl.Sensor2.Temperature.Value = 23;
        RoomTemperatureControl.Sensor3.Temperature.Value = 23;
    }

    /// <summary>Notification that the measurement ends.</summary>
    public override void Stop()
    {

    }

    /// <summary>
    /// Cleanup after the measurement. Complement to Initialize. This is not
    /// a "Dispose" method; your object should still be usable afterwards.
    /// </summary>
    public override void Shutdown()
    {

    }

    [OnUpdate(RoomTemperatureControl.Sensor1.MemberIDs.Temperature)]
    public void OnTemperatureChange_Sensor1()
    {
        RoomTemperatureControl.Sensor1.SetTemperature.CallAsync(RoomTemperatureControl.Sensor1.Temperature.Value);
    }

    [OnUpdate(RoomTemperatureControl.Sensor2.MemberIDs.Temperature)]
    public void OnTemperatureChange_Sensor2()
    {
        RoomTemperatureControl.Sensor2.SetTemperature.CallAsync(RoomTemperatureControl.Sensor2.Temperature.Value);
    }

    [OnUpdate(RoomTemperatureControl.Sensor3.MemberIDs.Temperature)]
    public void OnTemperatureChange_Sensor3()
    {
        RoomTemperatureControl.Sensor3.SetTemperature.CallAsync(RoomTemperatureControl.Sensor3.Temperature.Value);
    }

    [OnUpdate(Configuration.Application.MemberIDs.ShowHeaterStateOnLED)]
    public void OnShowHeaterStateOnLED()
    {
        Configuration.Application.SetShowHeaterStateOnLED.CallAsync(Configuration.Application.ShowHeaterStateOnLED.Value);
    }

    [OnCall(RoomTemperatureControl.Heater.MemberIDs.SetHeaterState)]
    public void OnSetHeaterState(byte state)
    {
        RoomTemperatureControl.Heater.HeaterState.Value = state;
    }
}