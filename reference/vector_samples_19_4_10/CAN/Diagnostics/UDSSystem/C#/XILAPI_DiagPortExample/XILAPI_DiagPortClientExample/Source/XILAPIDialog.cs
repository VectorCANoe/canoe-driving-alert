/*---------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
---------------------------------------------------------------------------*/

#region Usings

using System;
using System.Linq;
using System.Windows.Forms;

#endregion

namespace XILAPI_DiagPortClientExample.Source
{
  public partial class XilApiDialog : Form
  {
    #region Configuration Strings

    private const string ConfigVendorName = "Vector";

#if X86
    private const string ConfigProductName = "CANoe32"; // This XIL API Diagnostic Port Example application is a 32bit application.
    private const string ConfigBitness = "32 bit";
#else
    private const string ConfigProductName = "CANoe64"; // This XIL API Diagnostic Port Example application is a 64bit application.
    private const string ConfigBitness = "64 bit";
#endif

    // Version of the XIL API assemblies depends on the chosen configuration
#if XIL_API_2_2_0
    private const string ConfigProductVersion = "2.2.0"; 
#else
    private const string ConfigProductVersion = "2.1.0";
#endif
    private const string ConfigDiagnosticPortConfig = "../../../../XIL API Configuration/VectorDiagPortConfig.xml";

    private const string ConfigDiagnosticTarget = "DoorFL";

#endregion
	
#region Members

    private readonly XilApiClient _mXil;

#endregion
	
    /// <summary>
    ///   Visible data grid rows for fault memory display (necessary for initializing faultMemory structure)
    /// </summary>
    private const int CiNumberOfVisibleDataGridRows = 6;

    /// <summary>
    ///   Fault memory contents structure
    /// </summary>
    public struct FaultMemStruct
    {
      public string[][] ArrContents;
      public string[] StrEnvDataHeaderText;
    }

    private FaultMemStruct _mFaultMemory;

    /// <summary>
    ///   Shows the example dialog and starts the XIL API client
    /// </summary>
    public XilApiDialog()
    {
      InitializeComponent();
      gbActiveWhenConnected.Enabled = false;
      _mXil = new XilApiClient(out _mFaultMemory, CiNumberOfVisibleDataGridRows);
    }

    /// <summary>
    ///   Called when [load].
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="EventArgs" /> instance containing the event data.</param>
    private void OnLoad(object sender, EventArgs e)
    {
      // Initialize data grid and combo boxes
      FillDataGrid();
      BasedOnXilApiVersionLabel.Text = "Based on XIL API Version " + ConfigProductVersion + " (" + ConfigBitness + ")";
      cbCountryCode.SelectedIndex = 0;
      cbVehicleType.SelectedIndex = 0;
    }
	
	  /// <summary>
    ///   Called when [form closing].
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="FormClosingEventArgs" /> instance containing the event data.</param>
    private void OnFormClosing(object sender, FormClosingEventArgs e)
    {
      if (_mXil.IsConnected)
        _mXil.Shutdown();
    }

    /// <summary>
    ///   Fills the data grid with contents of _mFaultMemory
    /// </summary>
    private void FillDataGrid()
    {
      int k;

      dgrdFaultMemory.EnableHeadersVisualStyles = false;
      dgrdFaultMemory.ColumnHeadersBorderStyle = DataGridViewHeaderBorderStyle.Single;

      dgrdFaultMemory.RowHeadersVisible = false;
      foreach (DataGridViewColumn col in dgrdFaultMemory.Columns)
      {
        col.SortMode = DataGridViewColumnSortMode.NotSortable;
      }

      dgrdFaultMemory.Rows.Clear();
      for (k = 0; k < CiNumberOfVisibleDataGridRows; k++)
      {
        dgrdFaultMemory.Rows.Add(_mFaultMemory.ArrContents[k].ToArray<object>());
      }

      dgrdFaultMemory.Columns[5].HeaderText = _mFaultMemory.StrEnvDataHeaderText[0];
      dgrdFaultMemory.Columns[6].HeaderText = _mFaultMemory.StrEnvDataHeaderText[1];
    }

    /// <summary>
    ///   Connects to CANoe
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="EventArgs" /> instance containing the event data.</param>
    private void BtnConnect_Click(object sender, EventArgs e)
    {
      try
      {
        _mXil.Init(ConfigVendorName, ConfigProductName, ConfigProductVersion, ConfigDiagnosticPortConfig, ConfigDiagnosticTarget);

        btnConnect.Enabled = false;
        btnDisconnect.Enabled = true;
        gbActiveWhenConnected.Enabled = true;
      }
      catch (Exception ex)
      {
        MessageBox.Show(ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
      }
    }

    /// <summary>
    ///   Disconnects from CANoe
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="EventArgs" /> instance containing the event data.</param>
    private void BtnDisconnect_Click(object sender, EventArgs e)
    {
      _mXil.Shutdown();
      btnConnect.Enabled = true;
      btnDisconnect.Enabled = false;
      gbActiveWhenConnected.Enabled = false;
      tbSerialNumber.Text = "";
    }

    /// <summary>
    ///   Reads the serial number of the diagnostic target
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="EventArgs" /> instance containing the event data.</param>
    private void BtnReadSerialNo_Click(object sender, EventArgs e)
    {
      _mXil.ReadSerialNumber(out var strSerialNumber);
      tbSerialNumber.Text = strSerialNumber;
    }

    /// <summary>
    ///   Reads the variant coding information from the diagnostic target
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="EventArgs" /> instance containing the event data.</param>
    private void BtnReadVariantCoding_Click(object sender, EventArgs e)
    {
      _mXil.ReadVariantCoding(out var strCountryCode, out var strVehicleType);
      if ("" != strCountryCode) cbCountryCode.Text = strCountryCode;
      if ("" != strVehicleType) cbVehicleType.Text = strVehicleType;
    }

    /// <summary>
    ///   Writes the variant coding information to the diagnostic target
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="EventArgs" /> instance containing the event data.</param>
    private void BtnWriteVariantCoding_Click(object sender, EventArgs e)
    {
      _mXil.WriteVariantCoding(cbCountryCode.Text, cbVehicleType.Text);
    }

    /// <summary>
    ///   Reads the fault memory contents from the diagnostic target
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="EventArgs" /> instance containing the event data.</param>
    private void BtnReadFaultMemory_Click(object sender, EventArgs e)
    {
      _mXil.ReadFaultMemory(out _mFaultMemory);
      FillDataGrid();
    }
	
    /// <summary>
    ///   Clears the fault memory contents on the diagnostic target
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="EventArgs" /> instance containing the event data.</param>
    private void BtnClearFaultMemory_Click(object sender, EventArgs e)
    {
      _mXil.ClearFaultMemory(out _mFaultMemory);
      FillDataGrid();
    }
  }
}
