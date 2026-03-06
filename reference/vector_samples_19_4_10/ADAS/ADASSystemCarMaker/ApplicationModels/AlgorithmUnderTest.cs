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

    private ulong radarObjectTrackingID;

    public ulong RadarObjectTrackingID
    {
        get { return radarObjectTrackingID; }
        set { radarObjectTrackingID = value; }
    }

    private ulong radarObjectMeasurementStatus;

    public ulong RadarObjectMeasurementStatus
    {
        get { return radarObjectMeasurementStatus; }
        set { radarObjectMeasurementStatus = value; }
    }

    private double radarObjectPosX;

    public double RadarObjectPosX
    {
        get { return radarObjectPosX; }
        set { radarObjectPosX = value; }
    }

    private double radarObjectPosY;

    public double RadarObjectPosY
    {
        get { return radarObjectPosY; }
        set { radarObjectPosY = value; }
    }

    private double radarObjectPosZ;

    public double RadarObjectPosZ
    {
        get { return radarObjectPosZ; }
        set { radarObjectPosZ = value; }
    }

    private double radarObjectSpeed;

    public double RadarObjectSpeed
    {
        get { return radarObjectSpeed; }
        set { radarObjectSpeed = value; }
    }

    private double egoSpeed;
    public double EgoSpeed
    {
        get { return egoSpeed; }
        set { egoSpeed = value; }
    }

    bool keepBrakeAssistActive = false;

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

    /// <summary>Callback called on update of the radar sensor</summary>
    [OnUpdate(radar.MemberIDs.sensor_info)]
    public void OnUpdateRadarDo()
    {
        var detectedObjects = radar.GetDetectedObjects.Call();

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
        if (detectedObject.moving_object.header.tracking_id.value.ImplValue.Value == 1)
        {
            RadarObjectTrackingID = detectedObject.moving_object.header.tracking_id.value.ImplValue.Value;
            RadarObjectMeasurementStatus = detectedObject.moving_object.header.measurement_state.ImplValue.Value;

            RadarObjectPosX = detectedObject.moving_object.baseInfo.position.x.ImplValue.Value;
            RadarObjectPosY = detectedObject.moving_object.baseInfo.position.y.ImplValue.Value;
            RadarObjectPosZ = detectedObject.moving_object.baseInfo.position.z.ImplValue.Value;

            RadarObjectSpeed = detectedObject.moving_object.baseInfo.velocity.x.ImplValue.Value;

            EgoSpeed = CarMaker.Car.vx.Value;

            double timeToImpact = 999999; // ms
            double distanceToObject = 0; //m
            int isWarningActive = 0;

            if (RadarObjectMeasurementStatus == 2) // Radar object is active and measured
            {
                distanceToObject = RadarObjectPosX;
                if (RadarObjectPosY < 3.0 && RadarObjectPosY > -3.0)  // Radar object is in same lane
                {
                    if (RadarObjectSpeed < 0) // Radar Object is slower
                    {
                        timeToImpact = (RadarObjectPosX / Math.Abs(RadarObjectSpeed)) * 1000;

                        if (timeToImpact < 3000)  // ms
                        {
                            isWarningActive = 1;
                            keepBrakeAssistActive = true;
                        }
                        else
                        {
                            if (keepBrakeAssistActive)
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
            }

            // Write the output of the algorithm on the output objects
            ADAS.OutputSimpleAlgorithm.timeToImpact.ImplValue = timeToImpact;
            ADAS.OutputSimpleAlgorithm.isWarningActive.ImplValue = isWarningActive;
            ADAS.OutputSimpleAlgorithm.distanceToObject.ImplValue = distanceToObject;
            ADAS.OutputSimpleAlgorithm.egoSpeed.ImplValue = EgoSpeed;

            if (timeToImpact == 999999)
            {
                if (keepBrakeAssistActive)
                    keepBrakeAssistActive = false;
            }
        }
    }

    /// <summary>Notification that the measurement ends.</summary>
    public override void Stop()
    {
        // Reset the output objects
        ADAS.OutputSimpleAlgorithm.timeToImpact.ImplValue = 999999;
        ADAS.OutputSimpleAlgorithm.isWarningActive.ImplValue = 0;
    }

    /// <summary>
    /// Cleanup after the measurement. Complement to Initialize. This is not
    /// a "Dispose" method; your object should still be usable afterwards.
    /// </summary>
    public override void Shutdown()
    {

    }
}