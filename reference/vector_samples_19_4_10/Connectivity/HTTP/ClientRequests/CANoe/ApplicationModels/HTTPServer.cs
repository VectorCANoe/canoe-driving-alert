using System;
using System.Text;
using System.IO;
using System.Net;
using System.Collections.Generic;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;


public class HTTPServerModel : MeasurementScript
{
    private static readonly Dictionary<int, string> storage = new Dictionary<int, string> { };

    [WaitingHandler]
    [OnCall(HTTPServer.httpServer.MemberIDs.OnRequest)]
    public _HTTP.DataTypes.HTTPResponseMessage OnRequest(_HTTP.DataTypes.HTTPRequestMessage request)
    {
        _HTTP.DataTypes.HTTPResponseMessage response = _HTTP.DataTypes.HTTPResponseMessage.CreateInstance();
        switch (request.HTTPMethod.Value)
        {
            case "POST":
                return HandlePOSTMethod(request);
            case "GET":
                return HandleGETMethod(request);
            case "DELETE":
                return HandleDELETEMethod(request);
            default:
                return response;
        }
    }

    public _HTTP.DataTypes.HTTPResponseMessage HandleGETMethod(_HTTP.DataTypes.HTTPRequestMessage request)
    {
        _HTTP.DataTypes.HTTPResponseMessage response = _HTTP.DataTypes.HTTPResponseMessage.CreateInstance();
        // Remove the leading / 
        int lastSlashIndex = request.RequestUri.Value.LastIndexOf('/');
        string userId = request.RequestUri.Value.Substring(lastSlashIndex + 1);

        if (storage.TryGetValue(int.Parse(userId), out string payload))
        {
            response.StatusCode.Value = 200;
            response.StatusText.Value = "OK";
            SetResponseHeader(response);
            response.Body.Value = Encoding.UTF8.GetBytes(payload);
        }
        else
        {
            response.StatusCode.Value = 404;
            response.StatusText.Value = $"No user for id {userId} found";
        }
        return response;
    }

    public _HTTP.DataTypes.HTTPResponseMessage HandlePOSTMethod(_HTTP.DataTypes.HTTPRequestMessage request)
    {
        _HTTP.DataTypes.HTTPResponseMessage response = _HTTP.DataTypes.HTTPResponseMessage.CreateInstance();
        var cco =
            Application.Datatypes.Local.Serializer.Deserialize_UserInformation.CallAsyncAndWait(request.Body.Value,
                2000);
        var deserializedBody = cco.Call.Result;
        

        if (storage.ContainsKey(deserializedBody.user_id.Value))
        {
            storage[deserializedBody.user_id.Value] = System.Text.Encoding.ASCII.GetString(request.Body.Value);
        }
        else
        {
            storage.Add(deserializedBody.user_id.Value, System.Text.Encoding.ASCII.GetString(request.Body.Value));
        }
        

        response.StatusCode.Value = 200;
        response.StatusText.Value = "OK";
        SetResponseHeader(response);
        response.Body.Value = request.Body.Value;
        return response;
    }

    public _HTTP.DataTypes.HTTPResponseMessage HandleDELETEMethod(_HTTP.DataTypes.HTTPRequestMessage request)
    {
        _HTTP.DataTypes.HTTPResponseMessage response = _HTTP.DataTypes.HTTPResponseMessage.CreateInstance();
        // Remove the leading / 
        int lastSlashIndex = request.RequestUri.Value.LastIndexOf('/');
        string userId = request.RequestUri.Value.Substring(lastSlashIndex + 1);

        if (storage.TryGetValue(int.Parse(userId), out string payload))
        {
            storage.Remove(int.Parse(userId));
            response.StatusCode.Value = 204;
            response.StatusText.Value = "No Content";
            SetResponseHeader(response);
        }
        else
        {
            response.StatusCode.Value = 404;
            response.StatusText.Value = $"No user for id {userId} found";
        }
        return response;
    }

    public void SetResponseHeader(_HTTP.DataTypes.HTTPResponseMessage response)
    {
        using var header = _HTTP.DataTypes.Header.CreateInstance();
        response.Header.Assign(header);
        response.Header.Value.Length = 1;
        using var headerField = _HTTP.DataTypes.HeaderField.CreateInstance();
        headerField.FieldName = "Content-Type";
        headerField.FieldValue = "application/json";
        response.Header.Value[0].Assign(headerField);
    }

}
