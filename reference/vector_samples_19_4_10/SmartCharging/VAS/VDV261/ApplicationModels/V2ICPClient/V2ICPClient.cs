using System;
using System.Net;
using System.Text;
using V2ICP.DataTypes.V1;
using Vector.CANoe.Runtime;
using Vector.Tools;



public class V2ICPClient : MeasurementScript
{
  private V2ICP.DataTypes.V1.V2ICPResponseContent DeserializeV2ICPResponseV1(byte[] responseBytes)
  {
    var responseStruct = V2ICP.DataTypes.V1.V2ICPSerializer.Deserialize_V2ICPResponseContent.CallAsyncAndWait(responseBytes, 1000).Call.Result;
    return responseStruct;
  }

  private byte[] SerializeV2ICPRequestV1(V2ICP.DataTypes.V1.V2ICPRequestContent requestStruct)
  {
    var requestBytes = V2ICP.DataTypes.V1.V2ICPSerializer.Serialize_V2ICPRequestContent.CallAsyncAndWait(requestStruct, 1000).Call.Result;
    return requestBytes;
  }

  private V2ICP.DataTypes.V2.V2ICPResponseContent DeserializeV2ICPResponseV2(byte[] responseBytes)
  {
    var responseStruct = V2ICP.DataTypes.V2.V2ICPSerializer.Deserialize_V2ICPResponseContent.CallAsyncAndWait(responseBytes, 1000).Call.Result;
    return responseStruct;
  }

  private byte[] SerializeV2ICPRequestV2(V2ICP.DataTypes.V2.V2ICPRequestContent requestStruct)
  {
    var requestBytes = V2ICP.DataTypes.V2.V2ICPSerializer.Serialize_V2ICPRequestContent.CallAsyncAndWait(requestStruct, 1000).Call.Result;
    return requestBytes;
  }

  private void _AddHeader(_HTTP.DataTypes.HTTPRequestMessage msg, string headerName, string headerValue)
  {
    var headerField = _HTTP.DataTypes.HeaderField.CreateInstance();
    headerField.FieldName = headerName;
    headerField.FieldValue = headerValue;

    msg.Header.Value.Length++;
    
    msg.Header.Value[msg.Header.Value.Length - 1].Assign(headerField);

  }

  private string _GetBasicAuthorizationString(string username, string password)
  {
    string plainAuthHeaderValue = username + ":" + password;
    byte[] asciiBytesAuthHeader = Encoding.ASCII.GetBytes(plainAuthHeaderValue);
    string base64AuthHeaderValue = Convert.ToBase64String(asciiBytesAuthHeader);

    return "Basic" + " " + base64AuthHeaderValue;
  }

  // The WaitingHandler Attribute is important, otherwise Execution.Wait or CallAsyncAndWait will not work
  // The method marked in this way must be a non-static public method and must in addition be marked with
  // at least one of the OnChange or OnUpdate attributes for value entities
  // or one of the function call attributes OnCalling, OnCall, OnReturning or OnCalled.
  [Vector.CANoe.Runtime.WaitingHandler]
  [OnCall(V2ICP.Endpoints.V2ICPClient.MemberIDs.V2ICPMethodV1)]
  public V2ICP.DataTypes.V1.V2ICPResponse V2ICPMethodV1(V2ICP.DataTypes.V1.V2ICPRequestContent requestData)
  {
    V2ICP.DataTypes.V1.V2ICPResponse response = V2ICP.DataTypes.V1.V2ICPResponse.CreateInstance();

    try
    {
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV1, HTTPBinding.Path.AttributeDefinitionPath, out string pathAttributeValue, replaced: true);
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV1, HTTPBinding.Host.AttributeDefinitionPath, out string hostAttributeValue, replaced: true);
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV1, HTTPBinding.IPConfig.Node.AttributeDefinitionPath, out string nodeAttributeValue, replaced: true);
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV1, HTTPBinding.IPConfig.Network.AttributeDefinitionPath, out string networkAttributeValue, replaced: true);
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV1, HTTPBinding.IPConfig.TLSConfiguration.AttributeDefinitionPath, out string tlsConfigAttributeValue, replaced: true);

       

      #region Serialize Request Struct
      var requestBytes = SerializeV2ICPRequestV1(requestData);
      #endregion

      #region Prepare Generic Request     
      var requestMessage = _HTTP.DataTypes.HTTPRequestMessage.CreateInstance();
      requestMessage.HTTPMethod = "POST";
      requestMessage.RequestUri = $"{hostAttributeValue}/{pathAttributeValue}";

      requestMessage.IPConfig.Value.Network         = networkAttributeValue;
      requestMessage.IPConfig.Value.Node            = nodeAttributeValue;
      requestMessage.IPConfig.Value.TLSConfig.Value = tlsConfigAttributeValue;

      var basicAuthHeaderValue = _GetBasicAuthorizationString(V2ICP.Endpoints.V2ICPClient.BasicAuthUsername.Value, 
                                                              V2ICP.Endpoints.V2ICPClient.BasicAuthPassword.Value);

      // Init Headers
      requestMessage.Header.Assign(_HTTP.DataTypes.Header.CreateInstance());

      _AddHeader(requestMessage, "User-Agent"   , V2ICP.DataTypes.V1.HTTPUserAgent.Value);
      _AddHeader(requestMessage, "accept"       , V2ICP.DataTypes.HTTPAccept.Value);
      _AddHeader(requestMessage, "Content-Type" , V2ICP.DataTypes.HTTPContentType.Value);
      _AddHeader(requestMessage, "Authorization", basicAuthHeaderValue);

      requestMessage.Body.Assign(requestBytes);
      #endregion

      #region Execute HTTP Request 
      // HTTP_SendRequest
      var httpResponseWaitHandle = _HTTP.Client.HTTP_SendRequest.CallAsyncAndWait(requestMessage, 
                                                                                  (int)V2ICP.Endpoints.V2ICPClient.ResponseTimeout.Value);
      var call = httpResponseWaitHandle.Call;
      if(call == null)
      {
        response.StatusCode = ulong.MaxValue;
        response.StatusText = "Failed to process Request";
        response.Content.HasValue = false;
        V2ICP.Endpoints.V2ICPClient.OnRequestFailure.Trigger();
      }
      else
      {
        var httpResponse = call.Result;
        if(httpResponse == null)
        {
          response.StatusCode = ulong.MaxValue;
          response.StatusText = "Response Timeout";
          response.Content.HasValue = false;
          V2ICP.Endpoints.V2ICPClient.OnResponseTimeout.Trigger();
        }
        else
        {
          response.StatusCode = (ulong) httpResponse.StatusCode.Value;
          response.StatusText = httpResponse.StatusText.Value;

          if ((HttpStatusCode)httpResponse.StatusCode.Value == HttpStatusCode.OK)
          {
            if(!httpResponse.Body.HasValue || httpResponse.Body.Value.Value.Length == 0 )
            {
              response.StatusCode = ulong.MaxValue;
              response.StatusText = "Original Status Code OK, but no data in body!";
              response.Content.HasValue = false;
            }
            else
            {
              var responseContent = DeserializeV2ICPResponseV1(httpResponse.Body.Value);
              if(responseContent == null)
              {
                response.StatusCode = ulong.MaxValue;
                response.StatusText = "Original Status Code OK with data in body, but deserialization failed!";
                response.Content.HasValue = false;
              }
              else
              {
                // Good case, keep Status & Text
                response.Content.Assign(responseContent);
              }
            }
          }
          else
          {
            // Other Status Code received
            response.Content.HasValue = false;
          }
        }
      }

      #endregion
    }
    catch (Exception ex)
    {
      response.StatusCode = ulong.MaxValue;
      response.StatusText = "Exception: " + ex.Message;
      response.Content.HasValue = false;
    }

    // Do not return NULL to CANoe, otherwise the Runtime Kernel will say good bye 
    
    return response;
  }




  [Vector.CANoe.Runtime.WaitingHandler]
  [OnCall(V2ICP.Endpoints.V2ICPClient.MemberIDs.V2ICPMethodV2)]
  public V2ICP.DataTypes.V2.V2ICPResponse V2ICPMethodV2(V2ICP.DataTypes.V2.V2ICPRequestContent requestData)
  {
    V2ICP.DataTypes.V2.V2ICPResponse response = V2ICP.DataTypes.V2.V2ICPResponse.CreateInstance();

    try
    {
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV2, HTTPBinding.Path.AttributeDefinitionPath, out string pathAttributeValue, replaced: true);
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV2, HTTPBinding.Host.AttributeDefinitionPath, out string hostAttributeValue, replaced: true);
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV2, HTTPBinding.IPConfig.Node.AttributeDefinitionPath, out string nodeAttributeValue, replaced: true);
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV2, HTTPBinding.IPConfig.Network.AttributeDefinitionPath, out string networkAttributeValue, replaced: true);
      AttributeAccess.GetAttributeValue(V2ICP.Endpoints.V2ICPClient.V2ICPMethodV2, HTTPBinding.IPConfig.TLSConfiguration.AttributeDefinitionPath, out string tlsConfigAttributeValue, replaced: true);

       

      #region Serialize Request Struct
      var requestBytes = SerializeV2ICPRequestV2(requestData);
      #endregion

      #region Prepare Generic Request     
      var requestMessage = _HTTP.DataTypes.HTTPRequestMessage.CreateInstance();
      requestMessage.HTTPMethod = "POST";
      requestMessage.RequestUri = $"{hostAttributeValue}/{pathAttributeValue}";

      requestMessage.IPConfig.Value.Network         = networkAttributeValue;
      requestMessage.IPConfig.Value.Node            = nodeAttributeValue;
      requestMessage.IPConfig.Value.TLSConfig.Value = tlsConfigAttributeValue;

      var basicAuthHeaderValue = _GetBasicAuthorizationString(V2ICP.Endpoints.V2ICPClient.BasicAuthUsername.Value, 
                                                              V2ICP.Endpoints.V2ICPClient.BasicAuthPassword.Value);

      // Init Headers
      requestMessage.Header.Assign(_HTTP.DataTypes.Header.CreateInstance());

      _AddHeader(requestMessage, "User-Agent"   , V2ICP.DataTypes.V2.HTTPUserAgent.Value);
      _AddHeader(requestMessage, "accept"       , V2ICP.DataTypes.HTTPAccept.Value);
      _AddHeader(requestMessage, "Content-Type" , V2ICP.DataTypes.HTTPContentType.Value);
      _AddHeader(requestMessage, "Authorization", basicAuthHeaderValue);

      requestMessage.Body.Assign(requestBytes);
      #endregion

      #region Execute HTTP Request 
      // HTTP_SendRequest
      var httpResponseWaitHandle = _HTTP.Client.HTTP_SendRequest.CallAsyncAndWait(requestMessage, 
                                                                                  (int)V2ICP.Endpoints.V2ICPClient.ResponseTimeout.Value);
      var call = httpResponseWaitHandle.Call;
      if(call == null)
      {
        response.StatusCode = ulong.MaxValue;
        response.StatusText = "Failed to process Request";
        response.Content.HasValue = false;
        V2ICP.Endpoints.V2ICPClient.OnRequestFailure.Trigger();
      }
      else
      {
        var httpResponse = call.Result;
        if(httpResponse == null)
        {
          response.StatusCode = ulong.MaxValue;
          response.StatusText = "Response Timeout";
          response.Content.HasValue = false;
          V2ICP.Endpoints.V2ICPClient.OnResponseTimeout.Trigger();
        }
        else
        {
          response.StatusCode = (ulong) httpResponse.StatusCode.Value;
          response.StatusText = httpResponse.StatusText.Value;

          if ((HttpStatusCode)httpResponse.StatusCode.Value == HttpStatusCode.OK)
          {
            if(!httpResponse.Body.HasValue || httpResponse.Body.Value.Value.Length == 0 )
            {
              response.StatusCode = ulong.MaxValue;
              response.StatusText = "Original Status Code OK, but no data in body!";
              response.Content.HasValue = false;
            }
            else
            {
              var responseContent = DeserializeV2ICPResponseV2(httpResponse.Body.Value);
              if(responseContent == null)
              {
                response.StatusCode = ulong.MaxValue;
                response.StatusText = "Original Status Code OK with data in body, but deserialization failed!";
                response.Content.HasValue = false;
              }
              else
              {
                // Good case, keep Status & Text
                response.Content.Assign(responseContent);
              }
            }
          }
          else
          {
            // Other Status Code received
            response.Content.HasValue = false;
          }
        }
      }

      #endregion
    }
    catch (Exception ex)
    {
      response.StatusCode = ulong.MaxValue;
      response.StatusText = "Exception: " + ex.Message;
      response.Content.HasValue = false;
    }

    // Do not return NULL to CANoe, otherwise the Runtime Kernel will say good bye 
    
    return response;
  }
}

