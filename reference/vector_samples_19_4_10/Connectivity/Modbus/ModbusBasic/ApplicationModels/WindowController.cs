using Vector.Tools;
using Vector.CANoe.Runtime;
using ModbusBinding.DataTypes;

/// <summary>
/// Manages the low level client which is used to communicate the window state to the modbus server of the thermostat.
/// </summary>
public class WindowController : MeasurementScript
{
    public override void Start()
    {
        base.Start();
        ConnectParams connectParams = new ConnectParams();
        connectParams.TargetIP = "127.0.0.31";
        connectParams.TargetPort.ImplValue = 502;
        using (var cct = ModbusDemo.client.ConnectMaster.CallAsync(connectParams)) { }
        WindowState.OnChange += OnWindowStateUpdate;
    }

    public void OnWindowStateUpdate()
    {
        uint windowState = WindowState.Value;
        if(windowState == 0)
        {
            OnClose();
        }
        else if(windowState == 1)
        {
            OnOpen();
        }
    }

    public void OnClose()
    {
        using (var cct = ModbusDemo.client.Instance.WriteCoil.CallAsync(0, false, 0)) { }
        Output.WriteLine("window closed");
    }

    public void OnOpen()
    {
        using (var cct = ModbusDemo.client.Instance.WriteCoil.CallAsync(0, true, 0)) { }
        Output.WriteLine("window opened");
    }
}