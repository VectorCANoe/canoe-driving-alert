using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using Vector.Scripting.UI;
using Vector.CANoe.TFS;
using Vector.CANoe.VTS;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;

[TestClass]
public class BrakeAssistantTests
{
    static string detectedObjectName = String.Empty;
    static _ADAS.DataModel.IDetectedMovingObject detectedObject = null;

    [Export]
    [TestCase("Is radar Object Present", "Test if the to be measured radar object appears")]
    public static void IsRadarObjectPresent()
    {
        if (Execution.WaitForUpdate(radar.sensor_info.detected_objects, 10000) == 1)
        {
            detectedObjectName = radar.GetDetectedObjectByTrackingId.Call(1);
            Output.WriteLine(detectedObjectName);
            if (detectedObjectName != String.Empty)
            {
                detectedObject = DORegistry.LookupDistributedObject<_ADAS.DataModel.IDetectedMovingObject>(detectedObjectName, "ADAS");
            }

            if (detectedObject != null)
                Report.TestStepPass("Success, the to be measured and tested radar object appeared.");
            else
                Report.TestStepFail("Fail, the to be measured and tested radar object appeared not!");
        }
        else
        {
            if (detectedObject != null)
                Report.TestStepPass("Success, the to be measured and tested radar object appeared.");
            else
                Report.TestStepFail("Fail, the to be measured and tested radar object appeared not!");
        }
    }

    [Export]
    [TestCase("Is MeasurementState Valid", "Test if the measured radar object has permanently an valid status")]
    public static void IsMeasurementStateValid()
    {
        if (detectedObject.moving_object.header.measurement_state.ImplValue.Value == 2) // Valid
        {
            Execution.Wait(10);

            if (Execution.WaitForChange(detectedObject.moving_object.header.measurement_state, 12000) == 0) // 0 = Timeout, 1 = Success, -1 = Fail (Measurement Aborted or sth. like this)
            {
                Report.TestStepPass("Success, the Measurement State was permanently 2 (Valid)");
            }
            else
            {
                Report.TestStepFail("Fail, the Measurement State was not permanently 2, it changed to " + detectedObject.moving_object.header.measurement_state.ImplValue.Value.ToString() + " for some time");
            }
        }
        else
        {
            Report.TestStepFail("Fail, the Measurement State was not 2 (Valid)");
        }
    }

    [Export]
    [TestCase("Is Existence Probability Over 70%", "Test if the measured radar object has permanently an existence probability over 70%")]
    public static void IsExistenceProbabilityOver70Percent()
    {
        string existenceProb = String.Empty;
        int executionTime = 0;

        if (detectedObject.moving_object.header.existence_probability.ImplValue.Value >= 0.7)
        {
            Report.TestStepPass("Success, the Existence Probability was over 70%");
        }
        else
        {
            Execution.Wait(10);

            while (executionTime <= 60000)
            {
                if (Execution.WaitForUpdate(detectedObject.moving_object.header.existence_probability, 100) == 1) // 0 = Timeout, 1 = Success, -1 = Fail
                {
                    if (detectedObject.moving_object.header.existence_probability.ImplValue.Value >= 0.7)
                    {
                        Report.TestStepPass("Success, the Existence Probability was over 70%");
                        break;
                    }
                    else
                    {
                        Execution.Wait(100);
                        executionTime += 100;
                        continue;
                    }
                }
                else
                {
                    Execution.Wait(100);
                    executionTime += 100;
                    continue;
                }
            }
        }
    }

    [Export]
    [TestCase("Is radar Object In Same Lane", "Test if the measured radar object is in the same lane as the Device Under Test")]
    public static void IsradarObjectInSameLane()
    {
        int executionTime = 0;

        while (executionTime <= 60000)
        {
            if (detectedObject.moving_object.baseInfo.position.y.ImplValue.Value <= 1.5)
            {
                Report.TestStepPass("Success, the radar object is in the same lane as the Device Under Test");
                return;
            }
            Execution.Wait(100);
            executionTime += 100;
        }
        Report.TestStepFail("Fail, the radar object was never in the same lane as the Device Under Test");
    }
}