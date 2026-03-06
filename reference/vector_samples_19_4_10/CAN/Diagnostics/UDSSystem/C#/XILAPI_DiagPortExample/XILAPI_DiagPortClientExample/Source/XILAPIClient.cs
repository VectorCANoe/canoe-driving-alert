/*---------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
---------------------------------------------------------------------------*/

#region Usings

using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using System.Runtime.Remoting.Metadata.W3cXsd2001; // for certificate hex string to byte array conversion

// ASAM XIL Assemblies (to be installed with setup from from "<CANoe installation directory>\Installer Additional Components\XILAPI")
using ASAM.XIL.Implementation.TestbenchFactory.Testbench;
using ASAM.XIL.Interfaces.Testbench;
using ASAM.XIL.Interfaces.Testbench.Common.ValueContainer;
using ASAM.XIL.Interfaces.Testbench.DiagPort;
using ASAM.XIL.Interfaces.Testbench.DiagPort.Enum;

#endregion

namespace XILAPI_DiagPortClientExample.Source
{
  internal class XilApiClient
  {
    /// <summary>
    ///   Visible data grid rows for initialization of faultMemory structure
    /// </summary>
    private readonly int _mIVisibleDataGridRows;

    // Diagnostic Port instance
    private IDiagPort _mDiagnosticPort;

    // ECU instance
    private IECU _mEcu;

    // Test bench instance
    private ITestbench _mTestBench;
    
    /// <summary>
    ///   Constructor of the XilApiClient class.
    /// </summary>
    /// <param name="faultMemory">Structure containing the fault memory contents to be displayed.</param>
    /// <param name="visibleDataGridRows">Visible data grid rows for initialization of faultMemory structure.</param>
    public XilApiClient(out XilApiDialog.FaultMemStruct faultMemory, int visibleDataGridRows)
    {
      _mIVisibleDataGridRows = visibleDataGridRows;
      InitFaultMemContents(out faultMemory);
    }

    /// <summary>
    ///   Gets a value indicating whether the Diagnostic port is connected.
    /// </summary>
    /// <value>
    ///   <c>true</c> if this instance is connected; otherwise, <c>false</c>.
    /// </value>
    public bool IsConnected { get; private set; }

    /// <summary>
    ///   Initializes the test bench and the Diagnostic port and sets the diagnostic target.
    /// </summary>
    /// <param name="vendorName">Name of the vendor.</param>
    /// <param name="productName">The product name.</param>
    /// <param name="productVersion">The product version.</param>
    /// <param name="diagnosticPortConfigurationFile">The Diagnostic port configuration file.</param>
    /// <param name="ecuQualifier">The ECU Qualifier of the diagnostic target.</param>
    public void Init(string vendorName, string productName, string productVersion, string diagnosticPortConfigurationFile, string ecuQualifier)
    {
      // Create the test bench
      try
      {
        var factory = new TestbenchFactory();
        _mTestBench = factory.CreateVendorSpecificTestbench(vendorName, productName, productVersion);
      }
      catch (Exception ex)
      {
        var msg = "Could not create the test bench. Is the ASAM XIL API and CANoe XIL API correctly installed?";
        msg += Environment.NewLine + Environment.NewLine;
        msg += "Error details: " + ex.Message;

        throw new Exception(msg);
      }

      // Create the Diagnostic port
      try
      {
        _mDiagnosticPort = _mTestBench.DiagPortFactory.CreateDiagPort("Example Diagnostic Port");
        _mDiagnosticPort.Configure(_mDiagnosticPort.LoadConfiguration(diagnosticPortConfigurationFile));
      }
      catch (Exception ex)
      {
        var msg = "Could not create the Diagnostic port.";
        msg += Environment.NewLine + Environment.NewLine;
        msg += "Error details: " + ex.Message + Environment.NewLine + Environment.NewLine;
        msg += "Did you enable the XIL API Server port under 'CANoe Options | Extensions | XIL API & FDX protocol'?";

        throw new Exception(msg);
      }

      // Set the diagnostic target
      try
      {
        _mEcu = _mDiagnosticPort.GetECU(ecuQualifier);
      }
      catch (Exception ex)
      {
        var msg = "Could not set diagnostic target.";
        msg += Environment.NewLine + Environment.NewLine;
        msg += "Error details: " + ex.Message;

        throw new Exception(msg);
      }

      IsConnected = true;

      _mEcu.SetCommunicationMode(CommunicationMode.eEXPLICIT);
      _mEcu.StartCommunication();
    }

    /// <summary>
    ///   Shutdown of the test bench.
    /// </summary>
    public void Shutdown()
    {
      IsConnected = false;

      _mDiagnosticPort.Disconnect();
      _mDiagnosticPort.Dispose();
    }

    /// <summary>
    ///   Reads the serial number of the ECU via diagnostic service.
    /// </summary>
    /// <param name="strSerialNumber">String with serial number to be returned.</param>
    public void ReadSerialNumber(out string strSerialNumber)
    {
      var didSerNumberRead = _mEcu.CreateDIDByName("Serial Number");
      var data = _mEcu.ReadDIDValue(didSerNumberRead);
      strSerialNumber = "";

      if (data.Values.Count <= 0) return;

      if (data.Values.ElementAt(0).PhysicalValue is IUintValue serialNumber)
      {
        strSerialNumber = serialNumber.Value.ToString();
      }
    }

    /// <summary>
    ///   Authenticates the tester at the diagnostic target using UDS service 0x29 "Authentication".
    /// </summary>
    private void Authenticate()
    {
      // For simplification, the response data of the ECU is not checked here.
      // Additionally, the ECU simulation in UDSSystem.cfg does not check the data in "Authentication Verify Certificate Unidirectional" and 
      // "Authentication Proof Of Ownership", therefore sending the request with null data is sufficient.
      var ecuBaseController = _mEcu.GetECUBaseController();
      const string cert = "30820206308201ABA0030201020214716C5CB5A9189CE1AD3314D8E2574E11D73994D0300A06082A8648CE3D040302303E310B3009060355040613024445311A3018060355040A0C11566563746F725F496E666F726D6174696B3113301106035504030C0A554453307832395F4341301E170D3231313131373136333135335A170D3331313131353136333135335A3041310B3009060355040613024445311A3018060355040A0C11566563746F725F496E666F726D6174696B3116301406035504030C0D554453203078323920655054493059301306072A8648CE3D020106082A8648CE3D03010703420004D4C441466D5004C9C85473857E7DA7DB42F41C8698E0B1A32515770BBF8520D1836ED0DFE4469CC95A716C0C56ABCE169F9B744405C9F6D0CF0A805118B8A05AA38183308180301D0603551D0E04160414F38304C5A511A462E7C144C79FC9763799174CFE301F0603551D23041830168014993DA3341C96281A2868EC1296DCE36E967B59CF301D0603551D250416301406082B0601050507030106082B06010505070302300B0603551D0F0404030203883012060B2B0601040182E92E0201010403020104300A06082A8648CE3D0403020349003046022100AA4EE3C5E498D7B2380A6DEA65FFD147519AE545CC27A1BD68945803CEB149D6022100B4A4C64BA8E541D577DF8C1C786EB89D31B0260FCFC942A541FC7938AAAF10AA";

      SoapHexBinary authConfigureShb = SoapHexBinary.Parse("2908"); // Authentication_Authentication_Configure
      ecuBaseController.SendHexService(authConfigureShb.Value);

      SoapHexBinary verifyCertShb = SoapHexBinary.Parse("290100"+"020A"+cert+"0000"); // Authentication_Verify_Certificate_Unidirectional + Length + Certificate + NoChallengeClient
      ecuBaseController.SendHexService(verifyCertShb.Value);

      SoapHexBinary proofOfOwnershipShb = SoapHexBinary.Parse("290300000000"); // Authentication_Proof_Of_Ownership
      ecuBaseController.SendHexService(proofOfOwnershipShb.Value);
    }

    /// <summary>
    ///   Unlocks the diagnostic target, i.e. requests a seed from the diagnostic target, computes the corresponding key and
    ///   sends the key to the diagnostic target.
    /// </summary>
    private void UnlockEcu()
    {
      var ecuBaseController = _mEcu.GetECUBaseController();
      
      ecuBaseController.SendHexService(new List<byte> { 0x10, 0x01 });  // Default_Session_Start
      ecuBaseController.SendHexService(new List<byte> { 0x10, 0x03 });  // ExtendedDiagnosticSession_Start
      Authenticate();

      ecuBaseController.SendHexService(new List<byte> { 0x10, 0x02 });  // ProgrammingSession_Start

      var data = ecuBaseController.SendHexService(new List<byte> { 0x27, 0x01 });  // SeedLevel_0x01_Request

      if (data.Count != 4) return;

      // Calculate key, for simplification computed directly (i.e. not by using the seed & key DLL)
      var seed = (data.ElementAt(2)<<8) + data.ElementAt(3);
      var key = (~(seed & 0xFFFF) & 0xFFFF);
      var byte1 = (byte)(key & 0xFF);
      var byte0 = (byte)((key >> 8) & 0xFF);

      // Send Key
      ecuBaseController.SendHexService(new List<byte> { 0x27, 0x02, byte0, byte1 });
    }

    /// <summary>
    ///   Reads the variant coding of the ECU after unlocking the ECU.
    /// </summary>
    /// <param name="strCountryCode">Returns string with read country code.</param>
    /// <param name="strVehicleType">Returns string with read vehicle type.</param>
    public void ReadVariantCoding(out string strCountryCode, out string strVehicleType)
    {
      strCountryCode = "";
      strVehicleType = "";


      // SECURITY ACCESS -----------------------------------------------------
      UnlockEcu();


      // READ VARIANT CODING -------------------------------------------------
      var variantData = _mEcu.GetVariantData();
      if (variantData==null || variantData.Count == 0)
      {
        MessageBox.Show("ERROR: Variant Data could not be read! (Did the security access fail?)");
      }
      else
      {
        var vehicleTypeAndCountryCode = variantData.ElementAt(0);

        if (vehicleTypeAndCountryCode.RawValue.Count == 0)
        {
          MessageBox.Show("ERROR: Variant Data could not be read!(Did the security access fail ?)");
        }
        else {
          if (vehicleTypeAndCountryCode.Values.ElementAt(1).PhysicalValue is IStringValue countryCode)
          {
            strCountryCode = countryCode.Value;
          }

          if (vehicleTypeAndCountryCode.Values.ElementAt(2).PhysicalValue is IStringValue vehicleType)
          {
            strVehicleType = vehicleType.Value;
          }
        }
      }
    }

    /// <summary>
    ///   Writes the variant coding of the ECU after unlocking the ECU.
    /// </summary>
    /// <param name="sCountryCode">The country code as string to be written.</param>
    /// <param name="sVehicleType">The vehicle type as string to be written.</param>
    public void WriteVariantCoding(string sCountryCode, string sVehicleType)
    {
      // SECURITY ACCESS -----------------------------------------------------
      UnlockEcu();

      // READ AND WRITE VARIANT CODING ---------------------------------------
      var variantCodingDataBeforeWrite = _mEcu.GetVariantData();

      var codingStringDid = variantCodingDataBeforeWrite.First(did => did.DID.Name == "Variant Coding");
      var countryCodeValue = codingStringDid.Values.First(v => v.Path.EndsWith("CountryType"));
      var vehicleTypeValue = codingStringDid.Values.First(v => v.Path.EndsWith("VehicleType"));

      // Change physical value
      var newPhysicalValueCountryCode = _mTestBench.ValueFactory.CreateStringValue(sCountryCode);
      countryCodeValue.PhysicalValue = newPhysicalValueCountryCode;

      var newPhysicalValueVehicleType = _mTestBench.ValueFactory.CreateStringValue(sVehicleType);
      vehicleTypeValue.PhysicalValue = newPhysicalValueVehicleType;
      
      // Write modified variant data back to the ECU
      _mEcu.SetVariantData(new List<IDIDValue> { codingStringDid });


      var variantCodingDataAfterWrite = _mEcu.GetVariantData();

      var codingStringDidAfterWrite = variantCodingDataAfterWrite.First(did => did.DID.Name == "Variant Coding");
      var countryCodeValueAfterWrite = codingStringDidAfterWrite.Values.First(v => v.Path.EndsWith("CountryType"));
      var vehicleTypeValueAfterWrite = codingStringDidAfterWrite.Values.First(v => v.Path.EndsWith("VehicleType"));

      if (!((countryCodeValueAfterWrite.PhysicalValue is IStringValue countryCodeAfterWrite) &&
            (vehicleTypeValueAfterWrite.PhysicalValue is IStringValue vehicleTypeAfterWrite) &&
            (countryCodeValue.PhysicalValue is IStringValue countryCodeBeforeWrite) &&
            (vehicleTypeValue.PhysicalValue is IStringValue vehicleTypeBeforeWrite))) 
      {
        MessageBox.Show("ERROR: Unknown error occurred during writing variant coding!");
        return;
      }

      if ((countryCodeAfterWrite.Value != countryCodeBeforeWrite.Value) ||
          (vehicleTypeAfterWrite.Value != vehicleTypeBeforeWrite.Value))
      {
        MessageBox.Show("ERROR: Writing variant coding failed!");
      }
    }

    /// <summary>
    ///   Initializes the string array containing the fault memory contents with 'iVisibleDataGridRows' rows.
    /// </summary>
    /// <param name="faultMemory">Structure to be initialized.</param>
    public void InitFaultMemContents(out XilApiDialog.FaultMemStruct faultMemory)
    {
      int k;

      faultMemory.ArrContents = new string[_mIVisibleDataGridRows][];
      for (k = 0; k < _mIVisibleDataGridRows; k++)
      {
        faultMemory.ArrContents[k] = new[] { "", "", "", "", "", "", "" };
      }

      faultMemory.StrEnvDataHeaderText = new[] { "Supply Voltage", "Odometer Value" };
    }

    /// <summary>
    ///   Reads the fault memory.
    /// </summary>
    /// <param name="faultMemory">Structure to be filled with fault memory contents.</param>
    public void ReadFaultMemory(out XilApiDialog.FaultMemStruct faultMemory)
    {
      var ecuFaultMemory = _mEcu.GetEcuFaultMemory();
      var faultMemoryContents = ecuFaultMemory.Read(ASAM.XIL.Interfaces.Testbench.DiagPort.Enum.DtcFilterType.eActive);

      InitFaultMemContents(out faultMemory);


      if (faultMemoryContents.Count == 0) MessageBox.Show("Nothing stored in fault memory!");
      else
      {
        int k;

        for (k = 0; k < faultMemoryContents.Count; k++)
        {
          var fault = faultMemoryContents.ElementAt(k);
          var troubleCode = fault.Value;
          var desc = troubleCode.GetDescription();
          var status = troubleCode.GetStatus(); // Status
          var envData = troubleCode.GetEnvironmentDataCollection();
          if ((envData.Last(v => v.Path.EndsWith("SupplyVoltage")).PhysicalValue is IFloatValue supplyVoltage) &&
              (envData.Last(o => o.Path.EndsWith("OdometerValue")).PhysicalValue is IUintValue odometerValue))
          {
            faultMemory.ArrContents[k] = new[] { (k + 1).ToString(), fault.Key.ToString("X6"), troubleCode.GetLongName(), "0x" + status.ToString("X2"), desc, supplyVoltage.Value.ToString("F1"), odometerValue.Value.ToString() };
          }
        }
      }
    }
      
    /// <summary>
    ///   Clears the fault memory.
    /// </summary>
    /// <param name="faultMemory">Structure to be filled with fault memory contents.</param>
    public void ClearFaultMemory(out XilApiDialog.FaultMemStruct faultMemory)
    {
      ReadFaultMemory(out faultMemory);

      var ecuFaultMemory = _mEcu.GetEcuFaultMemory();
      ecuFaultMemory.Clear();
      var faultMemoryContents = ecuFaultMemory.Read(ASAM.XIL.Interfaces.Testbench.DiagPort.Enum.DtcFilterType.eActive);
      if (faultMemoryContents.Count != 0)
      {
          MessageBox.Show("ERROR: Could not clear fault memory!");
      }
      else
      {
          InitFaultMemContents(out faultMemory);
      }
    }
  }
}