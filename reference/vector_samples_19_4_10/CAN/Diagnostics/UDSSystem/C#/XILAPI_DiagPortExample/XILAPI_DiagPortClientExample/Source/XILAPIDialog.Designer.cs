/*---------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
---------------------------------------------------------------------------*/

namespace XILAPI_DiagPortClientExample.Source
{
    partial class XilApiDialog
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
      this.btnReadSerialNo = new System.Windows.Forms.Button();
      this.btnConnect = new System.Windows.Forms.Button();
      this.btnDisconnect = new System.Windows.Forms.Button();
      this.tbSerialNumber = new System.Windows.Forms.TextBox();
      this.btnPerformDiagSequence = new System.Windows.Forms.Button();
      this.gbActiveWhenConnected = new System.Windows.Forms.GroupBox();
      this.groupBox3 = new System.Windows.Forms.GroupBox();
      this.groupBox2 = new System.Windows.Forms.GroupBox();
      this.BasedOnXilApiVersionLabel = new System.Windows.Forms.Label();
      this.button1 = new System.Windows.Forms.Button();
      this.dgrdFaultMemory = new System.Windows.Forms.DataGridView();
      this.gbVariantCoding = new System.Windows.Forms.GroupBox();
      this.btnReadVariantCoding = new System.Windows.Forms.Button();
      this.cbCountryCode = new System.Windows.Forms.ComboBox();
      this.btnWriteVariantCoding = new System.Windows.Forms.Button();
      this.cbVehicleType = new System.Windows.Forms.ComboBox();
      this.label3 = new System.Windows.Forms.Label();
      this.label4 = new System.Windows.Forms.Label();
      this.colIndex = new System.Windows.Forms.DataGridViewTextBoxColumn();
      this.colDTC = new System.Windows.Forms.DataGridViewTextBoxColumn();
      this.colLongName = new System.Windows.Forms.DataGridViewTextBoxColumn();
      this.colStatus = new System.Windows.Forms.DataGridViewTextBoxColumn();
      this.colDescription = new System.Windows.Forms.DataGridViewTextBoxColumn();
      this.colEnvDataValue1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
      this.colEnvDataValue2 = new System.Windows.Forms.DataGridViewTextBoxColumn();
      this.Column1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
      this.gbActiveWhenConnected.SuspendLayout();
      this.groupBox3.SuspendLayout();
      this.groupBox2.SuspendLayout();
      ((System.ComponentModel.ISupportInitialize)(this.dgrdFaultMemory)).BeginInit();
      this.gbVariantCoding.SuspendLayout();
      this.SuspendLayout();
      // 
      // btnReadSerialNo
      // 
      this.btnReadSerialNo.Location = new System.Drawing.Point(6, 19);
      this.btnReadSerialNo.Name = "btnReadSerialNo";
      this.btnReadSerialNo.Size = new System.Drawing.Size(77, 23);
      this.btnReadSerialNo.TabIndex = 0;
      this.btnReadSerialNo.Text = "Read";
      this.btnReadSerialNo.UseVisualStyleBackColor = true;
      this.btnReadSerialNo.Click += new System.EventHandler(this.BtnReadSerialNo_Click);
      // 
      // btnConnect
      // 
      this.btnConnect.Location = new System.Drawing.Point(28, 12);
      this.btnConnect.Name = "btnConnect";
      this.btnConnect.Size = new System.Drawing.Size(134, 23);
      this.btnConnect.TabIndex = 1;
      this.btnConnect.Text = "Connect";
      this.btnConnect.UseVisualStyleBackColor = true;
      this.btnConnect.Click += new System.EventHandler(this.BtnConnect_Click);
      // 
      // btnDisconnect
      // 
      this.btnDisconnect.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
      this.btnDisconnect.Enabled = false;
      this.btnDisconnect.Location = new System.Drawing.Point(453, 12);
      this.btnDisconnect.Name = "btnDisconnect";
      this.btnDisconnect.Size = new System.Drawing.Size(134, 23);
      this.btnDisconnect.TabIndex = 2;
      this.btnDisconnect.Text = "Disconnect";
      this.btnDisconnect.UseVisualStyleBackColor = true;
      this.btnDisconnect.Click += new System.EventHandler(this.BtnDisconnect_Click);
      // 
      // tbSerialNumber
      // 
      this.tbSerialNumber.BackColor = System.Drawing.SystemColors.ControlLightLight;
      this.tbSerialNumber.Location = new System.Drawing.Point(89, 19);
      this.tbSerialNumber.Name = "tbSerialNumber";
      this.tbSerialNumber.ReadOnly = true;
      this.tbSerialNumber.Size = new System.Drawing.Size(77, 20);
      this.tbSerialNumber.TabIndex = 3;
      // 
      // btnPerformDiagSequence
      // 
      this.btnPerformDiagSequence.Location = new System.Drawing.Point(7, 19);
      this.btnPerformDiagSequence.Name = "btnPerformDiagSequence";
      this.btnPerformDiagSequence.Size = new System.Drawing.Size(77, 23);
      this.btnPerformDiagSequence.TabIndex = 4;
      this.btnPerformDiagSequence.Text = "Read";
      this.btnPerformDiagSequence.UseVisualStyleBackColor = true;
      this.btnPerformDiagSequence.Click += new System.EventHandler(this.BtnReadFaultMemory_Click);
      // 
      // gbActiveWhenConnected
      // 
      this.gbActiveWhenConnected.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.gbActiveWhenConnected.Controls.Add(this.groupBox3);
      this.gbActiveWhenConnected.Controls.Add(this.groupBox2);
      this.gbActiveWhenConnected.Controls.Add(this.gbVariantCoding);
      this.gbActiveWhenConnected.Location = new System.Drawing.Point(-1, 45);
      this.gbActiveWhenConnected.Name = "gbActiveWhenConnected";
      this.gbActiveWhenConnected.Size = new System.Drawing.Size(613, 384);
      this.gbActiveWhenConnected.TabIndex = 5;
      this.gbActiveWhenConnected.TabStop = false;
      // 
      // groupBox3
      // 
      this.groupBox3.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.groupBox3.Controls.Add(this.btnReadSerialNo);
      this.groupBox3.Controls.Add(this.tbSerialNumber);
      this.groupBox3.Location = new System.Drawing.Point(10, 19);
      this.groupBox3.Name = "groupBox3";
      this.groupBox3.Size = new System.Drawing.Size(597, 58);
      this.groupBox3.TabIndex = 20;
      this.groupBox3.TabStop = false;
      this.groupBox3.Text = "Serial Number";
      // 
      // groupBox2
      // 
      this.groupBox2.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.groupBox2.Controls.Add(this.BasedOnXilApiVersionLabel);
      this.groupBox2.Controls.Add(this.button1);
      this.groupBox2.Controls.Add(this.btnPerformDiagSequence);
      this.groupBox2.Controls.Add(this.dgrdFaultMemory);
      this.groupBox2.Location = new System.Drawing.Point(13, 143);
      this.groupBox2.Name = "groupBox2";
      this.groupBox2.Size = new System.Drawing.Size(591, 235);
      this.groupBox2.TabIndex = 19;
      this.groupBox2.TabStop = false;
      this.groupBox2.Text = "Fault Memory";
      // 
      // BasedOnXilApiVersionLabel
      // 
      this.BasedOnXilApiVersionLabel.AutoSize = true;
      this.BasedOnXilApiVersionLabel.Location = new System.Drawing.Point(4, 218);
      this.BasedOnXilApiVersionLabel.Name = "BasedOnXilApiVersionLabel";
      this.BasedOnXilApiVersionLabel.Size = new System.Drawing.Size(152, 13);
      this.BasedOnXilApiVersionLabel.TabIndex = 10;
      this.BasedOnXilApiVersionLabel.Text = "Based on XIL API version x.x.x";
      // 
      // button1
      // 
      this.button1.Location = new System.Drawing.Point(90, 19);
      this.button1.Name = "button1";
      this.button1.Size = new System.Drawing.Size(75, 23);
      this.button1.TabIndex = 5;
      this.button1.Text = "Clear";
      this.button1.UseVisualStyleBackColor = true;
      this.button1.Click += new System.EventHandler(this.BtnClearFaultMemory_Click);
      // 
      // dgrdFaultMemory
      // 
      this.dgrdFaultMemory.AllowUserToAddRows = false;
      this.dgrdFaultMemory.AllowUserToDeleteRows = false;
      this.dgrdFaultMemory.AllowUserToResizeRows = false;
      this.dgrdFaultMemory.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.dgrdFaultMemory.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
      this.dgrdFaultMemory.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.colIndex,
            this.colDTC,
            this.colLongName,
            this.colStatus,
            this.colDescription,
            this.colEnvDataValue1,
            this.colEnvDataValue2,
            this.Column1});
      this.dgrdFaultMemory.Location = new System.Drawing.Point(7, 58);
      this.dgrdFaultMemory.Margin = new System.Windows.Forms.Padding(3, 300, 3, 3);
      this.dgrdFaultMemory.Name = "dgrdFaultMemory";
      this.dgrdFaultMemory.ReadOnly = true;
      this.dgrdFaultMemory.Size = new System.Drawing.Size(578, 155);
      this.dgrdFaultMemory.TabIndex = 9;
      // 
      // gbVariantCoding
      // 
      this.gbVariantCoding.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.gbVariantCoding.Controls.Add(this.btnReadVariantCoding);
      this.gbVariantCoding.Controls.Add(this.cbCountryCode);
      this.gbVariantCoding.Controls.Add(this.btnWriteVariantCoding);
      this.gbVariantCoding.Controls.Add(this.cbVehicleType);
      this.gbVariantCoding.Controls.Add(this.label3);
      this.gbVariantCoding.Controls.Add(this.label4);
      this.gbVariantCoding.Location = new System.Drawing.Point(10, 83);
      this.gbVariantCoding.Name = "gbVariantCoding";
      this.gbVariantCoding.Size = new System.Drawing.Size(597, 54);
      this.gbVariantCoding.TabIndex = 18;
      this.gbVariantCoding.TabStop = false;
      this.gbVariantCoding.Text = "Variant Coding";
      // 
      // btnReadVariantCoding
      // 
      this.btnReadVariantCoding.Location = new System.Drawing.Point(6, 20);
      this.btnReadVariantCoding.Name = "btnReadVariantCoding";
      this.btnReadVariantCoding.Size = new System.Drawing.Size(77, 23);
      this.btnReadVariantCoding.TabIndex = 14;
      this.btnReadVariantCoding.Text = "Read";
      this.btnReadVariantCoding.UseVisualStyleBackColor = true;
      this.btnReadVariantCoding.Click += new System.EventHandler(this.BtnReadVariantCoding_Click);
      // 
      // cbCountryCode
      // 
      this.cbCountryCode.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
      this.cbCountryCode.FormattingEnabled = true;
      this.cbCountryCode.Items.AddRange(new object[] {
            "Europe",
            "USA",
            "Japan"});
      this.cbCountryCode.Location = new System.Drawing.Point(464, 22);
      this.cbCountryCode.Name = "cbCountryCode";
      this.cbCountryCode.Size = new System.Drawing.Size(100, 21);
      this.cbCountryCode.TabIndex = 17;
      // 
      // btnWriteVariantCoding
      // 
      this.btnWriteVariantCoding.Location = new System.Drawing.Point(89, 19);
      this.btnWriteVariantCoding.Name = "btnWriteVariantCoding";
      this.btnWriteVariantCoding.Size = new System.Drawing.Size(77, 23);
      this.btnWriteVariantCoding.TabIndex = 15;
      this.btnWriteVariantCoding.Text = "Write";
      this.btnWriteVariantCoding.UseVisualStyleBackColor = true;
      this.btnWriteVariantCoding.Click += new System.EventHandler(this.BtnWriteVariantCoding_Click);
      // 
      // cbVehicleType
      // 
      this.cbVehicleType.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
      this.cbVehicleType.FormattingEnabled = true;
      this.cbVehicleType.Items.AddRange(new object[] {
            "Coupe",
            "Sedan",
            "Transporter"});
      this.cbVehicleType.Location = new System.Drawing.Point(267, 22);
      this.cbVehicleType.Name = "cbVehicleType";
      this.cbVehicleType.Size = new System.Drawing.Size(100, 21);
      this.cbVehicleType.TabIndex = 16;
      // 
      // label3
      // 
      this.label3.AutoSize = true;
      this.label3.Location = new System.Drawing.Point(193, 25);
      this.label3.Name = "label3";
      this.label3.Size = new System.Drawing.Size(68, 13);
      this.label3.TabIndex = 10;
      this.label3.Text = "Vehicle type:";
      // 
      // label4
      // 
      this.label4.AutoSize = true;
      this.label4.Location = new System.Drawing.Point(384, 25);
      this.label4.Name = "label4";
      this.label4.Size = new System.Drawing.Size(74, 13);
      this.label4.TabIndex = 11;
      this.label4.Text = "Country Code:";
      // 
      // colIndex
      // 
      this.colIndex.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.ColumnHeader;
      this.colIndex.HeaderText = "#";
      this.colIndex.Name = "colIndex";
      this.colIndex.ReadOnly = true;
      this.colIndex.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.NotSortable;
      this.colIndex.Width = 20;
      // 
      // colDTC
      // 
      this.colDTC.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.None;
      this.colDTC.HeaderText = "DTC";
      this.colDTC.Name = "colDTC";
      this.colDTC.ReadOnly = true;
      this.colDTC.Width = 54;
      // 
      // colLongName
      // 
      this.colLongName.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.None;
      this.colLongName.HeaderText = "SAE code";
      this.colLongName.Name = "colLongName";
      this.colLongName.ReadOnly = true;
      this.colLongName.Width = 80;
      // 
      // colStatus
      // 
      this.colStatus.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.None;
      this.colStatus.HeaderText = "Status";
      this.colStatus.Name = "colStatus";
      this.colStatus.ReadOnly = true;
      this.colStatus.Width = 62;
      // 
      // colDescription
      // 
      this.colDescription.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.None;
      this.colDescription.HeaderText = "Description";
      this.colDescription.Name = "colDescription";
      this.colDescription.ReadOnly = true;
      this.colDescription.Width = 85;
      // 
      // colEnvDataValue1
      // 
      this.colEnvDataValue1.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.None;
      this.colEnvDataValue1.HeaderText = "EnvData1_Value";
      this.colEnvDataValue1.Name = "colEnvDataValue1";
      this.colEnvDataValue1.ReadOnly = true;
      this.colEnvDataValue1.Width = 113;
      // 
      // colEnvDataValue2
      // 
      this.colEnvDataValue2.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.None;
      this.colEnvDataValue2.HeaderText = "EnvData2_Value";
      this.colEnvDataValue2.Name = "colEnvDataValue2";
      this.colEnvDataValue2.ReadOnly = true;
      this.colEnvDataValue2.Width = 113;
      // 
      // Column1
      // 
      this.Column1.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill;
      this.Column1.HeaderText = "";
      this.Column1.Name = "Column1";
      this.Column1.ReadOnly = true;
      // 
      // XilApiDialog
      // 
      this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
      this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
      this.ClientSize = new System.Drawing.Size(611, 428);
      this.Controls.Add(this.btnConnect);
      this.Controls.Add(this.btnDisconnect);
      this.Controls.Add(this.gbActiveWhenConnected);
      this.MinimumSize = new System.Drawing.Size(400, 467);
      this.Name = "XilApiDialog";
      this.Text = "XILAPI Client";
      this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.OnFormClosing);
      this.Load += new System.EventHandler(this.OnLoad);
      this.gbActiveWhenConnected.ResumeLayout(false);
      this.groupBox3.ResumeLayout(false);
      this.groupBox3.PerformLayout();
      this.groupBox2.ResumeLayout(false);
      this.groupBox2.PerformLayout();
      ((System.ComponentModel.ISupportInitialize)(this.dgrdFaultMemory)).EndInit();
      this.gbVariantCoding.ResumeLayout(false);
      this.gbVariantCoding.PerformLayout();
      this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button btnReadSerialNo;
        private System.Windows.Forms.Button btnConnect;
        private System.Windows.Forms.Button btnDisconnect;
        private System.Windows.Forms.TextBox tbSerialNumber;
        private System.Windows.Forms.Button btnPerformDiagSequence;
        private System.Windows.Forms.GroupBox gbActiveWhenConnected;
        private System.Windows.Forms.DataGridView dgrdFaultMemory;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button btnReadVariantCoding;
        private System.Windows.Forms.Button btnWriteVariantCoding;
        private System.Windows.Forms.ComboBox cbCountryCode;
        private System.Windows.Forms.ComboBox cbVehicleType;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.GroupBox gbVariantCoding;
    private System.Windows.Forms.Label BasedOnXilApiVersionLabel;
    private System.Windows.Forms.DataGridViewTextBoxColumn colIndex;
    private System.Windows.Forms.DataGridViewTextBoxColumn colDTC;
    private System.Windows.Forms.DataGridViewTextBoxColumn colLongName;
    private System.Windows.Forms.DataGridViewTextBoxColumn colStatus;
    private System.Windows.Forms.DataGridViewTextBoxColumn colDescription;
    private System.Windows.Forms.DataGridViewTextBoxColumn colEnvDataValue1;
    private System.Windows.Forms.DataGridViewTextBoxColumn colEnvDataValue2;
    private System.Windows.Forms.DataGridViewTextBoxColumn Column1;
  }
}

