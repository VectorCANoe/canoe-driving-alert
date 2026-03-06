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
public class SerializationTestIn
{
    public static void subscribeToTopic(String topic)
    {
        var subscriptionRequest = new _MQTT.DataTypes.SubscriptionRequest();

        subscriptionRequest.TopicFilter = topic;
        subscriptionRequest.RequestedQos.ImplValue = 0;

        SerializationModel.SerializationService.Client.MQTT_SubscribeTopic.Call(subscriptionRequest);
    }

    [Export]
    [TestCase]
    public static void SerializationTestCaseIn()
    {
        SerializationModel.SerializationService.Client.MQTT_Connect.Call("Client", true, 60, null, null, null);

        subscribeToTopic("CANoe/SerializationService/JsonToBytes");

        var WaitResult = SerializationModel.SerializationService.Client.MQTT_OnSubscribe.WaitForNextCall(5000);
        if (WaitResult.WaitResult <= 0)
        {
            Report.TestStepFail("Serialization In", "Did not receive SUBACK.");
        }

        SerializationModel.person person = new SerializationModel.person();
        person.age.ImplValue = 2;
        person.name = "PersonFromHighLevelClient";

        SerializationModel.SerializationService.HighLevelClient.JSONPublisher.Value = person;

        var WaitResultPublish = SerializationModel.SerializationService.Client.MQTT_OnPublishReceived.WaitForNextCall(5000);
        if (WaitResultPublish.WaitResult <= 0)
        {
            Report.TestStepFail("Serialization In", "Did not receive MQTT message.");
        }
        var payload = SerializationModel.SerializationService.Client.MQTT_OnPublishReceived.LatestCall.Message.Payload.GetBytes();

        SerializationModel.SerializationService.Serializer.Deserialize_Person.CallAsyncAndWait(payload, 5000);
        var personDeserialized = SerializationModel.SerializationService.Serializer.Deserialize_Person.LatestReturn.Result;

        bool success = personDeserialized.age.ImplValue == person.age.ImplValue && personDeserialized.name == person.name;
        if (success)
        {
            Report.TestStepPass("Serialization In", "Received the original message.");
        }
        else
        {
            Report.TestStepFail("Serialization In", "Failed.");
        }

        SerializationModel.SerializationService.Client.MQTT_Disconnect.Call();
        SerializationModel.SerializationService.Client.MQTT_OnDisconnect.WaitForNextCall(5000);
    }
}