using System;
using System.IO;
using System.Windows.Forms;
using CANoeVariant=CANoe;
using Diagnostic;

namespace ExampleDiagnosticsViaCOM
{
  public partial class Diag_COM_Example : Form
  {
    //objects referencing CANoe interface (Vector.CANoe.Interop.dll)
    CANoeVariant.Application mApp;
    CANoeVariant.UI mUI;
    CANoeVariant.Write mWrite;
    CANoeVariant.Measurement mMeas;
    CANoeVariant.CAPL mCapl;
    CANoeVariant.TestConfiguration mTestConfiguration;
    CANoeVariant.Networks mNetworks;
    CANoeVariant.Network mNetwork;
    CANoeVariant.Network tempNetwork;
    CANoeVariant.Devices mDevices;
    CANoeVariant.Devices tempDevices;
    CANoeVariant.Device mDevice;
    CANoeVariant.Device tempDevice;

    //objects referencing Diagnostic interface (Diagnostic.Interop.dll)
    Diagnostic.Diagnostic mDiagnostic;
    Diagnostic.DiagnosticRequest mRequestDefaultSessionStart;
    Diagnostic.DiagnosticRequest mRequestSerialNumber;

    const string mECUQualifier = "DoorFL";
    const string mBusName = "CAN1";
    const string mSampleConfigurationRelPath = "../../../../../";
    const string mSampleConfigurationName = "UDSSystem.cfg";
    byte[] rawRequestSerialNumberRead = {0x22, 0xF1, 0x8C};
    byte[] rawRequestDefaultSessionStart = {0x10, 0x01};

    CANoeVariant.eVerdictState gCurrentVerdict;

    TreeViewEventArgs lastSelectionTreeEvent=null;

    void initCANoe()
    {
      mApp = new CANoeVariant.Application();
      mApp.OnQuit += new CANoeVariant._IApplicationEvents_OnQuitEventHandler(mApp_OnQuit);
      System.Threading.Thread.Sleep(2000);

      mUI = (CANoeVariant.UI)mApp.UI;
      mWrite = (CANoeVariant.Write)mUI.Write;

      OpenConfig(mSampleConfigurationName);

      mMeas = (CANoeVariant.Measurement)mApp.Measurement;
      if (!mMeas.Running)
      {
        mCapl = (CANoeVariant.CAPL)mApp.CAPL;
        mCapl.Compile("");
        mMeas.Start();
      }

      OutputVerdict("<No verdict>", System.Drawing.Color.DimGray, System.Drawing.Color.White);

      mTestConfiguration = (CANoeVariant.TestConfiguration)mApp.Configuration.TestConfigurations[1];
      if (mTestConfiguration != null)
      {
        mTestConfiguration.OnStart += new CANoeVariant._ITestConfigurationEvents_OnStartEventHandler(tcEvent_OnStart);
        mTestConfiguration.OnStop += new CANoeVariant._ITestConfigurationEvents_OnStopEventHandler(tcEvent_OnStop);
        mTestConfiguration.OnVerdictChanged += new CANoeVariant._ITestConfigurationEvents_OnVerdictChangedEventHandler(tcEvent_OnVerdictChanged);
        mTestConfiguration.OnVerdictFail += new CANoeVariant._ITestConfigurationEvents_OnVerdictFailEventHandler(tcEvent_OnVerdictFail);
      }
    }

    void initDeviceTree()
    {
      mNetworks = (CANoeVariant.Networks)mApp.Networks;

      networksTreeView.BeginUpdate();

      for (int i = 0; i < mNetworks.Count; i++)
      {
        tempNetwork = (CANoeVariant.Network)mNetworks[i + 1];
        tempDevices = (CANoeVariant.Devices)tempNetwork.Devices;

        networksTreeView.Nodes.Add(tempNetwork.Name);

        for (int k = 0; k < tempDevices.Count; k++)
        {
          tempDevice = (CANoeVariant.Device)tempDevices[k + 1];
          try
          {
            Diagnostic.Diagnostic a = tempDevice.Diagnostic;                  // Only add diagnostic devices
            networksTreeView.Nodes[i].Nodes.Add(tempDevice.Name);
          }
          catch
          {
          }
        }
      }
      networksTreeView.Nodes[0].Expand();

      networksTreeView.EndUpdate();
    }

    void deInitDiagHandlers(TreeViewEventArgs e)
    {
      if (mDiagnostic == null)
        return;

      try
      {
        mRequestDefaultSessionStart.OnResponse -= reqDefaultSessionStart_OnResponse;
      }
      catch
      {
        mRequestDefaultSessionStart.OnResponse -= reqByteStream_OnResponse;
      }

      try
      {
        mRequestSerialNumber.OnResponse -= reqReadSerialNumber_OnResponse;
      }
      catch
      {
        mRequestSerialNumber.OnResponse -= reqByteStream_OnResponse;
      }

      mRequestDefaultSessionStart.OnConfirmation -= req_OnConfirmation;
      mRequestSerialNumber.OnConfirmation -= req_OnConfirmation;
    }

    void initDiagHandlers(TreeViewEventArgs e)
    {
      if (mNetworks == null)
        return;

      if (e.Node.Parent == null)
        return;

      string networkName = e.Node.Parent.Text;

      mNetwork = (CANoeVariant.Network)mApp.Networks[networkName];
      if (mNetwork == null)
        return;

      mDevices = (CANoeVariant.Devices)mNetwork.Devices;
      if (mDevices == null)
        return;

      string ecuQualifier = e.Node.Text;

      mDevice = (CANoeVariant.Device)mDevices[ecuQualifier];
      if (mDevice == null)
        return;

      mDiagnostic = (Diagnostic.Diagnostic)mDevice.Diagnostic;

      if (mDiagnostic == null)
        return;

      // create symbolic request and assign corresponding handlers
      try
      {
        mRequestDefaultSessionStart = (Diagnostic.DiagnosticRequest)mDiagnostic.CreateRequest("DefaultSession_Start");
        mRequestDefaultSessionStart.OnResponse += new Diagnostic._IDiagnosticRequestEvents_OnResponseEventHandler(reqDefaultSessionStart_OnResponse);
      }
      catch // If Service is named differently in diagnostic description, send out a raw request
      {
        mRequestDefaultSessionStart = mDiagnostic.CreateRequestFromStream(rawRequestDefaultSessionStart);
        mRequestDefaultSessionStart.OnResponse += new Diagnostic._IDiagnosticRequestEvents_OnResponseEventHandler(reqByteStream_OnResponse);
      }

      try
      {
        mRequestSerialNumber = (Diagnostic.DiagnosticRequest)mDiagnostic.CreateRequest("SerialNumber_Read");
        mRequestSerialNumber.OnResponse += new Diagnostic._IDiagnosticRequestEvents_OnResponseEventHandler(reqReadSerialNumber_OnResponse);
      }
      catch // If Service is named differently in diagnostic description, send out a raw request
      {
        mRequestSerialNumber = mDiagnostic.CreateRequestFromStream(rawRequestSerialNumberRead);
        mRequestSerialNumber.OnResponse += new Diagnostic._IDiagnosticRequestEvents_OnResponseEventHandler(reqByteStream_OnResponse);
      }

      mRequestDefaultSessionStart.OnConfirmation += new Diagnostic._IDiagnosticRequestEvents_OnConfirmationEventHandler(req_OnConfirmation);
      mRequestSerialNumber.OnConfirmation += new Diagnostic._IDiagnosticRequestEvents_OnConfirmationEventHandler(req_OnConfirmation);
    }


    // Get the full pathname from relative path and filename or return null if it does not exist
    string GetFullName(string relpath, string configName)
    {
      FileInfo fi1 = new FileInfo(relpath + configName);

      if (fi1 != null && fi1.Exists)
      {
          return fi1.FullName;
      }

      return null;
    }

    // Open the specified config (if it isn't open already)
    void OpenConfig(string configName)
    {
	  string FullName = GetFullName(mSampleConfigurationRelPath, configName);
      if (FullName != null)
      {
        if (FullName != mApp.Configuration.FullName)
        {
          mApp.Configuration.Modified = false;
          mApp.Open(FullName, false, false);

          OutputText("Successfully opened '" + FullName + "'!"); 
        }
      }
      else
      {
        MessageBox.Show("Could not find the configuration file '" + mSampleConfigurationRelPath + configName + "'!", "Hint", MessageBoxButtons.OK);
      }
    }

    public Diag_COM_Example()
    {
      InitializeComponent();

      try
      {
        initCANoe();
        initDeviceTree();
        disableSendFunctions();
      }
      catch (System.Runtime.InteropServices.COMException e)
      {
        MessageBox.Show(e.Message.ToString(), "Exception", MessageBoxButtons.OK);
        System.Environment.Exit(1);
      }
    }

    // The access of Windows Forms Controls is not thread safe
    // ==> as the diagnostic handlers are called in the CANoe/CANoe4SW thread, use "Invoke" method to switch to main thread

    delegate void OutputTextDelegate(String text);

    void OutputText(String text)
    {
      if (text == null)
      {
        throw new ArgumentNullException("s");
      }

      if (tbResult.InvokeRequired)
      {
        OutputTextDelegate outputTextDelegate = new OutputTextDelegate(OutputText);

        Invoke(outputTextDelegate, new Object[] { text });
      }
      else
      {
        if (tbResult.Text == "")
        {
          tbResult.Text = text;
        }
        else
        {
          tbResult.Text += System.Environment.NewLine + text;
          tbResult.SelectionStart = tbResult.TextLength; // Set Caret to end of text
          tbResult.ScrollToCaret();
        }
      }
    }

    delegate void OutputSerialNumberDelegate(String serialNumber);

    void OutputSerialNumber(String serialNumber)
    {
      if (serialNumber == null)
      {
        throw new ArgumentNullException("s");
      }

      if (tbSerialNumber.InvokeRequired)
      {
        OutputSerialNumberDelegate outputSerialNumberDelegate = new OutputSerialNumberDelegate(OutputSerialNumber);

        Invoke(outputSerialNumberDelegate, new Object[] { serialNumber });
      }
      else
      {
        tbSerialNumber.Text = serialNumber;
      }
    }

    delegate void OutputVerdictDelegate(String verdict, System.Drawing.Color foreColor, System.Drawing.Color backColor);

    void OutputVerdict(String verdict, System.Drawing.Color foreColor, System.Drawing.Color backColor)
    {
      if (verdict == null)
      {
        throw new ArgumentNullException("s");
      }

      if (tbVerdict.InvokeRequired)
      {
        OutputVerdictDelegate outputVerdictDelegate = new OutputVerdictDelegate(OutputVerdict);

        Invoke(outputVerdictDelegate, new Object[] { verdict, foreColor, backColor });
      }
      else
      {
        tbVerdict.Text = verdict;
        tbVerdict.ForeColor = foreColor;
        tbVerdict.BackColor = backColor;
      }
    }

    private void SendRequestAndHandleResponses(Diagnostic.DiagnosticRequest req)
    {
      // put request in queue
      try
      {
        req.Send(true);
      }
      catch (System.Runtime.InteropServices.COMException e)
      {
        MessageBox.Show(e.Message.ToString(), "Exception", MessageBoxButtons.OK);
        MessageBox.Show("Probably could not send the request. Did you stop measurement?", "Hint", MessageBoxButtons.OK);
      }
    }

    void req_OnConfirmation()
    {
      OutputText("Request successfully sent!");
    }

    void outputSessionResponseParams(string sender, string sessionType, int P2, int P2Ex)
    {
      OutputText("Positive Response from " + sender +
                                 ", Type=" + sessionType +
                                   ", P2=" + P2.ToString() +
                                 ", P2Ex=" + P2Ex.ToString());
    }

    void reqDefaultSessionStart_OnResponse(Object response)
    {
      Diagnostic.DiagnosticResponse mResponse = (Diagnostic.DiagnosticResponse)response;
      if (mResponse.Positive)
      {
        string sessionType = mResponse.GetParameter("DiagSessionType", Diagnostic.eValueType.cSymbolicValue);

        if (sessionType == null) // In case parameter is named differently in diagnostic description
        {
          OutputText("Parameter 'DiagSessionType' not found, deriving from raw values!");
          switch ((byte)mResponse.Stream[1]) 
          {
            case 0x81:
            case 0x85:
              sessionType = String.Format("0x{0:X2}", (byte)mResponse.Stream[1]);
              OutputText("Positive Response received, Type=" + sessionType);
              break;
            default:
              OutputText(String.Format("Unknown session type, type=0x{0:X2}", (byte)mResponse.Stream[1]));
              break;
          }
        }
        else 
        {
          string sender = mResponse.Sender.ToString();

          int P2 = Convert.ToInt32(mResponse.GetParameter("P2"));
          int P2Ex = Convert.ToInt32(mResponse.GetParameter("P2Ex"));

          outputSessionResponseParams(sender, sessionType, P2, P2Ex);
        }
      }
      else
      {
        OutputText("Negative Response received, NRC=0x" + mResponse.ResponseCode.ToString("X02"));
      }
    }

    void reqReadSerialNumber_OnResponse(Object response)
    {
      Diagnostic.DiagnosticResponse mResponse = (Diagnostic.DiagnosticResponse)response;
      if (mResponse.Positive)
      {
        string serialNumber;

        serialNumber = mResponse.GetParameter("SerialNumber");
        if (serialNumber != null)
        {
          OutputText("Positive Response from " + mResponse.Sender.ToString() +
                            ", serial number=" + serialNumber);
          OutputSerialNumber(serialNumber);
        }
      }
      else
      {
        OutputText("Negative Response received, NRC=0x" + mResponse.ResponseCode.ToString("X02"));
        OutputSerialNumber("<negative Response>");
      }
    }

    void reqByteStream_OnResponse(Object response)
    {
      Diagnostic.DiagnosticResponse mResponse = (Diagnostic.DiagnosticResponse)response;
      if (mResponse.Positive)
      {
        switch ((byte)mResponse.Stream[0])
        {
          case 0x50:
            {
              string sessionType = String.Format("0x{0:X2}", (byte)mResponse.Stream[1]);
              int P2 = (((int)mResponse.Stream[2]) << 8) + mResponse.Stream[3];
              int P2Ex = (((int)mResponse.Stream[4]) << 8) + mResponse.Stream[5];
              outputSessionResponseParams(mResponse.Sender.ToString(), sessionType, P2, P2Ex * 10); // P2Ex derived from formula
            }
            break;
          case 0x62:
            {
              int iSerialNumber = 0;
              for (int i = 3; i < 7; i++)
              {
                iSerialNumber = (iSerialNumber << 8) + mResponse.Stream[i];
              }
              OutputText("Positive Response from " + mResponse.Sender.ToString() +
                         ", serial number=" + iSerialNumber.ToString());
                         OutputSerialNumber(iSerialNumber.ToString());
            }
            break;
          default:
            OutputText(string.Format("Unknown positive Response from {0:s} (raw)!", mResponse.Sender.ToString()));
            break;
        }
      }
      else
      {
        OutputText(string.Format("Negative Response from {0:s} (raw), NRC=0x{1:X02}", mResponse.Sender.ToString(), mResponse.ResponseCode));
      }
    }

    void tcEvent_OnStart()
    {
      OutputText("Test started!");
      gCurrentVerdict = CANoeVariant.eVerdictState.cVerdictNone;
      OutputVerdict("Running", System.Drawing.Color.Green, System.Drawing.Color.White);
    }

    void tcEvent_OnStop(CANoeVariant.eStopReason reason)
    {
      OutputText("Test stopped, Reason: "+reason.ToString());
      if (reason == CANoeVariant.eStopReason.cStopReasonEnd)
      {
        switch (gCurrentVerdict) 
        {
          case CANoeVariant.eVerdictState.cVerdictPassed:
            OutputVerdict("Passed", System.Drawing.Color.Black, System.Drawing.Color.ForestGreen);
            break;
          case CANoeVariant.eVerdictState.cVerdictErrorInTestSystem:
            OutputVerdict("Error in Test System", System.Drawing.Color.White, System.Drawing.Color.DarkRed);
            break;
          case CANoeVariant.eVerdictState.cVerdictFailed:
          default:
            OutputVerdict("Failed", System.Drawing.Color.Black, System.Drawing.Color.Red);
            break;
        }
      }
    }

    void tcEvent_OnVerdictChanged(CANoeVariant.eVerdictState verdict)
    {
      OutputText("Verdict changed, new verdict: " + verdict.ToString());
      gCurrentVerdict = verdict;
      if (verdict == CANoeVariant.eVerdictState.cVerdictPassed)
      {
        OutputVerdict("Running", System.Drawing.Color.ForestGreen, System.Drawing.Color.White);
      }
      else
      {
        OutputVerdict("Running", System.Drawing.Color.Red, System.Drawing.Color.White);
      }
    }

    void tcEvent_OnVerdictFail()
    {
      gCurrentVerdict = CANoeVariant.eVerdictState.cVerdictFailed;
      OutputText("Test failed!");
    }

    void mApp_OnQuit()
    {
      // clean up
      mDevices = null;
      mDevice = null;
      mNetwork = null;
      tempNetwork = null;
      mDiagnostic = null;
      mCapl = null;
      mMeas = null;
      mApp = null;
    }

    void enableSendFunctions()
    {
      btnReadSwVersion.Enabled = true;
      btnDefaultSessionStart.Enabled = true;
    }

    void disableSendFunctions()
    {
      btnReadSwVersion.Enabled = false;
      btnDefaultSessionStart.Enabled = false;
    }

    private void networksTreeView_AfterSelect(object sender, TreeViewEventArgs e)
    {
      string nodeText = e.Node.Text;

      if (lastSelectionTreeEvent != null)
      {
        deInitDiagHandlers(lastSelectionTreeEvent);
      }

      if (e.Node.Parent != null) // if node has a parent, i.e. is no network
      {
        OutputText("Selected ECU '" + nodeText + "'!");
        initDiagHandlers(e);
        enableSendFunctions();
      }
      else
      {
        OutputText("Selected Network '" + nodeText + "'!");
        disableSendFunctions();
      }

      lastSelectionTreeEvent = e;
    }

    private void btnClose_Click(object sender, EventArgs e)
    {
      System.Windows.Forms.Application.Exit();
    }

    private void btnReadSwVersion_Click(object sender, EventArgs e)
    {
      if (mDiagnostic != null)
      {
        SendRequestAndHandleResponses(mRequestSerialNumber);
      }
    }

    private void btnExecuteDiagTest_Click(object sender, EventArgs e)
    {
      if (mTestConfiguration != null)
      {
        OutputText("Starting Diag Test...");
        mTestConfiguration.Start();
      } 
    }

    private void btnDefaultSessionStart_Click(object sender, EventArgs e)
    {
      if (mDiagnostic != null)
      {
        SendRequestAndHandleResponses(mRequestDefaultSessionStart);
      }
    }

    private void btnClear_Click(object sender, EventArgs e)
    {
      tbResult.Text = "";
    }
  }
}
