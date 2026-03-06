using System;
using System.Collections.ObjectModel;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using Vector.Scripting.UI;
using Vector.CANoe.TFS;
using Vector.CANoe.VTS;
using NetworkDB;

[TestClass]
public class ECGMonitorTests
{
    [Export]
    [TestCase]
    [TraceItem("a31342c143aea0ddc7783")]
    [TraceItem("a31342c143aea0ddc7784")]
    public static void First_normal_heart_rhythm_then_sudden_emergency()
    {
        CaplTestFunctions.TestUtils.SendECGSignalWithoutArrhythmia();
        Execution.Wait(10000);
        CheckAlarmTransferredToECGMonitor(0);
        CaplTestFunctions.TestUtils.StopECGSignalWithoutArrhythmia();
        CaplTestFunctions.TestUtils.StartSimulatingEmergencyCase();
        Execution.Wait(10000);
        CheckAlarmTransferredToECGMonitor(1);
    }

    [Export]
    [TestCase]
    [TraceItem("a31342c143aea0ddc7783")]
    [TraceItem("a31342c143aea0ddc7784")]
    public static void Emergency_stabilizing_to_normal_heart_rhythm()
    {
        CaplTestFunctions.TestUtils.StartSimulatingEmergencyCase();
        Execution.Wait(10000);
        CheckAlarmTransferredToECGMonitor(1);
        CaplTestFunctions.TestUtils.StopSimulatingEmergencyCase();
        CaplTestFunctions.TestUtils.SendECGSignalWithoutArrhythmia();
        Execution.Wait(10000);
        CheckAlarmTransferredToECGMonitor(0);
    }

    [Export]
    [TestFunction]
    public static void CheckAlarmTransferredToECGMonitor(uint expectAlarmON)
    {
        if (expectAlarmON == 0)
        {
            Report.TestCaseComment("Checking heart rate alarm transferred to ECG Monitor...");
            if (SmartECG.ECGMonitor.heartRateCritical.Value == true)
            {
                SampleDataControl.SampleDataControl.isEmergencySimulationRunning = false;
                CaplTestFunctions.TestUtils.StopECGSignalWithoutArrhythmia();
                Report.TestStepFail("Test failed: Heart Rate Alarm transferred to ECG Monitor is ON, despite an ECG signal without arrhythmia.");
            }
            else
            {
                Report.TestCaseComment("Verified that Heart Rate Alarm transferred to ECG Monitor is OFF for ECG signal without arrhythmia.");
            }
        }
        else
        {
            if (SmartECG.ECGMonitor.heartRateCritical.Value == false)
            {
                Report.TestStepFail("Test failed: Heart Rate Alarm transferred to ECG Monitor is OFF, despite an ECG signal which represents an emergency case with arrhythmia.");
            }
            else
            {
                Report.TestStepPass("Test successful: Heart Rate Alarm transferred to ECG Monitor is ON in emergency situation where ECG signal shows arrhythmia.");
            }
            CaplTestFunctions.TestUtils.StopSimulatingEmergencyCase();
        }
    }
}