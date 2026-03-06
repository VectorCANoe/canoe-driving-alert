using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;
using System.Collections.Generic;
using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;
using System.Diagnostics;
using System.Collections.Concurrent;
using System.IO;
using System.Text;


public class HumiditySimulation : MeasurementScript
{
    const string TemperatureTopic = "rooms/living/devFan/AvgTemperature";

    public override void Start()
    {
        ClimateSimulation.HumiditySimulation.HumiditySensor.MQTT_Connect.Call("HumiditySensor_CANoe", null, 60, null, null, null);

        using var Subscription = _MQTT.DataTypes.SubscriptionRequest.CreateInstance();
        Subscription.TopicFilter = TemperatureTopic;
        Subscription.RequestedQos.Value = 0;

        ClimateSimulation.HumiditySimulation.HumiditySensor.MQTT_SubscribeTopic.Call(Subscription);
    }

    [OnCall(ClimateSimulation.HumiditySimulation.HumiditySensor.MemberIDs.MQTT_OnPublishReceived)]
    public void OnPublishReceived(_MQTT.DataTypes.MQTTPublishMessage Message)
    {
        if (Message.PublishTopic == TemperatureTopic)
        {
            var payload = Message.Payload.Value;
            string JsonStringConsumedAvgTemperatureFan = System.Text.Encoding.ASCII.GetString(payload);
            long ConsumedAvgTemperatureFan = Int64.Parse(JsonStringConsumedAvgTemperatureFan);

            long value = ConsumedAvgTemperatureFan - 20;
            long ProvidedHumidity = (50 + value);

            ClimateSimulation.PanelSettings.PanelSetting.Humidity.Value = ProvidedHumidity;

            using var publishMessage = _MQTT.DataTypes.MQTTPublishMessage.CreateInstance();

            string JsonStringProvidedHumidity = ProvidedHumidity.ToString();
            publishMessage.Payload.Value = System.Text.Encoding.ASCII.GetBytes(JsonStringProvidedHumidity);
            publishMessage.PublishTopic = "rooms/living/devHumidityDetector/humidity";
            publishMessage.QoS.Value = 0;
            publishMessage.Retain.Value = false;

            ClimateSimulation.HumiditySimulation.HumiditySensor.MQTT_Publish.Call(publishMessage);
        }
    }

    public override void Stop()
    {
        ClimateSimulation.HumiditySimulation.HumiditySensor.MQTT_Disconnect.Call();
    }

}
