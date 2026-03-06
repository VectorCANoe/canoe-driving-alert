using System;
using System.Runtime.Serialization;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Diag = Vector.Diagnostics;
using Vector.Scripting.UI;
using Vector.CANoe.TFS;
using Vector.CANoe.VTS;

using rep = Vector.CANoe.TFS.Report;
using ExternalSignals; // System Variables to stimulate the ECU

[TestClass]
public class DotNetTest
{
  const string EcuQualifier = "DoorFR";
  const string FgrQualifier = "FunctionalGroup";

  static void ApplyVoltage(double voltage, uint ms)
  {
    SupplyVoltage.Value = voltage;

    rep.TestStep(string.Format("Stimulate ECU with voltage {0:f1}V for 1 sec.", voltage));
    Vector.CANoe.Threading.Execution.Wait((int)ms); // Wait until DTC should have been stored in case of over- or undervoltage before reading the fault memory
  }

  static void InitFaultMemAndGenerateTwoDTCs()
  {
    // Simulated Voltages applied via System Variable
    const double NormalVoltageValue_V = 12.4;
    const double HighVoltageValue1_V = 15.4;
    const double HighVoltageValue2_V = 16.1;
    const double LowVoltageValue_V = 9.5;

    ApplyVoltage(LowVoltageValue_V, 1010);   // Low voltage: Stimulate setting 1nd DTC (0x000001)
    ApplyVoltage(HighVoltageValue1_V, 1010);// High voltage, 1st time: Stimulate setting 2nd DTC (0x000002)
    ApplyVoltage(NormalVoltageValue_V, 20);  // Set voltage back to normal level
    ApplyVoltage(HighVoltageValue2_V, 1010); // High voltage, 2nd time:  Add snapshot record for DTC 0x000002
    ApplyVoltage(NormalVoltageValue_V, 10);  // Set voltage back to normal level
  }

  static Diag.Response sendReqestAndReceiveResponse(Diag.Request req, bool PositiveResponseExpectedFlag)
  {
    rep.TestStep("Trying to send diagnostic request");
    Diag.SendResult result = req.Send();

    if (result.Status == Diag.SendStatus.CommunicationError)
    {
      rep.TestStepFail("Communication error when sending diagnostic request!");
      return null;
    }

    if (result.Status != Diag.SendStatus.Ok)
      return null;

    if (result.Response == null)
    {
      rep.TestStepFail("Did not receive a diagnostic response!");
      return null;
    }

    rep.TestStepPass("Successfully received a diagnostic response!");

    // process response object
    Diag.Response response = result.Response;


    if (response.IsPositive)
    {
      if (PositiveResponseExpectedFlag)
      {
        rep.TestStepPass("Received positive diagnostic response as expected!");

        string str = "";
        for (int k = 0; k < response.Pdu.GetLength(0); k++)
        {
          str = str + string.Format("{0:X2} ", response.Pdu[k]);
        }

        rep.TestStepPass("PDU: " + str);
        return response;
      }
      else
      {
        rep.TestStepFail("Received positive instead of negative response!");
      }
    }
    else // Negative response 
    {
      using (Diag.Parameter nrc = response.Parameters["RC"])
      {
        if (nrc != null)
        {
          if (!PositiveResponseExpectedFlag)
          {
            rep.TestStepPass("Received negative response as expected, NRC=" + nrc.Value.ToString() + "!");
            return response;
          }
          else
          {
            rep.TestStepFail("Received negative response (NRC=" + nrc.Value.ToString() + ") instead of positive response !");
          }
        }
        else
        {
          rep.TestStepFail("NRC not found in negative response!");
        }
      }
    }

    return null; // error occurred
  }

  [Export]
  [TestCase]
  public static void PerformAuthentication()
  {
    using (Diag.Ecu ecuDoor = Diag.Application.GetEcu(EcuQualifier))
    {
      if (ecuDoor == null)
      {
        rep.TestStepFail("No ECU with this ECU qualifier found!");
        return;
      }

      Diag.AuthenticationResult result = ecuDoor.Authenticate("Cert=UDS 0x29 Supplier;AutoSessionChange=1;");
      if (result == Diag.AuthenticationResult.Ok)
      {
        rep.TestStepPass("Authentication successful.");
      }
      else
      {
        rep.TestStepFail("Authentication failed!");
      }
    }
  }

  [Export]
  [TestCase]
  public static void ReadSerialNumber()
  {
    using (Diag.Ecu ecuDoor = Diag.Application.GetEcu(EcuQualifier))
    {
      if (ecuDoor == null)
      {
        rep.TestStepFail("No ECU with this ECU qualifier found!");
        return;
      }

      using (Diag.Request reqReadSerialNumber = ecuDoor.CreateRequest("SerialNumber_Read"))
      {
        // alternatively, create raw request:
        //Diag.Request reqReadSerialNumber = ecuDoor.CreateRequest(new byte[] { 0x22, 0xF1, 0x8C });

        using (Diag.Response resp = sendReqestAndReceiveResponse(reqReadSerialNumber, true))
        {
          if (resp != null)
          {
            Diag.Parameter serialNumber = resp.GetParameter("SerialNumber");
            if (serialNumber == null)
            {
              rep.TestStepFail("Parameter not found in response!");
            }
            else
            {
              rep.TestStepPass("Read " + serialNumber.ToString());
            }
          }
        }
      }
    }

    Vector.CANoe.Threading.Execution.Wait(1);
  }

  [Export]
  [TestCase]
  public static void ReadSerialNumberFunctional()
  {
    using (Diag.Ecu fgr = Diag.Application.GetEcu(FgrQualifier))
    {

      if (fgr == null)
      {
        rep.TestStepFail("No ECU with this ECU qualifier found!");
        return;
      }

      using (Diag.Request reqReadSerialNumber = fgr.CreateRequest("SerialNumber_Read"))
      {

        using (Diag.SendResult result = reqReadSerialNumber.Send())
        {
          if (result.Status == Diag.SendStatus.CommunicationError)
          {
            rep.TestStepFail("Communication error when trying to send diagnostic request to functional group!");
            return;
          }
          else if (result.Status == Diag.SendStatus.Ok)
          {
            if (result.Responses != null)
            {
              // Process response objects
              if (2 != result.Responses.Count)
              {
                rep.TestStepFail("Did not receive expected number of responses (" + result.Responses.Count.ToString() + " instead of 2)");
              }
              else
              {
                foreach (Diag.Response response in result.Responses)
                {
                  using (Diag.Parameter serialNumber = response.GetParameter("SerialNumber"))
                  {
                    if (serialNumber == null)
                    {
                      rep.TestStepFail("No serial number found in response!");
                    }
                    else
                    {
                      rep.TestStepPass("Read " + serialNumber.ToString());
                    }
                  }
                }
              }
            }
            else
            {
              rep.TestStepFail("Error when receiving response!");
            }
          }
        }
      }
    }

    Vector.CANoe.Threading.Execution.Wait(1);
  }

  [Export]
  [TestCase]
  public static void VariantCoding()
  {
    const byte SecurityLevel1 = 0x01;
    const byte SecurityLevel2 = 0x11;

    using (Diag.Ecu ecuDoor = Diag.Application.GetEcu(EcuQualifier))
    {
      if (ecuDoor == null)
      {
        rep.TestStepFail("No ECU with this ECU qualifier found!");
        return;
      }

      // Switch to extended session
      using (Diag.Request reqExtSessionStart = ecuDoor.CreateRequest("ExtendedDiagnosticSession_Start"))
      {
        using (Diag.Response resp = sendReqestAndReceiveResponse(reqExtSessionStart, true))
        {
          if (resp != null)
          {
            // Unlock ECU
            Diag.SecurityAccessResult result = ecuDoor.Unlock(SecurityLevel1, "AB"); // Option String 'AB' will be passed to the Seed&Key DLL

            if (result != Diag.SecurityAccessResult.Success)
            {
              rep.TestStepFail("Could not unlock ECU with SecurityLevel 0x01!");
              rep.TestStepFail("Result=" + result.ToString());
            }
            else
            {
              rep.TestStepPass("Successfully unlocked ECU with SecurityLevel1 0x01!");
            }

            result = ecuDoor.Unlock(SecurityLevel2, "CDEF"); // Option String 'CDEF' will be passed to the Seed&Key DLL

            if (result != Diag.SecurityAccessResult.Success)
            {
              rep.TestStepFail("Could not unlock ECU with Security Level 0x11!");
              rep.TestStepFail("Result=" + result.ToString());
            }
            else
            {
              rep.TestStepPass("Successfully unlocked ECU with SecurityLevel 0x11!");
            }
          }
        }
      }
    }

    Vector.CANoe.Threading.Execution.Wait(1);
  }

  [Export]
  [TestCase]
  public static void CheckFaultMemory()
  {
    using (Diag.Ecu ecuDoor = Diag.Application.GetEcu(EcuQualifier))
    {
      if (ecuDoor == null)
      {
        rep.TestStepFail("No ECU with this ECU qualifier found!");
        return;
      }

      InitFaultMemAndGenerateTwoDTCs();

      using (Diag.Request reqReadFaultMemory = ecuDoor.CreateRequest("FaultMemory_ReadAllIdentified"))
      {
        if (reqReadFaultMemory != null)
        {
          using (Diag.Parameter StatusMask = reqReadFaultMemory.GetParameter("DtcStatusbyte"))
          {
            if (StatusMask == null)
            {
              rep.TestStepFail("Parameter 'DtcStatusbyte' not found!");
            }
            else
            {
              uint[] expectedDTC = { 0x000016, 0x000017 };
              byte[] rawStatusMask = { 0x09 };

              StatusMask.Value.Set(rawStatusMask); // Set raw parameter value because we access a structure here (alternatively, set each single bit individually)

              using (Diag.Response resp = sendReqestAndReceiveResponse(reqReadFaultMemory, true))
              {
                // Evaluate Fault Memory Contents
                using (Diag.Parameter iterParam = resp.Parameters["ListOfDTC"])
                {
                  if (iterParam != null)
                  {
                    // List of DTCs is available
                    if (iterParam.Parameters.Count == 2)
                    {
                      // List is not empty, check all DTCs
                      for (int k = 0; k < iterParam.Parameters.Count; k++)
                      {
                        using (Diag.Parameter dtc = iterParam.Parameters[k].Parameters["DTC"])
                        {
                          if (dtc.Value.ToUInt32() == expectedDTC[k])
                          {
                            rep.TestStepPass(string.Format("Found expected DTC 0x{0:X6}!", expectedDTC[k]));
                          }
                          else
                          {
                            rep.TestStepFail(string.Format("Did not find expected DTC 0x{0:X6}!", expectedDTC[k]));
                          }
                        }
                      }
                    }
                    else
                    {
                      rep.TestStepFail("Did not find expected number of DTCs!");
                    }
                  }
                  else
                  {
                    rep.TestStepFail("Did not find any DTC!");
                  }
                }
              }
            }
          }
        }
        else
        {
          rep.TestStepFail("Could not create request!");
        }
      }
    }

    Vector.CANoe.Threading.Execution.Wait(1);
  }

  [Export]
  [TestCase]
  public static void CheckFaultMemoryNew()
  {
    const int ExpectedNumberOfSnapshotRecords = 2;
    const int ExpectedNumberOfSnapshotParams = 4;

    using (Diag.Ecu ecuDoor = Diag.Application.GetEcu(EcuQualifier))
    {
      if (ecuDoor == null)
      {
        rep.TestStepFail("No ECU with this ECU qualifier found!");
        return;
      }

      ecuDoor.ActivateTesterPresent(true);
      InitFaultMemAndGenerateTwoDTCs();

      rep.TestStep("Reading DTCs without status byte parameter.");
      using (Diag.ReadDtcResult result = ecuDoor.ReadDtcs())
      {

        if (result.Status == Diag.FaultMemoryStatus.Success)
        {
          foreach (Diag.Dtc dtc in result.Dtcs)
          {
            rep.TestStepPass(string.Format("Found DTC 0x{0:X6} with Display trouble code 0x{1:X6}, Error text '{2}', SAE code '{3}' and Status 0x{4:X2}!",
              dtc.HexCode, dtc.DisplayTroubleCode, dtc.ErrorText, dtc.SaeCode, dtc.Status));

            rep.TestStep(string.Format("DTC 0x{0}", dtc.HexCode), string.Format("Found following additional information for DTC 0x{0:X6}:", dtc.HexCode));

            foreach (Diag.DtcInformation addInfo in dtc.DtcInformationItems)
            {
              if (addInfo.Unit == "")
              {
                rep.TestStepPass(string.Format("'{0}': value: {1}", addInfo.Name, addInfo.Value));
              }
              else
              {
                rep.TestStepPass(string.Format("'{0}': value: {1}, unit: {2}", addInfo.Name, addInfo.Value, addInfo.Unit));
              }
            }
          }
          if (result.Dtcs.Count != 2)
          {
            rep.TestStepFail(string.Format("Only found {0} insted of 2 DTCs!", result.Dtcs.Count));
          }
        }
        else
        {
          rep.TestStepFail(string.Format("Error: Reading DTCs failed!"));
        }

        rep.TestStep("Reading DTCs with status byte value 0x09.");
        using (Diag.ReadDtcResult result2 = ecuDoor.ReadDtcs(0x09))
        {

          if (result2.Status == Diag.FaultMemoryStatus.Success)
          {
            foreach (Diag.Dtc dtc2 in result2.Dtcs)
            {
              rep.TestStepPass(string.Format("Found DTC 0x{0:X6} with Error text '{1}', SAE code '{2}' and Status 0x{3:X2}!", dtc2.HexCode, dtc2.ErrorText, dtc2.SaeCode, dtc2.Status));

              var clearDtcResult = ecuDoor.ClearDtc(dtc2);

              if (clearDtcResult.Status == Diag.FaultMemoryStatus.Success)
              {
                rep.TestStepPass(string.Format("Clearing DTC {0} worked.", dtc2.HexCode));
              }
              else
              {
                rep.TestStepFail(string.Format("Error clearing DTC {0}: {1}", dtc2.HexCode, clearDtcResult.Status));
              }
            }
          }
          else
          {
            rep.TestStepFail(string.Format("Error: Reading DTCs failed!"));
          }

          rep.TestStep("Re-generating two DTCs.");
          InitFaultMemAndGenerateTwoDTCs();
          InitFaultMemAndGenerateTwoDTCs();

          rep.TestStep("Reading DTCs without status byte parameter.");
          using (Diag.ReadDtcResult result3 = ecuDoor.ReadDtcs())
          {

            if (result3.Status == Diag.FaultMemoryStatus.Success)
            {
              rep.TestStep(string.Format("Found {0} DTCs!", result3.Dtcs.Count));

              foreach (Diag.Dtc dtc3 in result3.Dtcs)
              {
                // read all available snapshot records
                Diag.ReadEnvironmentDataResult resultenv3 = ecuDoor.ReadSnapshotDataRecords(dtc3);
                if (resultenv3.EnvironmentData.Count == ExpectedNumberOfSnapshotRecords)
                {
                  rep.TestStepPass(string.Format("Found {0} snapshot records for DTC 0x{1:X6}!", resultenv3.EnvironmentData.Count, dtc3.HexCode));

                  foreach (Diag.ParameterCollection SnapShot in resultenv3.EnvironmentData)
                  {
                    rep.TestStep(string.Format("Snapshot {0}", (SnapShot[0].Parameters[0].Value.GetBytes())[0]),
                      string.Format("Evaluating snapshot '{0}' of DTC 0x{1:X6}!", SnapShot[0].Parameters[0].Value, dtc3.HexCode));

                    // read snapshot record
                    Diag.ParameterCollection SnapShotParams = SnapShot[0].Parameters[2].Parameters;
                    if (SnapShotParams.Count > 0)
                    {
                      rep.TestStep(string.Format("Found following Snapshot Parameters for DTC 0x{0:X6}:", dtc3.HexCode));
                      foreach (Diag.Parameter SnapshotParam in SnapShotParams)
                      {
                        if (SnapshotParam.Unit == "")
                        {
                          rep.TestStepPass(string.Format("{0}: {1}", SnapshotParam.Name.ToString(), SnapshotParam.Value));
                        }
                        else
                        {
                          rep.TestStepPass(string.Format("{0}: {1} [{2}]", SnapshotParam.Name.ToString(), SnapshotParam.Value, SnapshotParam.Unit));
                        }
                      }
                    }
                    if (SnapShotParams.Count != ExpectedNumberOfSnapshotParams)
                    {
                      rep.TestStepFail(string.Format("SnapShotParams.Count of DTC 0x{0:X6} different than expected: {1} instead of {2}", dtc3.HexCode, SnapShotParams.Count, ExpectedNumberOfSnapshotParams));
                    }
                  }
                }
                else
                {
                  rep.TestStepFail(string.Format("SnapShotParams.Count of DTC 0x{0:X6} different than expected: {1} instead of {2}", dtc3.HexCode, resultenv3.EnvironmentData.Count, ExpectedNumberOfSnapshotRecords));
                }
              }
            }
            else
            {
              rep.TestStepFail(string.Format("Error: Reading DTCs failed, Status: {0}!", result3.Status.ToString()));
            }
          }
        }
      }
    }

    Vector.CANoe.Threading.Execution.Wait(100);
  }
}