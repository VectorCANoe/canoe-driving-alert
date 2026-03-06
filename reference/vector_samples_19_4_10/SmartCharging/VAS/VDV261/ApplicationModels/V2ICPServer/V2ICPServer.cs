using System;
using System.Linq;
using System.Net;
using System.Text;
using V2ICP.Endpoints;
using V2ICP.Interfaces;

using Vector.CANoe.Runtime;
using Vector.CANoe.Runtime.DBElements;
using Vector.CANoe.Threading;
using Vector.Tools;


public class V2ICPServer : MeasurementScript
{
  Timer tStartServer;

  [Vector.CANoe.Runtime.WaitingHandler]
  [OnCall(V2ICP.Endpoints.V2ICPServer.MemberIDs.OnRequest)]
  public _HTTP.DataTypes.HTTPResponseMessage OnRequest(_HTTP.DataTypes.HTTPRequestMessage genericRequestObject)
  {
    V2ICP.Interfaces.ServerPreProcessingData serverPreProcessingData = ServerPreProcessingData.CreateInstance();
    V2ICP.Interfaces.ServerPostProcessingData serverPostProcessingData = ServerPostProcessingData.CreateInstance();

    // Generic HTTP Response
    _HTTP.DataTypes.HTTPResponseMessage genericResponseObject = _HTTP.DataTypes.HTTPResponseMessage.CreateInstance();

    try
    {
      if ( 
         (!_OnRequestCheckMethod            (serverPreProcessingData, genericRequestObject, genericResponseObject))
      || (!_OnRequestCheckPath              (serverPreProcessingData, genericRequestObject, genericResponseObject))
      || (!_OnRequestCheckUserAgentHeader   (serverPreProcessingData, genericRequestObject, genericResponseObject))
      || (!_OnRequestCheckAuthHeader        (serverPreProcessingData, genericRequestObject, genericResponseObject))
      || (!_OnRequestCheckAcceptHeader      (serverPreProcessingData, genericRequestObject, genericResponseObject))
      || (!_OnRequestCheckContentTypeHeader (serverPreProcessingData, genericRequestObject, genericResponseObject))
      )
      {
        _AssignPreProcessingData(serverPreProcessingData);
        
        _TriggerAbort();
      }
      else
      {
        // HTTP Version
        // Host
        // Keep Alive
      
        #region Content Handling
        _ProcessContent(serverPreProcessingData, serverPostProcessingData, genericRequestObject, genericResponseObject);
        #endregion

        Execution.Wait(_GetResponseDelay());
      }
      
    }
    catch (Exception exc)
    {
      genericResponseObject.StatusCode = (ulong)HttpStatusCode.InternalServerError;
      genericResponseObject.StatusText.Assign(exc.ToString());
    }

    serverPostProcessingData.StatusCode.Value = genericResponseObject.StatusCode.Value;
    serverPostProcessingData.StatusText.Value = genericResponseObject.StatusText.Value;

    _AssignPostProcessingData(serverPostProcessingData);

    // Suspend is not yet available

    // Send Response
    return genericResponseObject;
  }

  private int _GetResponseDelay()
  {
    return (int)V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDelay.Value;
  }

  public void StartV2ICPServer(Object o, ElapsedEventArgs e)
  {
    V2ICP.Endpoints.V2ICPServer.Startup.Call();
    tStartServer.Stop(); // Cancel cyclic timer
  }

    /// <summary>Notification that the measurement starts.</summary>
  public override void Start()
  {
    tStartServer = new Timer(new TimeSpan(0, 0, 0, 0, 250), StartV2ICPServer);
    tStartServer.Start();
  }

  #region Control
  [OnCall(V2ICP.Endpoints.V2ICPServer.MemberIDs.Startup)]
  public void OnStartupRequest()
  {
    V2ICP.Endpoints.V2ICPServer.Connect();
  }

  [OnCall(V2ICP.Endpoints.V2ICPServer.MemberIDs.Shutdown)]
  public void OnShutdownRequest()
  {
    V2ICP.Endpoints.V2ICPServer.Disconnect();
  }
  #endregion


  #region Serialization Utilities

  private V2ICP.DataTypes.V1.V2ICPRequestContent DeserializeV2ICPRequestV1(byte[] requestBytes)
  {
    var requestStruct = V2ICP.DataTypes.V1.V2ICPSerializer.Deserialize_V2ICPRequestContent.CallAsyncAndWait(requestBytes, 1000).Call.Result;
    return requestStruct;
  }

  private byte[] SerializeV2ICPResponseV1(V2ICP.DataTypes.V1.V2ICPResponseContent responseStruct)
  {
    var responseBytes = V2ICP.DataTypes.V1.V2ICPSerializer.Serialize_V2ICPResponseContent.CallAsyncAndWait(responseStruct, 1000).Call.Result;
    return responseBytes;
  }

  private V2ICP.DataTypes.V2.V2ICPRequestContent DeserializeV2ICPRequestV2(byte[] requestBytes)
  {
    var requestStruct = V2ICP.DataTypes.V2.V2ICPSerializer.Deserialize_V2ICPRequestContent.CallAsyncAndWait(requestBytes, 1000).Call.Result;
    return requestStruct;
  }

  private byte[] SerializeV2ICPResponseV2(V2ICP.DataTypes.V2.V2ICPResponseContent responseStruct)
  {
    var responseBytes = V2ICP.DataTypes.V2.V2ICPSerializer.Serialize_V2ICPResponseContent.CallAsyncAndWait(responseStruct, 1000).Call.Result;
    return responseBytes;
  }

  #endregion


  private void _AssignPreProcessingData(V2ICP.Interfaces.ServerPreProcessingData processingData)
  {
    V2ICP.Endpoints.V2ICPServer.PreProcessingData.Assign(processingData);
  }

  private void _AssignPostProcessingData(V2ICP.Interfaces.ServerPostProcessingData processingData)
  {
    V2ICP.Endpoints.V2ICPServer.PostProcessingData.Assign(processingData);
  }

  private void _TriggerAbort()
  {
    V2ICP.Endpoints.V2ICPServer.OnProcessingAborted.Trigger();
  }


  private string _GetPath(_HTTP.DataTypes.HTTPRequestMessage genericRequestObject)
  {
    string requestUri = genericRequestObject.RequestUri;
    Uri uri = new Uri(requestUri);
    string absolutePath = uri.AbsolutePath;             // "/v1/vehicleMessage"

    return absolutePath;
  }

  private bool _IsPathV1(string path)
  {
    return string.Equals(path, V2ICP.Endpoints.V2ICPServer.Control.PathConfig.PathV1.Value, StringComparison.OrdinalIgnoreCase);
  }

  private bool _IsPathV1(_HTTP.DataTypes.HTTPRequestMessage genericRequestObject)
  {
    return _IsPathV1(_GetPath(genericRequestObject));
  }

  private bool _IsPathV2(string path)
  {
    return string.Equals(path, V2ICP.Endpoints.V2ICPServer.Control.PathConfig.PathV2.Value, StringComparison.OrdinalIgnoreCase);
  }

  private bool _IsPathV2(_HTTP.DataTypes.HTTPRequestMessage genericRequestObject)
  {
    return _IsPathV2(_GetPath(genericRequestObject));
  }

  private string _GetHeaderValue(_HTTP.DataTypes.HTTPRequestMessage genericRequestObject, string headerName)
  {
    string headerValue = null;

    for (int i = 0; i < genericRequestObject.Header.Value.Length; i++)
    {
      var header = genericRequestObject.Header.Value[i];

      var name = header.FieldName.Value;
      var val = header.FieldValue.Value;

      if (!name.Equals(headerName, StringComparison.InvariantCultureIgnoreCase))
      {
        continue;
      }

      headerValue = val;
      break;
    }

    return headerValue;
  }

  private bool _IsFormatVIN(string input)
  {
    if (input.Length != V2ICP.DataTypes.LengthVIN.Value)
    {
      return false;
    }
    return input.All(c => V2ICP.DataTypes.ValidCharsVIN.Value.Contains(c));
  }

  private bool _IsBasicAuthHeader(string authHeaderValue)
  {
    return authHeaderValue.StartsWith("Basic ", StringComparison.InvariantCultureIgnoreCase);
  }

  private string _GetAuthScheme(string authHeaderValue)
  {
    string authScheme = null;

    if (_IsBasicAuthHeader(authHeaderValue))
    {
      authScheme = authHeaderValue.Split(' ').FirstOrDefault()?.Trim();
    }

    return authScheme;
  }

  private bool _IsAuthSchemeBasic(string authScheme)
  {
    return string.Equals(authScheme, "Basic", StringComparison.Ordinal);
  }


  private bool _GetUsernameAndPasswordBasicAuthHeader(string authHeaderValue, out string basicAuthValueBase64, out string plainAuthValue, out string username, out string password)
  {
    basicAuthValueBase64 = authHeaderValue.Substring("Basic ".Length);
    plainAuthValue = Encoding.ASCII.GetString(Convert.FromBase64String(basicAuthValueBase64));
    
    var plainParts = plainAuthValue.Split(':');

    if (plainParts.Length != 2)
    {
      username = null;
      password = null;

      return false;
    }

    username = plainParts[0];
    password = plainParts[1];

    return true;
  }

  private bool _CheckUsernameValue(string usernameInRequest, string usernameExpected)
  {
    if (string.Equals(usernameInRequest
                        , usernameExpected
                        , StringComparison.Ordinal))
    {
      // Username as expected
      return true;
    }
    else
    {
      // Username not as expected
      return false;
    }
  }

  private bool _CheckUsernameFormat(string usernameInRequest)
  {
    // Check Username Format
    if (_IsFormatVIN(usernameInRequest))
    {
      return true;
    }
    else
    {
      return false;
    }
  }

  private void _SetResponse(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, HttpStatusCode code, string text)
  {
    genericResponseObject.StatusCode = (ulong)code;
    genericResponseObject.StatusText.Assign(text);
  }

  private void _SetResponseAuthHeaderMissing(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "Authorization Header missing";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseBadBasicAuthHeader(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "Basic Authorization Header conversion from Base64 to ASCII string failed";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseUsernameValueMismatch(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string usernameInRequest, string usernameExpected)
  {
    string text = "Basic Authorization Username value Mismatch. Expected '" +
                                        (usernameExpected ?? "NULL") +
                                        "'. Received '" +
                                        (usernameInRequest ?? "NULL") + "'";
  
    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseUsernameFormatMismatch(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string usernameInRequest)
  {
    string text = "Basic Authorization Username value format Mismatch. Expected VIN Format (" + 
                  V2ICP.DataTypes.LengthVIN.Value + 
                  " Characters in range " + 
                  V2ICP.DataTypes.ValidCharsVIN.Value + 
                  " ) . Received '" +
                  (usernameInRequest ?? "NULL") + 
                  "'";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetReponseAuthHeaderNotBasic(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "Authorization Header is not Basic";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }


  private bool _CheckPasswordValue(string passwordInRequest, out string passwordExpected)
  {
    passwordExpected = V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.Password.Value;

    if (string.Equals(passwordInRequest
                        , passwordExpected
                        , StringComparison.Ordinal))
    {
      // Password as expected
      return true;
    }
    else
    {
      // Password not as expected
      return false;
    }
  }

  private void _SetResponsePasswordValueMismatch(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string passwordInRequest, string passwordExpected)
  {
    string text = "Basic Authorization Password value Mismatch. Expected '" +
                  (passwordExpected ?? "NULL") +
                  "'. Received '" +
                  (passwordInRequest ?? "NULL") + 
                  "'";
  
    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseV1PasswordFormatMismatch(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string passwordInRequest)
  {
    string text = "Basic Authorization Password value format Mismatch. Expected format (1..150 characters ). Received '" +
                  (passwordInRequest ?? "NULL") + 
                  "'";
    
    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseV2PasswordFormatMismatch(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string passwordInRequest)
  {
    string text = "Basic Authorization Password value format Mismatch. Expected format (8..150 characters, 1x Upper, 1x Lower, 1x Number, 1x Special _-+#*!()? ). Received '" +
                  (passwordInRequest ?? "NULL") + 
                  "'";
  
    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);  
  }

  private void _SetResponsePasswordPathIssue(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "Request Path could not be used to resolve version related password formatting rules";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }


  private bool _CheckV1PasswordFormat(string passwordInRequest)
  {
    bool formatMatch = true;

    // V1 only specifies that the string must be 1..150 characters long plain ASCII

    // Min length
    if(passwordInRequest.Length < 1)
    {
      // No Basic Auth should have been used!
      formatMatch = false;
    }

    // Max length
    if(passwordInRequest.Length > 150)
    {
      formatMatch = false;
    }

    // All Characters ASCII
    if(passwordInRequest.Any(c => c > sbyte.MaxValue))
    {
      formatMatch = false;
    }

    return formatMatch;
  }

  private bool _CheckV2PasswordFormat(string passwordInRequest)
  {
    bool formatMatch = true;

    // V2 specifies that the string must be 8..150 characters long plain ASCII with 1 Upper Case, 1 Lower Case, 1x Number, 1x Special _-+#*!()?

    // Min length
    if (passwordInRequest.Length < 8)
    {
      // No Basic Auth should have been used!
      formatMatch = false;
    }

    // Max length
    if (passwordInRequest.Length > 150)
    {
      formatMatch = false;
    }

    // All Characters ASCII
    if (passwordInRequest.Any(c => c > sbyte.MaxValue))
    {
      formatMatch = false;
    }

    // At least 1 Upper Case Letter
    if(!passwordInRequest.Any(c => "ABCDEFGHIJKLMNOPQRSTUVWXYZ".Contains(c)))
    {
      formatMatch = false;
    }

    // At least 1 Lower Case Letter
    if (!passwordInRequest.Any(c => "abcdefghijklmnopqrstuvwxyz".Contains(c)))
    {
      formatMatch = false;
    }

    // At least 1 Special Character
    if (!passwordInRequest.Any(c => "_-+#*!()?".Contains(c)))
    {
      formatMatch = false;
    }

    // At least 1 Number
    if (!passwordInRequest.Any(c => "0123456789".Contains(c)))
    {
      formatMatch = false;
    }

    return formatMatch;
  }

  private void _SetResponseContentTypeHeaderMissing(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "Content-Type Header missing";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseContentTypeMismatch(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string contentTypeInRequest)
  {
    string text = "Content-Type Header value Mismatch. Expected '" +
                  (V2ICP.DataTypes.HTTPContentType.Value ?? "NULL") +
                  "'. Received '" +
                  (contentTypeInRequest ?? "NULL") + "'";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseAcceptHeaderMissing(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "Accept Header missing";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseAcceptMismatch(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string accept)
  {
    string text = "Accept Header value Mismatch. Expected '" +
                  (V2ICP.DataTypes.HTTPAccept.Value ?? "NULL") +
                  "'. Received '" +
                  (accept ?? "NULL") + "'";
  
    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseMethodMismatch(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string method)
  {
    string text = "Method value Mismatch. Expected '" +
                  (V2ICP.DataTypes.HTTPMethod.Value ?? "NULL") +
                  "'. Received '" +
                  (method ?? "NULL") + "'";
 
    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponseUnexpectedPath(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject, string path)
  {
    string text = "Unexpected Request Path '" + 
                  path + 
                  "'";

    _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
  }

  private void _SetResponsePathV1Rejected(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "V2ICP Request V1 rejected";

    _SetResponse(genericResponseObject, HttpStatusCode.NotImplemented, text);
  }

  private void _SetResponsePathV2Rejected(_HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "V2ICP Request V2 rejected";

    _SetResponse(genericResponseObject, HttpStatusCode.NotImplemented, text);
  }



  private bool _OnRequestCheckAuthHeader(ServerPreProcessingData serverProcessingData, 
                                         _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                                         _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string authHeaderValue = _GetHeaderValue(genericRequestObject, "Authorization");

    if (authHeaderValue == null)
    {
      // No Authorization Header found
      serverProcessingData.BasicAuthData.Value.HeaderPresent = false;

      if (V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.MustBePresent)
      {
        if ( ! V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.ContinueWhenHeaderMissing)
        {
          _SetResponseAuthHeaderMissing(genericResponseObject);
          return false;
        }
      }

      return true;
    }


    // Authorization Header found
    serverProcessingData.BasicAuthData.Value.HeaderPresent = true;

    // It could be any Authorization, so we need to search for 'Basic '

    var authScheme = _GetAuthScheme(authHeaderValue);

    serverProcessingData.BasicAuthData.Value.AuthorizationScheme = authScheme;

    if (!_IsAuthSchemeBasic(authScheme))
    {
      _SetReponseAuthHeaderNotBasic(genericResponseObject);
      return false;
    }

    // Basic Auth Header



    bool userNameAndPasswordRead = _GetUsernameAndPasswordBasicAuthHeader(authHeaderValue,
                                                                          out string basicAuthValueBase64,
                                                                          out string plainAuthValue,
                                                                          out string usernameInRequest,
                                                                          out string passwordInRequest);

    serverProcessingData.BasicAuthData.Value.Base64Value  = basicAuthValueBase64;
    serverProcessingData.BasicAuthData.Value.PlainValue   = plainAuthValue;
    serverProcessingData.BasicAuthData.Value.Username     = usernameInRequest;
    serverProcessingData.BasicAuthData.Value.Password     = passwordInRequest;

    if (!userNameAndPasswordRead)
    {
      // Unexpected Format of Auth String
      _SetResponseBadBasicAuthHeader(genericResponseObject);
      return false;
    }


    // Check Username
    string usernameExpected = V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.Username.Value;
    if (!_CheckUsernameValue(usernameInRequest, usernameExpected))
    {
      serverProcessingData.BasicAuthData.Value.UsernameMatch = false;

      if ( ! V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.ContinueWhenUsernameMismatch)
      {
        // Username Mismatch handling
        _SetResponseUsernameValueMismatch(genericResponseObject, usernameInRequest, usernameExpected);
        return false;
      }
    }
    else
    {
      serverProcessingData.BasicAuthData.Value.UsernameMatch = true;

      if (!_CheckUsernameFormat(usernameInRequest))
      {
        serverProcessingData.BasicAuthData.Value.UsernameFormatMatch = false;

        if ( ! V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.ContinueWhenUsernameFormatMismatch)
        {
          _SetResponseUsernameFormatMismatch(genericResponseObject, usernameInRequest);
          return false;
        }
      }
      else
      {
        serverProcessingData.BasicAuthData.Value.UsernameFormatMatch = true;
      }
    }

    // Check Password
    if (!_CheckPasswordValue(passwordInRequest, out string passwordExpected))
    {
      serverProcessingData.BasicAuthData.Value.PasswordMatch = false;

      if ( ! V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.ContinueWhenPasswordMismatch)
      {
        // Password Mismatch handling
        _SetResponsePasswordValueMismatch(genericResponseObject, passwordInRequest, passwordExpected);
        return false;
      }
    }
    else
    {
      serverProcessingData.BasicAuthData.Value.PasswordMatch = true;

      if (_IsPathV1(genericRequestObject))
      {
        if (!_CheckV1PasswordFormat(passwordInRequest))
        {
          serverProcessingData.BasicAuthData.Value.PasswordFormatMatch = false;

          if ( ! V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.ContinueWhenPasswordFormatMismatch)
          {
            _SetResponseV1PasswordFormatMismatch(genericResponseObject, passwordInRequest);
            return false;
          }
        }
        else
        {
          serverProcessingData.BasicAuthData.Value.PasswordFormatMatch = true;
        }
      }
      else if(_IsPathV2(genericRequestObject))
      {
        if (!_CheckV2PasswordFormat(passwordInRequest))
        {
          serverProcessingData.BasicAuthData.Value.PasswordFormatMatch = false;

          if ( ! V2ICP.Endpoints.V2ICPServer.Control.BasicAuthConfig.ContinueWhenPasswordFormatMismatch)
          {
            _SetResponseV2PasswordFormatMismatch(genericResponseObject, passwordInRequest);
            return false;
          }
        }
        else
        {
          serverProcessingData.BasicAuthData.Value.PasswordFormatMatch = true;
        }
      }
      else
      {
        _SetResponsePasswordPathIssue(genericResponseObject);
        return false;
      }
    }

    return true;
  }

  private bool _OnRequestCheckUserAgentHeader(ServerPreProcessingData serverProcessingData, 
                                              _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                                              _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string userAgentValue = _GetHeaderValue(genericRequestObject, "User-Agent");
    string text = "";

    if (userAgentValue == null)
    {
      // User Agent not found
      serverProcessingData.UserAgentData.Value.HeaderPresent = false;

      if (V2ICP.Endpoints.V2ICPServer.Control.UserAgentConfig.MustBePresent)
      {
        if ( ! V2ICP.Endpoints.V2ICPServer.Control.UserAgentConfig.ContinueWhenHeaderMissing)
        {
          text = "User-Agent Header missing";
          _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
          return false;
        }
        else
        {
          // Do not touch the Response

          return true;
        }
      }
    }
    else
    {
      serverProcessingData.UserAgentData.Value.HeaderPresent = true;
      serverProcessingData.UserAgentData.Value.UserAgent = userAgentValue;

      // Check against expected Value
      var v1 = V2ICP.DataTypes.V1.HTTPUserAgent.Value;
      var v2 = V2ICP.DataTypes.V2.HTTPUserAgent.Value;

      if (_IsPathV1(genericRequestObject))
      {
        if (string.Equals(userAgentValue, v1, StringComparison.InvariantCultureIgnoreCase))
        {
          serverProcessingData.UserAgentData.Value.UserAgentMatch = true;
          // Value as expected
          return true;
        }
        else
        {
          serverProcessingData.UserAgentData.Value.UserAgentMatch = false;

          if ( ! V2ICP.Endpoints.V2ICPServer.Control.UserAgentConfig.ContinueWhenMismatch)
          {
            text = "User-Agent Value Mismatch. Expected: '" + (v1 ?? "NULL") + "'. Received '" + (userAgentValue ?? "NULL") + "'";
            _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
            return false;
          }
          else
          {
            // Mismatch accepted
            // Do not touch the Response

            return true;
          }
        }
      }

      if (_IsPathV2(genericRequestObject))
      {
        if (string.Equals(userAgentValue, v2, StringComparison.InvariantCultureIgnoreCase))
        {
          serverProcessingData.UserAgentData.Value.UserAgentMatch = true;
          // Value as expected
          return true;
        }
        else
        {
          serverProcessingData.UserAgentData.Value.UserAgentMatch = false;

          if ( ! V2ICP.Endpoints.V2ICPServer.Control.UserAgentConfig.ContinueWhenMismatch)
          {
            text = "User-Agent Value Mismatch. Expected: '" + 
                   (v2 ?? "NULL") + 
                   "'. Received '" + 
                   (userAgentValue ?? "NULL") + 
                   "'";
            _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
            return false;
          }
          else
          {
            // Mismatch accepted
            // Do not touch the Response

            return true;
          }
        }
      }

      // Unexpected Route
      serverProcessingData.UserAgentData.Value.UserAgentMatch = false;
      text = "Unexpected request. User-Agent Value cannot be checked. Received '" + 
             (userAgentValue ?? "NULL") + 
             "'";
      _SetResponse(genericResponseObject, HttpStatusCode.PreconditionFailed, text);
      
      return false;
    }

    return true;
  }

  private bool _OnRequestCheckContentTypeHeader(ServerPreProcessingData serverProcessingData, 
                                                _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                                                _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string contentType = _GetHeaderValue(genericRequestObject, "Content-Type");

    // The content type must be "application/json; charset=US-ASCII"
    // if "application/json" not present -> further processing is most likely not possible
    // charset=US-ASCII might be ok

    if(contentType is null)
    {
      serverProcessingData.ContentTypeData.Value.HeaderPresent = false;
      serverProcessingData.ContentTypeData.Value.ContentType = string.Empty;
      serverProcessingData.ContentTypeData.Value.ContentTypeMatch = false;

      if ( ! V2ICP.Endpoints.V2ICPServer.Control.ContentTypeConfig.ContinueWhenHeaderMissing)
      {
        _SetResponseContentTypeHeaderMissing(genericResponseObject);
        return false;
      }

      return true; // Tolerate missing Header
    }

    serverProcessingData.ContentTypeData.Value.HeaderPresent = true;
    serverProcessingData.ContentTypeData.Value.ContentType = contentType;


    if (!string.Equals(contentType, V2ICP.DataTypes.HTTPContentType.Value))
    {
      serverProcessingData.ContentTypeData.Value.ContentTypeMatch = false;

      if ( ! V2ICP.Endpoints.V2ICPServer.Control.ContentTypeConfig.ContinueWhenContentTypeMismatch)
      {
        _SetResponseContentTypeMismatch(genericResponseObject, contentType);
        return false;
      }
    }
    else
    {
      serverProcessingData.ContentTypeData.Value.ContentTypeMatch = true;
    }
    

    return true;
  }

  private bool _OnRequestCheckAcceptHeader(ServerPreProcessingData serverProcessingData, 
                                           _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                                           _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string accept = _GetHeaderValue(genericRequestObject, "Accept");

    // The content type must be "application/json; charset=US-ASCII"
    // if "application/json" not present -> further processing is most likely not possible
    // if  "charset=US-ASCII" not present -> might be ok

    if (accept is null)
    {
      serverProcessingData.AcceptData.Value.HeaderPresent = false;
      serverProcessingData.AcceptData.Value.Accept = string.Empty;
      serverProcessingData.AcceptData.Value.AcceptMatch = false;

      if ( ! V2ICP.Endpoints.V2ICPServer.Control.AcceptConfig.ContinueWhenHeaderMissing)
      {
        _SetResponseAcceptHeaderMissing(genericResponseObject);
        return false;
      }

      return true; // Tolerate missing Header
    }

    serverProcessingData.AcceptData.Value.HeaderPresent = true;
    serverProcessingData.AcceptData.Value.Accept = accept;

    if (!string.Equals(accept, V2ICP.DataTypes.HTTPAccept.Value))
    {
      serverProcessingData.AcceptData.Value.AcceptMatch = false;

      if ( ! V2ICP.Endpoints.V2ICPServer.Control.AcceptConfig.ContinueWhenAcceptMismatch)
      {
        _SetResponseAcceptMismatch(genericResponseObject, accept);
        return false;
      }
    }
    else
    {
      serverProcessingData.AcceptData.Value.AcceptMatch = true;
    }

    return true;
  }

  private bool _OnRequestCheckMethod(ServerPreProcessingData serverProcessingData, 
                                     _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                                     _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string method = genericRequestObject.HTTPMethod;

    serverProcessingData.MethodData.Value.MethodValue = method;

    if (!string.Equals(method, V2ICP.DataTypes.HTTPMethod.Value, StringComparison.OrdinalIgnoreCase))
    {
      serverProcessingData.MethodData.Value.MethodMatch = false;
      _SetResponseMethodMismatch(genericResponseObject, method);
      return false;
    }

    serverProcessingData.MethodData.Value.MethodMatch = true;

    return true;
  }

  private bool _OnRequestCheckPath(ServerPreProcessingData serverProcessingData, 
                                   _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                                   _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string path = _GetPath(genericRequestObject);

    serverProcessingData.PathData.Value.PathValue = path;

    if (_IsPathV1(path))
    {
      serverProcessingData.PathData.Value.PathV1Match = true;
      serverProcessingData.PathData.Value.PathV2Match = false;

      if (V2ICP.Endpoints.V2ICPServer.Control.PathConfig.RejectPathV1)
      {
        _SetResponsePathV1Rejected(genericResponseObject);
        return false;
      }

      return true;
    }
    else if (_IsPathV2(path))
    {
      serverProcessingData.PathData.Value.PathV1Match = false;
      serverProcessingData.PathData.Value.PathV2Match = true;

      if (V2ICP.Endpoints.V2ICPServer.Control.PathConfig.RejectPathV2)
      {
        _SetResponsePathV2Rejected(genericResponseObject);
        return false;
      }

      return true;
    }
    else
    {
      serverProcessingData.PathData.Value.PathV1Match = false;
      serverProcessingData.PathData.Value.PathV2Match = false;

      _SetResponseUnexpectedPath(genericResponseObject, path);
      return false;
    }
  }



  private void _ProcessContent(ServerPreProcessingData serverPreProcessingData, 
                               ServerPostProcessingData serverPostProcessingData, 
                               _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                               _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string path = _GetPath(genericRequestObject);

    if (_IsPathV1(path))
    {
      _ProcessContentV1(serverPreProcessingData, 
                        serverPostProcessingData, 
                        genericRequestObject, 
                        genericResponseObject);
    }
    else if (_IsPathV2(path))
    {
      _ProcessContentV2(serverPreProcessingData, 
                        serverPostProcessingData, 
                        genericRequestObject, 
                        genericResponseObject);
    }
    else
    {
      // Should not reach this path due to earlier Path Check
      string text = HttpStatusCode.BadRequest.ToString();

      _SetResponse(genericResponseObject, HttpStatusCode.BadRequest, text);
    }
  }


  private void _ProcessContentV1(ServerPreProcessingData serverPreProcessingData,
                                 ServerPostProcessingData serverPostProcessingData, 
                                 _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                                 _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "";
    HttpStatusCode code;
    var requestBytes = genericRequestObject.Body.Value;
    V2ICP.DataTypes.V1.V2ICPResponseContent responseStruct = V2ICP.DataTypes.V1.V2ICPResponseContent.CreateInstance();

    serverPreProcessingData.V2RequestData.HasValue = false;
    serverPreProcessingData.V2RequestString.HasValue = false;
    serverPostProcessingData.V2ResponseData.HasValue = false;
    serverPostProcessingData.V2ResponseString.HasValue = false;

    serverPreProcessingData.V1RequestString.Value.Assign(Encoding.UTF8.GetString(requestBytes));

    // Deserialize Request Struct
    var requestStruct = DeserializeV2ICPRequestV1(requestBytes);

    if (requestStruct == null)
    {
      // Failed to Deserialize Request. Further details can be found in the Binding Error prompt
      // Should we make the data types less restrictive to see value range violations?

      serverPreProcessingData.V1RequestData.HasValue = false;
      serverPostProcessingData.V1ResponseData.HasValue = false;

      text = HttpStatusCode.BadRequest.ToString();
      code = HttpStatusCode.BadRequest;
      _SetResponse(genericResponseObject, code, text);

      return;
    }
    else
    {
      serverPreProcessingData.V1RequestData.Value.Assign(requestStruct);
    }      

    // ToDo
    // Check Request
    // Check Sequence Counter
    // Check VIN
    // Check Seq 0 Content
    // Check Seq != 0 Content
    // Check Seq 255 -> 0

    _AssignPreProcessingData(serverPreProcessingData);
    V2ICP.Endpoints.V2ICPServer.OnRequestReceived.Trigger();
    Execution.Wait(100); // Wait 100ms


    // Determine Response Data (Fault Injection)
    byte[] responseBytes;
    if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomContentBytes.HasValue)
    {
        responseBytes = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomContentBytes.Value;

        serverPostProcessingData.V1ResponseData.HasValue = false;
    }
    else if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomContentString.HasValue)
    {
        responseBytes = Encoding.ASCII.GetBytes(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomContentString.Value);

        serverPostProcessingData.V1ResponseData.HasValue = false;
    }
    else
    {
      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomSequenceNumber.HasValue)
      {
        responseStruct.seq = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomSequenceNumber.Value.Value;
      }
      else
      {
        responseStruct.seq = requestStruct.seq;
      }
      
      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomVIN.HasValue)
      {
        responseStruct.vin = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomVIN.Value;
      }
      else
      {
        responseStruct.vin = requestStruct.vin;
      }

      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV1.AmbientTemp.HasValue)
      {
        responseStruct.ambienttemp.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV1.AmbientTemp.Value;
      }
      else
      {
        responseStruct.ambienttemp.Value = V2ICP.DataTypes.V1.ambienttemp_SNA.Value; // SNA
      }
      
      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV1.Driveoff.HasValue)
      {
        responseStruct.driveoff.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV1.Driveoff.Value;
      }
      else
      {
        responseStruct.driveoff.Value = V2ICP.DataTypes.V1.driveoff_SNA.Value; // SNA
      }

      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV1.PrecDsrd.HasValue)
      {
        responseStruct.prec_dsrd.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV1.PrecDsrd.Value;
      }
      else
      {
        responseStruct.prec_dsrd.Value = V2ICP.DataTypes.V1.PreconditioningRequestByDMS.SNA;
      }

      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV1.PrecHvac.HasValue)
      {
        responseStruct.prec_hvac.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV1.PrecHvac.Value;
      }
      else
      {
        responseStruct.prec_hvac.Value = V2ICP.DataTypes.V1.PreconditioningRequestByHVAC.NO_PRECONDITIONING_OR_SNA;
      }


      serverPostProcessingData.V1ResponseData.Value.Assign(responseStruct);
      
      responseBytes = SerializeV2ICPResponseV1(responseStruct);
    }

    genericResponseObject.Body.Value.Assign(responseBytes);

    serverPostProcessingData.V1ResponseString.Value.Assign(Encoding.ASCII.GetString(responseBytes));

    if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomStatusText.HasValue)
    {
      text = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomStatusText.Value;
    }
    else
    {
      text = HttpStatusCode.OK.ToString();
      
    }

    if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomStatusCode.HasValue)
    {
      code = (HttpStatusCode) (V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomStatusCode.Value.Value);
    }
    else
    {
      code = HttpStatusCode.OK;
    }


    _SetResponse(genericResponseObject, code, text);
  }


 private void _ProcessContentV2(ServerPreProcessingData serverPreProcessingData,
                                 ServerPostProcessingData serverPostProcessingData, 
                                 _HTTP.DataTypes.HTTPRequestMessage genericRequestObject, 
                                 _HTTP.DataTypes.HTTPResponseMessage genericResponseObject)
  {
    string text = "";
    HttpStatusCode code;
    var requestBytes = genericRequestObject.Body.Value;
    V2ICP.DataTypes.V2.V2ICPResponseContent responseStruct = V2ICP.DataTypes.V2.V2ICPResponseContent.CreateInstance();

    serverPreProcessingData.V2RequestData.HasValue = false;
    serverPreProcessingData.V2RequestString.HasValue = false;
    serverPostProcessingData.V2ResponseData.HasValue = false;
    serverPostProcessingData.V2ResponseString.HasValue = false;

    serverPreProcessingData.V2RequestString.Value.Assign(Encoding.UTF8.GetString(requestBytes));

    // Deserialize Request Struct
    var requestStruct = DeserializeV2ICPRequestV2(requestBytes);

    if (requestStruct == null)
    {
      // Failed to Deserialize Request. Further details can be found in the Binding Error prompt
      // Should we make the data types less restrictive to see value range violations?

      serverPreProcessingData.V2RequestData.HasValue = false;
      serverPostProcessingData.V2ResponseData.HasValue = false;

      text = HttpStatusCode.BadRequest.ToString();
      code = HttpStatusCode.BadRequest;
      _SetResponse(genericResponseObject, code, text);

      return;
    }
    else
    {
      serverPreProcessingData.V2RequestData.Value.Assign(requestStruct);
    }      

    // ToDo
    // Check Request
    // Check Sequence Counter
    // Check VIN
    // Check Seq 0 Content
    // Check Seq != 0 Content
    // Check Seq 255 -> 0

    _AssignPreProcessingData(serverPreProcessingData);
    V2ICP.Endpoints.V2ICPServer.OnRequestReceived.Trigger();
    Execution.Wait(100); // Wait 100ms


    // Determine Response Data (Fault Injection)
    byte[] responseBytes;
    if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomContentBytes.HasValue)
    {
        responseBytes = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomContentBytes.Value;

        serverPostProcessingData.V2ResponseData.HasValue = false;
    }
    else if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomContentString.HasValue)
    {
        responseBytes = Encoding.ASCII.GetBytes(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomContentString.Value);

        serverPostProcessingData.V2ResponseData.HasValue = false;
    }
    else
    {
      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomSequenceNumber.HasValue)
      {
        responseStruct.seq = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomSequenceNumber.Value.Value;
      }
      else
      {
        responseStruct.seq = requestStruct.seq;
      }
      
      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomVIN.HasValue)
      {
        responseStruct.vin = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomVIN.Value;
      }
      else
      {
        responseStruct.vin = requestStruct.vin;
      }

      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.AmbientTemp.HasValue)
      {
        responseStruct.ambienttemp.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.AmbientTemp.Value;
      }
      else
      {
        responseStruct.ambienttemp.Value = V2ICP.DataTypes.V2.ambienttemp_SNA.Value; // SNA
      }
      
      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.Driveoff.HasValue)
      {
        responseStruct.driveoff.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.Driveoff.Value;
      }
      else
      {
        responseStruct.driveoff.Value = V2ICP.DataTypes.V2.driveoff_SNA.Value; // SNA
      }

      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.PrecDsrd.HasValue)
      {
        responseStruct.prec_dsrd.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.PrecDsrd.Value;
      }
      else
      {
        responseStruct.prec_dsrd.Value = V2ICP.DataTypes.V2.PreconditioningRequestByDMS.SNA;
      }

      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.PrecHvac.HasValue)
      {
        responseStruct.prec_hvac.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.PrecHvac.Value;
      }
      else
      {
        responseStruct.prec_hvac.Value = V2ICP.DataTypes.V2.PreconditioningRequestByHVAC.SNA;
      }

      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.TargetDistance.HasValue)
      {
        responseStruct.target_dist.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.TargetDistance.Value;
      }
      else
      {
        responseStruct.target_dist.Value = V2ICP.DataTypes.V2.target_dist_SNA.Value;
      }      

      if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.TargetSoC.HasValue)
      {
        responseStruct.target_soc.Value = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.ResponseDataV2.TargetSoC.Value;
      }
      else
      {
        responseStruct.target_soc.Value = V2ICP.DataTypes.V2.target_soc_SNA.Value;
      }    
      
      serverPostProcessingData.V2ResponseData.Value.Assign(responseStruct);
      
      responseBytes = SerializeV2ICPResponseV2(responseStruct);
    }

    genericResponseObject.Body.Value.Assign(responseBytes);

    serverPostProcessingData.V2ResponseString.Value.Assign(Encoding.ASCII.GetString(responseBytes));

    if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomStatusText.HasValue)
    {
      text = V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomStatusText.Value;
    }
    else
    {
      text = HttpStatusCode.OK.ToString();
      
    }

    if(V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomStatusCode.HasValue)
    {
      code = (HttpStatusCode) (V2ICP.Endpoints.V2ICPServer.Control.ResponseControl.FaultInjection.CustomStatusCode.Value.Value);
    }
    else
    {
      code = HttpStatusCode.OK;
    }


    _SetResponse(genericResponseObject, code, text);
  }




} // class HTTPServer
