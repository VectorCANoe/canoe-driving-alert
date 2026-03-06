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
public class MyTestClass
{

    //--------------------------------------------------------
    // Test Connection/Subscription
    [Export]
    [TestCase("Subscription", "Testing Subscription of all Consumed Members")]
    public static void TestSubscription(ulong timeToWaitForSubscription)
    {
        Report.TestStep("Checking subscription of all consumed members");
        bool allSubscribed = true;
        bool allReturnedSuccessfully = true;

        ITypedValueEntityReadOnly<DOSubscriptionState>[] consumerStates =
        {
            ClimateSimulation.ClimateControl.ClimateControl.ConsumedTemperature1.SubscriptionState,
            ClimateSimulation.ClimateControl.ClimateControl.ConsumedTemperature2.SubscriptionState,
            ClimateSimulation.ClimateControl.ClimateControl.ConsumedTemperature3.SubscriptionState,
            ClimateSimulation.ClimateControl.ClimateControl.ConsumedTemperature4.SubscriptionState,
            ClimateSimulation.ClimateControl.ClimateControl.RotationSpeed.SubscriptionState,
            ClimateSimulation.FanSimulation.Fan1.ConsumedTemperature1.SubscriptionState,
            ClimateSimulation.FanSimulation.Fan1.ConsumedTemperature2.SubscriptionState,
            ClimateSimulation.FanSimulation.Fan1.ConsumedTemperature3.SubscriptionState,
            ClimateSimulation.FanSimulation.Fan1.ConsumedTemperature4.SubscriptionState,
            ClimateSimulation.FanSimulation.Fan1.ConsumedHumidity.SubscriptionState
        };

        int countConsumers = consumerStates.Length;
        int[] ret = new int[countConsumers];
        for (int i = 0; i < countConsumers; i++)
        {
            var val1 = (ulong)(2000 - Measurement.CurrentTime.TotalMilliseconds);
            var valMax = val1 > timeToWaitForSubscription ? val1 : timeToWaitForSubscription;
            try
            {
                ret[i] = Execution.WaitForUpdateCountGreater(consumerStates[i], 1, (int)valMax);
            }
            catch
            {
                //Catch exception of wait-method
                Report.TestStepFail("Subscription", "Not all WaitForUpdateCountGreater returned successfully");
            }
        }

        for (int i = 0; i < countConsumers; i++)
        {
            allReturnedSuccessfully = allReturnedSuccessfully && ret[i] > 0;
        }
        if (!allReturnedSuccessfully)
        {
            Report.TestStepFail("Subscription", "Not all WaitForUpdateCountGreater returned successfully");
        }

        for (int i = 0; i < countConsumers; i++)
        {
            allSubscribed = allSubscribed && (consumerStates[i].Value == DOSubscriptionState.Subscribed);
        }
        if (!allSubscribed)
        {
            Report.TestStepFail("Subscription", "Not all Consumers subscribed successfully");
        }
        else
        {
            Report.TestStepPass("Subscription", "All consumed members subscribed successfully");
        }
    }
}

//--------------------------------------------------------
