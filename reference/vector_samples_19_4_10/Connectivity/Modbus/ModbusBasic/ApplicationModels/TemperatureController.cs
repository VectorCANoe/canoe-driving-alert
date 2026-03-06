using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class TemperatureController : MeasurementScript
{
    private double PrevThermostatSetting;
    private double NewThermostatSetting;

    public override void Start()
    {
        thermostatSetting.Value_.Set.CallAsync(ThermostatSetting.Value);
        ThermostatSetting.OnChange += OnThermostatSettingChange;
    }

    private void OnThermostatSettingChange()
    {
        NewThermostatSetting = ThermostatSetting.Value;
    }

    [OnTimer(100)]
    public void Update()
    {
        if(NewThermostatSetting != PrevThermostatSetting)
        {
            PrevThermostatSetting = NewThermostatSetting;

            // send new data via Modbus high level client
            thermostatSetting.Instance.Value_.Set.CallAsync(NewThermostatSetting);
        }
    }
}