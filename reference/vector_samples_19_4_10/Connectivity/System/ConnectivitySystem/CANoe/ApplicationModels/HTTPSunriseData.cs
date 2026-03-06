using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class HTTPSunriseData : MeasurementScript
{
    [OnUpdate(LightSimulation.GlobalTime.timeObject.MemberIDs.currentTime)]
    public void executeSunriseSunsetDataRequest()
    {
        var currentTime = DateTime.Parse(LightSimulation.GlobalTime.timeObject.currentTime.Value);
        var date = currentTime.ToString("d");

        DateTime dayReference;
        var success = DateTime.TryParse(LightSimulation.Control.mainControl.sunriseSunsetData.sunrise, out dayReference);

        if (!success || date != dayReference.ToString("d"))
        {
            double lat = 48.824;
            double lng = 9.097;

            LightSimulation.SunriseSunset.sunriseSunsetObtainer.getSunriseSunset.CallAsync(lat, lng, date, (responseItem) =>
            {
                LightSimulation.SunriseSunset.httptomqtt.sunriseSunsetData.sunrise = DateTime.Parse(responseItem.results.sunrise).ToString("f");
                LightSimulation.SunriseSunset.httptomqtt.sunriseSunsetData.sunset = DateTime.Parse(responseItem.results.sunset).ToString("f");
                LightSimulation.SunriseSunset.httptomqtt.sunriseSunsetData.solar_noon = DateTime.Parse(responseItem.results.solar_noon).ToString("f");
            });
        }
    }

}