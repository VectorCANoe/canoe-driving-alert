using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;

using System.Threading;

public class ADASDataProvider : MeasurementScript
{
    /// <summary>
    /// Called before measurement start to perform necessary initializations,
    /// e.g. to create objects. During measurement, few additional objects
    /// should be created to prevent garbage collection runs in time-critical
    /// simulations.
    /// </summary>
    public override void Initialize()
    {

    }

    /// <summary>Notification that the measurement starts.</summary>
    public override void Start()
    {

    }

    /// <summary>Notification that the measurement ends.</summary>
    public override void Stop()
    {

    }

    /// <summary>
    /// Cleanup after the measurement. Complement to Initialize. This is not
    /// a "Dispose" method; your object should still be usable afterwards.
    /// </summary>
    public override void Shutdown()
    {

    }

    /// <summary>Callback called on update of the radar sensor</summary>
    [OnUpdate(FrontRadar.MemberIDs.sensor_info)]
    public void OnUpdateRadarDo()
    {
        var detectedObjects = FrontRadar.GetDetectedObjects.Call();

        for (int i = 0; i < detectedObjects.Length; i++)
        {
            _ADAS.DataModel.IDetectedMovingObject radarDynamicDetectedObject = DORegistry.LookupDistributedObject<_ADAS.DataModel.IDetectedMovingObject>(detectedObjects[i], "ADAS");

            // For simple demonstration purpose: React only on specific radar object from whom we know that it is braking in front of us
            if (radarDynamicDetectedObject != null && radarDynamicDetectedObject.moving_object.header.tracking_id.value.ImplValue.Value == 2)
            {
                // Set inputs: CANoe => ROS
                ADAS.InputROS.input.radarObject.trackingId.ImplValue = radarDynamicDetectedObject.moving_object.header.tracking_id.value.ImplValue.Value;
                ADAS.InputROS.input.radarObject.measurementStatus.ImplValue = radarDynamicDetectedObject.moving_object.header.measurement_state.ImplValue.Value;
                ADAS.InputROS.input.radarObject.posX.ImplValue = radarDynamicDetectedObject.moving_object.baseInfo.position.x.ImplValue.Value;
                ADAS.InputROS.input.radarObject.posY.ImplValue = radarDynamicDetectedObject.moving_object.baseInfo.position.y.ImplValue.Value;
                ADAS.InputROS.input.radarObject.posZ.ImplValue = radarDynamicDetectedObject.moving_object.baseInfo.position.z.ImplValue.Value;
                ADAS.InputROS.input.radarObject.speed.ImplValue = radarDynamicDetectedObject.moving_object.baseInfo.velocity.x.ImplValue.Value;
            }
        }
    }
}