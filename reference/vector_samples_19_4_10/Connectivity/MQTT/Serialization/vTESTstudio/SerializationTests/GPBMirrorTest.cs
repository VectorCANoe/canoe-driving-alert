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
public class GPBMirrorTest
{
    [Export]
    [TestCase]
    public static void GPBMirrorTestCase()
    {
        var mp = new SerializationModel.person();
        mp.age.ImplValue = 15;
        mp.name = "GPB";
        SerializationModel.GPBRepeatClient.GPBPublisher.Value = mp;

        Execution.WaitForUpdate(SerializationModel.GPBRepeatClient.GPBReceiver, 5000);
        var receivedValue = SerializationModel.GPBRepeatClient.GPBReceiver;
        bool success = receivedValue.age == mp.age.ImplValue && receivedValue.name == mp.name;
        if (success)
        {
            Report.TestStepPass("GPB Mirror", "Received the original message.");
        }
        else
        {
            Report.TestStepFail("GPB Mirror", "Failed.");
        }
    }
}