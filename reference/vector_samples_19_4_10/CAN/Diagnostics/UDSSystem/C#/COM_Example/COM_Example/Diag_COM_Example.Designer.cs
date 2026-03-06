namespace ExampleDiagnosticsViaCOM
{
    partial class Diag_COM_Example
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
      this.tbResult = new System.Windows.Forms.TextBox();
      this.groupBox1 = new System.Windows.Forms.GroupBox();
      this.button1 = new System.Windows.Forms.Button();
      this.networksTreeView = new System.Windows.Forms.TreeView();
      this.btnClose = new System.Windows.Forms.Button();
      this.label1 = new System.Windows.Forms.Label();
      this.btnReadSwVersion = new System.Windows.Forms.Button();
      this.tbSerialNumber = new System.Windows.Forms.TextBox();
      this.btnDefaultSessionStart = new System.Windows.Forms.Button();
      this.btnExecuteDiagTest = new System.Windows.Forms.Button();
      this.tbVerdict = new System.Windows.Forms.TextBox();
      this.groupBox1.SuspendLayout();
      this.SuspendLayout();
      // 
      // tbResult
      // 
      this.tbResult.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.tbResult.Location = new System.Drawing.Point(6, 48);
      this.tbResult.Multiline = true;
      this.tbResult.Name = "tbResult";
      this.tbResult.ScrollBars = System.Windows.Forms.ScrollBars.Both;
      this.tbResult.Size = new System.Drawing.Size(400, 99);
      this.tbResult.TabIndex = 2;
      // 
      // groupBox1
      // 
      this.groupBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
      this.groupBox1.Controls.Add(this.button1);
      this.groupBox1.Controls.Add(this.tbResult);
      this.groupBox1.Location = new System.Drawing.Point(194, 122);
      this.groupBox1.Name = "groupBox1";
      this.groupBox1.Size = new System.Drawing.Size(412, 153);
      this.groupBox1.TabIndex = 3;
      this.groupBox1.TabStop = false;
      this.groupBox1.Text = "Output";
      // 
      // button1
      // 
      this.button1.Location = new System.Drawing.Point(6, 19);
      this.button1.Name = "button1";
      this.button1.Size = new System.Drawing.Size(75, 23);
      this.button1.TabIndex = 3;
      this.button1.Text = "Clear";
      this.button1.UseVisualStyleBackColor = true;
      this.button1.Click += new System.EventHandler(this.btnClear_Click);
      // 
      // networksTreeView
      // 
      this.networksTreeView.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
      this.networksTreeView.HideSelection = false;
      this.networksTreeView.Location = new System.Drawing.Point(12, 28);
      this.networksTreeView.Name = "networksTreeView";
      this.networksTreeView.Size = new System.Drawing.Size(176, 247);
      this.networksTreeView.TabIndex = 3;
      this.networksTreeView.AfterSelect += new System.Windows.Forms.TreeViewEventHandler(this.networksTreeView_AfterSelect);
      // 
      // btnClose
      // 
      this.btnClose.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
      this.btnClose.Location = new System.Drawing.Point(531, 283);
      this.btnClose.Name = "btnClose";
      this.btnClose.Size = new System.Drawing.Size(75, 23);
      this.btnClose.TabIndex = 4;
      this.btnClose.Text = "Close";
      this.btnClose.UseVisualStyleBackColor = true;
      this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
      // 
      // label1
      // 
      this.label1.AutoSize = true;
      this.label1.Location = new System.Drawing.Point(12, 12);
      this.label1.Name = "label1";
      this.label1.Size = new System.Drawing.Size(77, 13);
      this.label1.TabIndex = 5;
      this.label1.Text = "Selected ECU:";
      // 
      // btnReadSwVersion
      // 
      this.btnReadSwVersion.Location = new System.Drawing.Point(194, 57);
      this.btnReadSwVersion.Name = "btnReadSwVersion";
      this.btnReadSwVersion.Size = new System.Drawing.Size(123, 23);
      this.btnReadSwVersion.TabIndex = 1;
      this.btnReadSwVersion.Text = "Read serial number";
      this.btnReadSwVersion.UseVisualStyleBackColor = true;
      this.btnReadSwVersion.Click += new System.EventHandler(this.btnReadSwVersion_Click);
      // 
      // tbSerialNumber
      // 
      this.tbSerialNumber.Location = new System.Drawing.Point(323, 59);
      this.tbSerialNumber.Name = "tbSerialNumber";
      this.tbSerialNumber.Size = new System.Drawing.Size(119, 20);
      this.tbSerialNumber.TabIndex = 6;
      this.tbSerialNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
      // 
      // btnDefaultSessionStart
      // 
      this.btnDefaultSessionStart.Location = new System.Drawing.Point(195, 28);
      this.btnDefaultSessionStart.Name = "btnDefaultSessionStart";
      this.btnDefaultSessionStart.Size = new System.Drawing.Size(122, 23);
      this.btnDefaultSessionStart.TabIndex = 7;
      this.btnDefaultSessionStart.Text = "Default Session Start";
      this.btnDefaultSessionStart.UseVisualStyleBackColor = true;
      this.btnDefaultSessionStart.Click += new System.EventHandler(this.btnDefaultSessionStart_Click);
      // 
      // btnExecuteDiagTest
      // 
      this.btnExecuteDiagTest.Location = new System.Drawing.Point(194, 86);
      this.btnExecuteDiagTest.Name = "btnExecuteDiagTest";
      this.btnExecuteDiagTest.Size = new System.Drawing.Size(123, 23);
      this.btnExecuteDiagTest.TabIndex = 1;
      this.btnExecuteDiagTest.Text = "Execute Diag Test";
      this.btnExecuteDiagTest.UseVisualStyleBackColor = true;
      this.btnExecuteDiagTest.Click += new System.EventHandler(this.btnExecuteDiagTest_Click);
      // 
      // tbVerdict
      // 
      this.tbVerdict.Location = new System.Drawing.Point(323, 88);
      this.tbVerdict.Name = "tbVerdict";
      this.tbVerdict.Size = new System.Drawing.Size(119, 20);
      this.tbVerdict.TabIndex = 8;
      this.tbVerdict.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
      // 
      // Diag_COM_Example
      // 
      this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
      this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
      this.ClientSize = new System.Drawing.Size(618, 318);
      this.Controls.Add(this.tbVerdict);
      this.Controls.Add(this.btnDefaultSessionStart);
      this.Controls.Add(this.tbSerialNumber);
      this.Controls.Add(this.label1);
      this.Controls.Add(this.btnClose);
      this.Controls.Add(this.networksTreeView);
      this.Controls.Add(this.groupBox1);
      this.Controls.Add(this.btnExecuteDiagTest);
      this.Controls.Add(this.btnReadSwVersion);
      this.Name = "Diag_COM_Example";
      this.Text = "Diag_COM_Example";
      this.groupBox1.ResumeLayout(false);
      this.groupBox1.PerformLayout();
      this.ResumeLayout(false);
      this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox tbResult;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.TreeView networksTreeView;
        private System.Windows.Forms.Button btnClose;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button btnReadSwVersion;
        private System.Windows.Forms.TextBox tbSerialNumber;
        private System.Windows.Forms.Button btnDefaultSessionStart;
        private System.Windows.Forms.Button btnExecuteDiagTest;
        private System.Windows.Forms.TextBox tbVerdict;
        private System.Windows.Forms.Button button1;
    }
}

