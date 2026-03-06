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
public class JSONModifierTest
{
    [Export]
    [TestCase]
    public static void JSONModifierTestCase()
    {
        var orig = new SerializationModel.person();
        orig.age.ImplValue = 32;
        orig.name = "JSONModifier";
        SerializationModel.JSONModifier.JSONPublisher.Value = orig;

        Execution.WaitForUpdate(SerializationModel.JSONModifier.JSONReceiver, 5000);
        var receivedValue = SerializationModel.JSONModifier.JSONReceiver;
        bool success =
          receivedValue.orig.age.ImplValue == orig.age.ImplValue
          && receivedValue.orig.name == orig.name
          && receivedValue.origAge == orig.age.ImplValue;
        if (success)
        {
            Report.TestStepPass("JSON Modifier", "Received the encapsulated message.");
        }
        else
        {
            Report.TestStepFail("JSON Modifier", "Failed.");
        }
    }
}