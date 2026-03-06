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
    [TestCase("Is Radar Object Present", "Test if the to be measured radar object appears")]
    public static void IsRadarObjectPresent()
    {
        if (Execution.WaitForChange(FrontRadar.sensor_info.detected_objects, 1000) == 1)
        {
            detectedObjectName = "Detected_id_2_by_FrontRadar"; // Look out for specific object (tracking id = 2)

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
    [TestCase("Is Radar Object In Same Lane", "Test if the measured radar object is in the same lane as the Device Under Test")]
    public static void IsRadarObjectInSameLane()
    {
        bool success = false;

        int executionTime = 0;

        while (executionTime <= 60000)
        {
            if (Execution.WaitForUpdate(detectedObject.moving_object.baseInfo.position.y, 100) == 1) // 0 = Timeout, 1 = Success, -1 = Fail
            {
                if (detectedObject.moving_object.baseInfo.position.y.ImplValue.Value <= 0.25 &&
                    detectedObject.moving_object.baseInfo.position.y.ImplValue.Value >= -0.25)
                {
                    success = true;
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

        if (success)
        {
            Report.TestStepPass("Success, the radar object is in the same lane as the Device Under Test");
        }
        else
        {
            Report.TestStepFail("Fail, the radar object was never in the same lane as the Device Under Test");
        }
    }

    [Export]
    [TestCase("Wait for Scenario end", "Waits until the current scenario has ended")]
    public static void WaitForScenarioEnd()
    {
        int executionTime = 0;

        while (executionTime <= 16500)
        {
            Execution.Wait(100);
            executionTime += 100;
            continue;
        }

        Report.TestStepPass("Success, scenario has ended.");
    }
}