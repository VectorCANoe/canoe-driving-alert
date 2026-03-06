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

public class AlgorithmUnderTest : MeasurementScript
{
    #region Properties

    public ulong RadarObjectTrackingID { get; set; }
    public ulong RadarObjectMeasurementStatus { get; set; }
    public double RadarObjectPosX { get; set; }
    public double RadarObjectPosY { get; set; }
    public double RadarObjectPosZ { get; set; }
    public double RadarObjectSpeed { get; set; }
    public double EgoSpeed { get; set; }

    #endregion

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
        // Reset the output objects
        ADAS.OutputSimpleAlgorithm.timeToImpact.Value = 999999;
        ADAS.OutputSimpleAlgorithm.isWarningActive.Value = 0;
    }

    /// <summary>
    /// Cleanup after the measurement. Complement to Initialize. This is not
    /// a "Dispose" method; your object should still be usable afterwards.
    /// </summary>
    public override void Shutdown()
    {

    }

    /// <summary>Callback called on update of the radar sensor</summary>
    [OnUpdate(ADAS.FrontRadar.MemberIDs.sensor_info)]
    public void OnUpdateRadarDo()
    {
        var detectedObjects = ADAS.FrontRadar.GetDetectedObjects.Call();

        for (int i = 0; i < detectedObjects.Length; i++)
        {
            _ADAS.DataModel.IDetectedMovingObject radarDynamicDetectedObject = DORegistry.LookupDistributedObject<_ADAS.DataModel.IDetectedMovingObject>(detectedObjects[i], "ADAS");
            if (radarDynamicDetectedObject != null)
            {
                ExecuteSimpleADASalgorithm(radarDynamicDetectedObject);
            }

        }
    }

    /// <summary>Simple Emergency Brake Assistant ADAS algorithm under test.</summary>
    public void ExecuteSimpleADASalgorithm(_ADAS.DataModel.IDetectedMovingObject detectedObject)
    {
        // For simple demonstration purpose: React only on specific radar object from whom we know that it is braking in front of us.
        if (detectedObject.moving_object.header.Value.tracking_id.Value.value.Value == 2)
        {
            RadarObjectTrackingID = detectedObject.moving_object.header.Value.tracking_id.Value.value.Value;
            RadarObjectMeasurementStatus = detectedObject.moving_object.header.Value.measurement_state.Value.ImplValue;

            RadarObjectPosX = detectedObject.moving_object.baseInfo.Value.position.Value.x.Value.ImplValue;
            RadarObjectPosY = detectedObject.moving_object.baseInfo.Value.position.Value.y.Value.ImplValue;
            RadarObjectPosZ = detectedObject.moving_object.baseInfo.Value.position.Value.z.Value.ImplValue;

            RadarObjectSpeed = detectedObject.moving_object.baseInfo.Value.velocity.Value.x.Value.ImplValue;

            EgoSpeed = ADAS.EgoVehicle.geo_data.speed.Value.ImplValue;

            double timeToImpact = 999999; // ms
            int isWarningActive = 0;

            if (RadarObjectMeasurementStatus == 2) // Radar object is active and measured
            {
                if (RadarObjectPosY < 3.0 && RadarObjectPosY > -3.0)  // Radar object is in same lane
                {
                    if (RadarObjectSpeed < 0) // Radar Object is slower
                    {
                        timeToImpact = (RadarObjectPosX / Math.Abs(RadarObjectSpeed)) * 1000;

                        if (timeToImpact < 3000)  // ms
                        {
                            isWarningActive = 1;
                        }
                        else
                        {
                            isWarningActive = 0;
                        }
                    }
                }
            }

            // Write the output of the algorithm on the output objects
            ADAS.OutputSimpleAlgorithm.timeToImpact.Value = timeToImpact;
            ADAS.OutputSimpleAlgorithm.isWarningActive.Value = isWarningActive;

            ADAS.OutputSimpleAlgorithm.egoSpeed.Value = EgoSpeed;
        }
    }
}