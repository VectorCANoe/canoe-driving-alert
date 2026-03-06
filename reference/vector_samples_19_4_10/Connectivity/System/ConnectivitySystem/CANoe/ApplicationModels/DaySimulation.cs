using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class DaySimulation : MeasurementScript
{
    public override void Start()
    {
        var currentTime = DateTime.Now;
        LightSimulation.GlobalTime.timeObject.currentTime.Value = currentTime.ToString("f");

        int timerInterval = 100; // in ms
        var SomeStructTimer = new Timer(this.increaseTime);
        SomeStructTimer.Interval = new TimeSpan(0, 0, 0, 0, timerInterval);
        SomeStructTimer.Start();
        //timer
    }

    void increaseTime(object sender, ElapsedEventArgs e)
    {
        if (LightSimulation.GlobalTime.timeObject.timeIsRunning.Value)
        {
            var tenMinutes = new TimeSpan(0, 10, 0);
            var currentTime = DateTime.Parse(LightSimulation.GlobalTime.timeObject.currentTime.Value);
            var nextTime = currentTime + tenMinutes;
            LightSimulation.GlobalTime.timeObject.currentTime.Value = nextTime.ToString("f");
            LightSimulation.GlobalTime.timeObject.hour.Value = nextTime.Hour <= 12 ? nextTime.Hour : nextTime.Hour - 12;
            LightSimulation.GlobalTime.timeObject.minute.Value = nextTime.Minute;
        }
    }

    [OnChange(LightSimulation.GlobalTime.timeObject.MemberIDs.toggle)]
    public void pauseDaySimulation()
    {
        if (LightSimulation.GlobalTime.timeObject.toggle.Value)
        {
            LightSimulation.GlobalTime.timeObject.timeIsRunning.Value = !LightSimulation.GlobalTime.timeObject.timeIsRunning.Value;
        }
    }

}