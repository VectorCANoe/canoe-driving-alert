using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class BasicFunctionalities : MeasurementScript
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
        // Example Code for creating a Sensor Beam
        VehicleSensor_1.sensor_info.sensor_view_configuration.range.PhysValue = 100;                       // m
        VehicleSensor_1.sensor_info.sensor_view_configuration.field_of_view_horizontal.ImplValue = 0.349;  // rad, equals 20° Degree
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

    //
    // Example Code for changing values in an DetectedObject *before* it is sent. Allows e.g. fault injection. 
    //
    // param type=TransientCallContext. The parameter list as defined for this method in the vCDL. In this case a Detected Object
    //
    [OnCalled(VehicleSensor_1.MemberIDs.OnDetectedObjectUpdate)]
    public void OnDetectedObjectUpdate(_ADAS.DataModel.ISensor_Types.OnDetectedObjectUpdate.TransientCallContext tcc)
    {
        string detObjName = VehicleSensor_1.GetDetectedObjectByTrackingId.Call(tcc.trackingId);
        _ADAS.DataModel.IDetectedMovingObject detObj = DORegistry.LookupDistributedObject<_ADAS.DataModel.IDetectedMovingObject>(detObjName, "ADAS");
        if (detObj != null)
        {
            detObj.moving_object.baseInfo.position.x.ImplValue = 20;  // [m]
            detObj.moving_object.baseInfo.position.y.ImplValue = 1;   // [m]
            detObj.moving_object.baseInfo.position.z.ImplValue = 1.5; // [m]
        }
    }

    //
    // Example Code for reacting on incoming DetectedObjects
    //
    [OnUpdate(VehicleSensor_1.MemberIDs.sensor_info)]
    public void OnVehicleSensor_1_Update()
    {
        #region Example Code for How-To iterate over all Dynamic Detected Objects and read their values

        // Get the names (list of strings) of all Dynamic Detected Objects
        var detectedObjectNames = VehicleSensor_1.GetDetectedObjects.Call();

        for (int i = 0; i < detectedObjectNames.Length; i++)
        {
            // Example Code for How-To get a Dynamic Detected Object by its Name and Namespace
            _ADAS.DataModel.IDetectedMovingObject myDynamicDetectedObject1 = DORegistry.LookupDistributedObject<_ADAS.DataModel.IDetectedMovingObject>(detectedObjectNames[i], "ADAS");

            // Example Code for How-To read a value in the Dynamic Detected Object
            double positionX = myDynamicDetectedObject1.moving_object.baseInfo.position.x.ImplValue.Value;
        }

        #endregion

        #region Example Code Code for How-To get a specific Dynamic Detected Object by its Tracking ID and read its values

        // Get the name (string) of a specific Dynamic Detected Object by its Tracking ID (5)
        var myDynamicDetectedObjectName = VehicleSensor_1.GetDetectedObjectByTrackingId.Call(5);

        if (myDynamicDetectedObjectName != String.Empty)
        {
            // Example Code for How-To get the Dynamic Detected Object by its Name and Namespace
            _ADAS.DataModel.IDetectedMovingObject myDynamicDetectedObject2 = DORegistry.LookupDistributedObject<_ADAS.DataModel.IDetectedMovingObject>(myDynamicDetectedObjectName, "ADAS");

            // Example Code for How-To read a value in the Dynamic Detected Object
            double positionY = myDynamicDetectedObject2.moving_object.baseInfo.position.y.ImplValue.Value;
        }

        #endregion
    }

    //
    // Example Code for creating a Detected Object and set some values
    //
    [OnKey('c')]
    public void GetOrCreateDetectedObjectOnKey(char key)
    {
        // Tries to get a DetectedMovingObject with the Tracking Id 8. 
        // If present, returns the Name of the Detected Moving Object.
        // If not, creates the Detected Moving Object and returns the Name. 
        // Empty string if create is not possible.
        var myCreatedDetectedObjectName = VehicleSensor_1.GetOrCreateDetectedObject.Call_Phys(8, _ADAS.DataModel.EDetectedObjectType.IDetectedMovingObject);

        if (myCreatedDetectedObjectName != String.Empty)
        {
            // Example Code for How-To get a Detected Moving Object by its Name and Namespace
            _ADAS.DataModel.IDetectedMovingObject myDetectedMovingObject = DORegistry.LookupDistributedObject<_ADAS.DataModel.IDetectedMovingObject>(myCreatedDetectedObjectName, "ADAS");

            // The BeginUpdate Call locks the Detected Moving Object for sending until released. 
            // Using this mechanism, the Detected Moving Object will only be sent when all values are set
            VehicleSensor_1.BeginUpdate.Call();

            // Example Code for setting values in a Detected Moving Object
            myDetectedMovingObject.moving_object.baseInfo.dimension.height.ImplValue = 1.5; // [m]
            myDetectedMovingObject.moving_object.baseInfo.dimension.width.ImplValue = 2;    // [m]
            myDetectedMovingObject.moving_object.baseInfo.dimension.length.ImplValue = 4;   // [m]

            myDetectedMovingObject.moving_object.baseInfo.position.x.ImplValue = 20;  // [m]
            myDetectedMovingObject.moving_object.baseInfo.position.y.ImplValue = 4;   // [m]
            myDetectedMovingObject.moving_object.baseInfo.position.z.ImplValue = 0;   // [m]

            // Complete and Update. Releases the Detected Moving Object and sends it
            VehicleSensor_1.SetDetectedObjectCompleted.Call(8, true);
            VehicleSensor_1.Update.Call();
        }
    }
}