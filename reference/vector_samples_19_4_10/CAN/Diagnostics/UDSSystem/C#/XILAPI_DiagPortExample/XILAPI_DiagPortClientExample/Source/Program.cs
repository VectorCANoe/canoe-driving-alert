/*---------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
---------------------------------------------------------------------------*/

#region Usings

using System;
using System.Windows.Forms;

#endregion

namespace XILAPI_DiagPortClientExample.Source
{
  internal static class Program
  {
    /// <summary>
    ///   The main entry point for the application.
    /// </summary>
    [STAThread]
    private static void Main()
    {
      Application.EnableVisualStyles();
      Application.SetCompatibleTextRenderingDefault(false);
      Application.Run(new XilApiDialog());
    }
  }
}
