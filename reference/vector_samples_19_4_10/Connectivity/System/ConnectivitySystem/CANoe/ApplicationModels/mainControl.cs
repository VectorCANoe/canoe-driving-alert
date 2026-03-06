using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class mainControl : MeasurementScript
{
    public override void Start()
    {
        LightSimulation.Control.mainControl.roomData.lights = false;
        LightSimulation.Control.mainControl.roomData.shades_east = false;
        LightSimulation.Control.mainControl.roomData.shades_west = false;
        LightSimulation.Control.manualControl.buttonLight.ImplValue = (uint)LightSimulation.Control.buttonStateLight.AUTO;
        LightSimulation.Control.manualControl.buttonShades_east.ImplValue = (uint)LightSimulation.Control.buttonStateShades.AUTO;
        LightSimulation.Control.manualControl.buttonShades_west.ImplValue = (uint)LightSimulation.Control.buttonStateShades.AUTO;
    }

    [OnUpdate(LightSimulation.GlobalTime.timeObject.MemberIDs.currentTime)]
    public void determineRoomData()
    {
        DateTime sunrise;
        DateTime sunset;
        DateTime solar_noon;

        if (DateTime.TryParse(LightSimulation.Control.mainControl.sunriseSunsetData.sunrise, out sunrise)
          && DateTime.TryParse(LightSimulation.Control.mainControl.sunriseSunsetData.sunset, out sunset)
          && DateTime.TryParse(LightSimulation.Control.mainControl.sunriseSunsetData.solar_noon, out solar_noon))
        {
            var currentTime = DateTime.Parse(LightSimulation.GlobalTime.timeObject.currentTime.Value);

            if (currentTime.ToString("d") == sunrise.ToString("d"))
            {
                if (LightSimulation.Control.mainControl.lightAutomatic.Value)
                {
                    LightSimulation.Control.mainControl.roomData.lights = isLightRequired(sunrise, sunset, currentTime);
                }
                if (LightSimulation.Control.mainControl.shades_eastAutomatic.Value)
                {
                    LightSimulation.Control.mainControl.roomData.shades_east = areShadesEastRequired(sunrise, solar_noon, currentTime);
                }
                if (LightSimulation.Control.mainControl.shades_westAutomatic.Value)
                {
                    LightSimulation.Control.mainControl.roomData.shades_west = areShadesWestRequired(solar_noon, sunset, currentTime);
                }
            }
        }
    }

    bool isLightRequired(DateTime sunrise, DateTime sunset, DateTime currentTime)
    {
        var wakeUpTime = DateTime.Parse(currentTime.ToString("d") + " 06:00");
        var bedTime = DateTime.Parse(currentTime.ToString("d") + " 22:00");

        bool itIsMorning = isTimeBetweenTimes(currentTime, wakeUpTime, sunrise);
        bool itIsEvening = isTimeBetweenTimes(currentTime, sunset, bedTime);

        return itIsMorning || itIsEvening;
    }

    bool areShadesEastRequired(DateTime sunrise, DateTime solar_noon, DateTime currentTime)
    {
        return isTimeBetweenTimes(currentTime, sunrise, solar_noon);
    }

    bool areShadesWestRequired(DateTime solar_noon, DateTime sunset, DateTime currentTime)
    {
        return isTimeBetweenTimes(currentTime, solar_noon, sunset);
    }

    bool isTimeBetweenTimes(DateTime currentTime, DateTime timeA, DateTime timeB)
    {
        return (DateTime.Compare(timeA, currentTime) == -1) && (DateTime.Compare(currentTime, timeB) == -1);
    }


    [OnUpdate(LightSimulation.Control.mainControl.MemberIDs.buttonLight)]
    public void OnLightButtonClicked()
    {
        if (LightSimulation.Control.mainControl.buttonLight.ImplValue == (uint)LightSimulation.Control.buttonStateLight.ON)
        {
            LightSimulation.Control.mainControl.roomData.lights = true;
            LightSimulation.Control.mainControl.lightAutomatic.Value = false;
        }
        else if (LightSimulation.Control.mainControl.buttonLight.ImplValue == (uint)LightSimulation.Control.buttonStateLight.OFF)
        {
            LightSimulation.Control.mainControl.roomData.lights = false;
            LightSimulation.Control.mainControl.lightAutomatic.Value = false;
        }
        else if (LightSimulation.Control.mainControl.buttonLight.ImplValue == (uint)LightSimulation.Control.buttonStateLight.AUTO)
        {
            LightSimulation.Control.mainControl.lightAutomatic.Value = true;
        }
    }

    [OnUpdate(LightSimulation.Control.mainControl.MemberIDs.buttonShades_east)]
    public void OnShades_eastButtonClicked()
    {
        if (LightSimulation.Control.mainControl.buttonShades_east.ImplValue == (uint)LightSimulation.Control.buttonStateShades.CLOSE)
        {
            LightSimulation.Control.mainControl.roomData.shades_east = true;
            LightSimulation.Control.mainControl.shades_eastAutomatic.Value = false;
        }
        else if (LightSimulation.Control.mainControl.buttonShades_east.ImplValue == (uint)LightSimulation.Control.buttonStateShades.OPEN)
        {
            LightSimulation.Control.mainControl.roomData.shades_east = false;
            LightSimulation.Control.mainControl.shades_eastAutomatic.Value = false;
        }
        else if (LightSimulation.Control.mainControl.buttonShades_east.ImplValue == (uint)LightSimulation.Control.buttonStateShades.AUTO)
        {
            LightSimulation.Control.mainControl.shades_eastAutomatic.Value = true;
        }
    }

    [OnUpdate(LightSimulation.Control.mainControl.MemberIDs.buttonShades_west)]
    public void OnShades_westButtonClicked()
    {
        if (LightSimulation.Control.mainControl.buttonShades_west.ImplValue == (uint)LightSimulation.Control.buttonStateShades.CLOSE)
        {
            LightSimulation.Control.mainControl.roomData.shades_west = true;
            LightSimulation.Control.mainControl.shades_westAutomatic.Value = false;
        }
        else if (LightSimulation.Control.mainControl.buttonShades_west.ImplValue == (uint)LightSimulation.Control.buttonStateShades.OPEN)
        {
            LightSimulation.Control.mainControl.roomData.shades_west = false;
            LightSimulation.Control.mainControl.shades_westAutomatic.Value = false;
        }
        else if (LightSimulation.Control.mainControl.buttonShades_west.ImplValue == (uint)LightSimulation.Control.buttonStateShades.AUTO)
        {
            LightSimulation.Control.mainControl.shades_westAutomatic.Value = true;
        }
    }
}