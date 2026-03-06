using System;
using System.IO;
using System.Text;
using System.Runtime.InteropServices;
using System.Collections.Generic;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using Vector.Scripting.UI;

public class DYNA4_RegisterUserFiles
{
    public void Execute()
    {
      TriggerAnimationProjectLauncher();
    }

    public void GetResults()
    {
      DYNA4.ModelName.Value = "SingleTrack_DriverAssistanceCANoe";
      DYNA4.EnabledSubsystemName.Value = "SimulationModel";
      DYNA4.UserFileAbsPath.Value = "DYNA4Scenario\\Roadworks";
    }

    private void TriggerAnimationProjectLauncher()
    {
      AnimationProjectLauncher.TriggerAnimationProjectLauncher.Value = 1;
    }
}