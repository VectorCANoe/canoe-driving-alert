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
public class JsonMirrorTest
{
    [Export]
    [TestCase]
    public static void JsonMirrorTestCase()
    {
        var mp = new SerializationModel.person();
        mp.age.ImplValue = 15;
        mp.name = "JSON";
        SerializationModel.JSONRepeatClient.JSONPublisher.Value = mp;

        Execution.WaitForUpdate(SerializationModel.JSONRepeatClient.JSONReceiver, 5000);
        var receivedValue = SerializationModel.JSONRepeatClient.JSONReceiver;
        bool success = receivedValue.age == mp.age.ImplValue && receivedValue.name == mp.name;
        if (success)
        {
            Report.TestStepPass("JSON Mirror", "Received the original message.");
        }
        else
        {
            Report.TestStepFail("JSON Mirror", "Failed.");
        }
    }
}