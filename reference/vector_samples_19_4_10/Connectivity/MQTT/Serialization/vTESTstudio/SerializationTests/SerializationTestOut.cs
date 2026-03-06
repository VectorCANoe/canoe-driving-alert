using System;
using System.Collections.ObjectModel;
using System.Text;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using Vector.Scripting.UI;
using Vector.CANoe.TFS;
using Vector.CANoe.VTS;
using NetworkDB;

[TestClass]
public class SerializationTestOut
{
    private static void publishToTopic(String topic, byte[] data)
    {
        var message = new _MQTT.DataTypes.MQTTPublishMessage();
        message.Payload.SetBytes(data);
        message.PublishTopic = topic;

        SerializationModel.SerializationService.Client.MQTT_Publish.Call(message);
    }

    [Export]
    [TestCase]
    public static void SerializationTestCaseOut()
    {
        SerializationModel.SerializationService.Client.MQTT_Connect.Call("Client", false, 60, null, null, null);
        SerializationModel.person person = new SerializationModel.person();
        person.age.ImplValue = 1;
        person.name = "PersonFromSerializationService";

        SerializationModel.SerializationService.Serializer.Serialize_Person.CallAsyncAndWait(person, 5000);
        var personSerialized = SerializationModel.SerializationService.Serializer.Serialize_Person.LatestReturn.Result;

        // Publish an MQTT message and wait
        // Every member has an update counter. To avoid race conditions we note the update counter before publishing the message and then wait until the counter has increased.
        var prePublishCounter = Vector.CANoe.Runtime.Runtime.GetStatus(SerializationModel.SerializationService.HighLevelClient.JSONReceiver).UpdateCount;
        publishToTopic("CANoe/SerializationService/BytesToJson", personSerialized.GetBytes());

        var WaitResult = Execution.WaitForUpdateCountGreater(SerializationModel.SerializationService.HighLevelClient.JSONReceiver, prePublishCounter, 5000);
        if (WaitResult <= 0)
        {
            Report.TestStepFail("Serialization Out", "Did not receive the MQTT message.");
        }
        var receivedValue = SerializationModel.SerializationService.HighLevelClient.JSONReceiver;

        bool success = receivedValue.age == person.age.ImplValue && receivedValue.name == person.name;
        if (success)
        {
            Report.TestStepPass("Serialization Out", "Received the original message.");
        }
        else
        {
            Report.TestStepFail("Serialization Out", "Failed.");
        }

        SerializationModel.SerializationService.Client.MQTT_Disconnect.Call();
        SerializationModel.SerializationService.Client.MQTT_OnDisconnect.WaitForNextCall(5000);
    }
}