using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Web;
using System.Net;
using System.Threading.Tasks;
using System.Text;
using static Local_Server;
using System.IO;
using System.Threading;

public class Local_Server : MeasurementScript
{

    [OnCall(NHTTPServer.httpServer.MemberIDs.OnRequest)]
    [WaitingHandler]
    public _HTTP.DataTypes.HTTPResponseMessage OnRequest(_HTTP.DataTypes.HTTPRequestMessage request)
    {
        _HTTP.DataTypes.HTTPResponseMessage response = _HTTP.DataTypes.HTTPResponseMessage.CreateInstance();
        switch (request.HTTPMethod.Value)
        {
            case "GET":
                return HandleGETMethod(request);
            default:
                return response;
        }
    }

    public _HTTP.DataTypes.HTTPResponseMessage HandleGETMethod(_HTTP.DataTypes.HTTPRequestMessage request)
    {
        _HTTP.DataTypes.HTTPResponseMessage response = _HTTP.DataTypes.HTTPResponseMessage.CreateInstance();

        var queryString = request.RequestUri;
        var parsedQuery = HttpUtility.ParseQueryString(queryString);

        string latitude = parsedQuery["lat"];
        string longitude = parsedQuery["lng"];
        string date = parsedQuery["date"];
        var sunData = GetSunData(latitude, longitude, date);
        var cco = Datatypes.Serializer.Serialize.CallAsyncAndWait(sunData, 5000);
        var serializedData = cco.Call.Result;

        response.StatusCode.Value = 200;
        response.StatusText.Value = "OK";
        SetResponseHeader(response);
        response.Body.Value = serializedData;

        return response;
    }

    public void SetResponseHeader(_HTTP.DataTypes.HTTPResponseMessage response)
    {
        using var header = _HTTP.DataTypes.Header.CreateInstance();
        response.Header.Value.Assign(header);
        response.Header.Value.Length = 1;
        using var headerField = _HTTP.DataTypes.HeaderField.CreateInstance();
        headerField.FieldName = "Content-Type";
        headerField.FieldValue = "application/json";
        response.Header.Value[0].Assign(headerField);
    }

    private Datatypes.SunriseResponseItem GetSunData(string lat, string lng, string date)
    {
        DateTime parsedDate;
        var resultData = Datatypes.SunriseResponseItem.CreateInstance();
        using var sunriseResultItem = Datatypes.SunriseResultItem.CreateInstance();
        resultData.results.Assign(sunriseResultItem);
        if (DateTime.TryParseExact(date, "MM/dd/yyyy", null, System.Globalization.DateTimeStyles.None, out parsedDate))
        {
            // Set the time to
            DateTime sunriseTime = new DateTime(parsedDate.Year, parsedDate.Month, parsedDate.Day, 8, 32, 0);
            DateTime sunsetTime = new DateTime(parsedDate.Year, parsedDate.Month, parsedDate.Day, 18, 43, 0);
            DateTime solarNoon = new DateTime(parsedDate.Year, parsedDate.Month, parsedDate.Day, 13, 37, 0);
            // Format the result in ISO 8601 format
            resultData.results.sunrise = sunriseTime.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:sszzz");
            resultData.results.sunset = sunsetTime.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:sszzz");
            resultData.results.solar_noon = solarNoon.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:sszzz");
        }

        return resultData;
    }

}
