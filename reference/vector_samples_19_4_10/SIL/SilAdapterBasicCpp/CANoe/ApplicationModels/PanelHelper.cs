using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;
using RoomTemperatureControl;
using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class PanelHelper : MeasurementScript
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

    [OnChange(RoomTemperatureControl.Sensor1.MemberIDs.Temperature)]
    [OnChange(RoomTemperatureControl.Sensor2.MemberIDs.Temperature)]
    [OnChange(RoomTemperatureControl.Sensor3.MemberIDs.Temperature)]
    public void OnTemperatureChange()
    {
        SetPanelAverageTemperature();
    }

    public void SetPanelAverageTemperature()
    {
        ExploratoryTesting.Panel.AverageTemperature.Value = (RoomTemperatureControl.Sensor1.Temperature.Value +
                                                RoomTemperatureControl.Sensor2.Temperature.Value +
                                                RoomTemperatureControl.Sensor3.Temperature.Value) / 3.0;
    }
}