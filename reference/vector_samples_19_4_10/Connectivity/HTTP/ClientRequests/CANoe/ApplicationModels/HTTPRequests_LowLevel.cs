using System;
using System.Text;
using System.IO;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using Vector.CANoe.Runtime;
using Vector.Tools;

public class HttpRequestsLowLevel : MeasurementScript
{
    private string mLocalServer = "http://localhost:8123";

    #region Local Add User
    [OnChange(Application.Panels.Local.ClientControlAddUser.MemberIDs.execute)]
    public void ExecuteLocalAddUser()
    {
        if (Application.Panels.Local.ClientControlAddUser.execute.Value == 1
            && Application.Panels.Local.ClientControlAddUser.mode.SymbValue == Application.Panels.HTTPBindingMode.USE_LOW_LEVEL)
        {
            using var response = Application.Datatypes.Local.UserInformation.CreateInstance();
            Application.Panels.Local.ClientControlAddUser.response.Assign(response);
            using var requestData = Application.Datatypes.Local.UserInformation.CreateInstance();
            requestData.user_id.Value = Application.Panels.Local.ClientControlAddUser.user_id.Value;
            requestData.name = Application.Panels.Local.ClientControlAddUser.name.Value;

            Application.Datatypes.Local.Serializer.Serialize_UserInformation.CallAsync(requestData, serializedData => SendAddUserRequest(serializedData));
        }
    }

    public void SendAddUserRequest(byte[] payload)
    {
        using var requestMessage = _HTTP.DataTypes.HTTPRequestMessage.CreateInstance();
        requestMessage.HTTPMethod = "POST";
        requestMessage.RequestUri = mLocalServer;
        using var header = _HTTP.DataTypes.Header.CreateInstance();
        requestMessage.Header.Value.Assign(header);
        requestMessage.Header.Value.Length = 1;
        using var headerField = _HTTP.DataTypes.HeaderField.CreateInstance();
        headerField.FieldName = "accept";
        headerField.FieldValue = "application/json";
        requestMessage.Header.Value[0].Assign(headerField);
        requestMessage.Body.Value = payload;
        _HTTP.Client.HTTP_SendRequest.CallAsync(requestMessage, (httpResponse) =>
        {
            if (httpResponse.StatusCode.Value == 200)
            {
                Application.Datatypes.Local.Serializer.Deserialize_UserInformation.CallAsync(httpResponse.Body.Value, receivedData => UpdateAddUserResponse(receivedData));
            }
            else
            {
                Output.WriteLine(String.Format("Received Http Status {0} {1}", httpResponse.StatusCode.Value, httpResponse.StatusText));
            }
        });
    }

    public void UpdateAddUserResponse(Application.Datatypes.Local.UserInformation receivedData)
    {
        Application.Panels.Local.ClientControlAddUser.response.user_id = receivedData.user_id.Value;
        Application.Panels.Local.ClientControlAddUser.response.name = receivedData.name;
    }

    #endregion

    #region Local Get User
    [OnChange(Application.Panels.Local.ClientControlGetUser.MemberIDs.execute)]
    public void ExecuteLocalGetUser()
    {
        if (Application.Panels.Local.ClientControlGetUser.execute.Value == 1
            && Application.Panels.Local.ClientControlGetUser.mode.SymbValue == Application.Panels.HTTPBindingMode.USE_LOW_LEVEL)
        {
            using var response = Application.Datatypes.Local.UserInformation.CreateInstance();
            Application.Panels.Local.ClientControlGetUser.response.Assign(response);
            var user_id = Application.Panels.Local.ClientControlGetUser.user_id.Value;

            using var requestMessage = _HTTP.DataTypes.HTTPRequestMessage.CreateInstance();
            requestMessage.HTTPMethod = "GET";
            requestMessage.RequestUri = mLocalServer + "/" + user_id.ToString();
            using var header = _HTTP.DataTypes.Header.CreateInstance();
            requestMessage.Header.Value.Assign(header);
            requestMessage.Header.Value.Length = 1;
            using var headerField = _HTTP.DataTypes.HeaderField.CreateInstance();
            headerField.FieldName = "accept";
            headerField.FieldValue = "application/json";
            requestMessage.Header.Value[0].Assign(headerField);

            _HTTP.Client.HTTP_SendRequest.CallAsync(requestMessage, (httpResponse) =>
            {
                if (httpResponse.StatusCode.Value == 200)
                {
                    Application.Datatypes.Local.Serializer.Deserialize_UserInformation.CallAsync(httpResponse.Body.Value, receivedData => UpdateGetUserResponse(receivedData));
                }
                else
                {
                    Output.WriteLine(String.Format("Received Http Status {0} {1}", httpResponse.StatusCode.Value, httpResponse.StatusText));
                }
            });

        }
    }


    public void UpdateGetUserResponse(Application.Datatypes.Local.UserInformation receivedData)
    {
        Application.Panels.Local.ClientControlGetUser.response.user_id = receivedData.user_id.Value;
        Application.Panels.Local.ClientControlGetUser.response.name = receivedData.name;
    }

    #endregion


    #region Local Delete User
    [OnChange(Application.Panels.Local.ClientControlDeleteUser.MemberIDs.execute)]
    public void ExecuteLocalDeleteUser()
    {
        if (Application.Panels.Local.ClientControlDeleteUser.execute.Value == 1
            && Application.Panels.Local.ClientControlDeleteUser.mode.SymbValue == Application.Panels.HTTPBindingMode.USE_LOW_LEVEL)
        {
            var user_id = Application.Panels.Local.ClientControlDeleteUser.user_id.Value;

            using var requestMessage = _HTTP.DataTypes.HTTPRequestMessage.CreateInstance();
            requestMessage.HTTPMethod = "DELETE";
            requestMessage.RequestUri = mLocalServer + "/" + user_id.ToString();
            using var header = _HTTP.DataTypes.Header.CreateInstance();
            requestMessage.Header.Value.Assign(header);
            requestMessage.Header.Value.Length = 1;
            using var headerField = _HTTP.DataTypes.HeaderField.CreateInstance();
            headerField.FieldName = "accept";
            headerField.FieldValue = "application/json";
            requestMessage.Header.Value[0].Assign(headerField);

            _HTTP.Client.HTTP_SendRequest.CallAsync(requestMessage, (httpResponse) =>
            {
                if (httpResponse.StatusCode.Value >= 300)
                {
                    Output.WriteLine(String.Format("Received Http Status {0} {1}", httpResponse.StatusCode.Value, httpResponse.StatusText));
                }
            });

        }
    }

    #endregion

}
