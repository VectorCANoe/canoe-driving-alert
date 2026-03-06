using System;
using System.Collections.Generic;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class Mapping : MeasurementScript
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
        radar.BeginUpdate.Call();
        radar.sensor_info.sensor_view_configuration.range.PhysValue = 150;
        // 40 deg in rad
        radar.sensor_info.sensor_view_configuration.field_of_view_horizontal.ImplValue = 0.698132;

        radar.Update.Call();
        // radar.SetDetectedObjectsCompleted.Call();
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

    //private int mDetectedObjectsCount = 0;

    _ADAS.DataModel.IDetectedMovingObject GetOrCreateMovingObject(UInt32 trackingId)
    {
        string detObj = radar.GetOrCreateDetectedObject.Call_Phys(trackingId, _ADAS.DataModel.EDetectedObjectType.IDetectedMovingObject);
        if (detObj != null && detObj != string.Empty)
        {
            return DORegistry.LookupDistributedObject<_ADAS.DataModel.IDetectedMovingObject>(detObj, "ADAS");
        }
        return null;
    }

    [OnChange(typeof(CarMaker.Car.vx))]
    public void OnCarUpdate()
    {
        radar.BeginUpdate.Call();
        radar.Update.Call();
    }

    [OnChange(typeof(CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.RefPnt.ds.x))]
    public void OnT00Update()
    {
        //Hardcoded Id 1
        _ADAS.DataModel.IDetectedMovingObject newDetectedObject = null;

        if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.dtct.Value == 1)
        {
            //Only Create Detected Object if Sensor Object is detected by CarMakerIbject Sensor
            newDetectedObject = GetOrCreateMovingObject(1);

            //measurement state detected
            newDetectedObject.moving_object.header.measurement_state.ImplValue = 2;

            newDetectedObject.moving_object.baseInfo.position.x.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.RefPnt.ds.x.Value; // [m]
            newDetectedObject.moving_object.baseInfo.position.y.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.RefPnt.ds.y.Value; // [m]
            newDetectedObject.moving_object.baseInfo.position.z.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.RefPnt.ds.z.Value; // [m]

            newDetectedObject.moving_object.baseInfo.velocity.x.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.RefPnt.dv.x.Value; // [m]
            newDetectedObject.moving_object.baseInfo.velocity.y.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.RefPnt.dv.y.Value; // [m]
            newDetectedObject.moving_object.baseInfo.velocity.z.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.RefPnt.dv.z.Value; // [m]

            //Dimension hardcoded
            newDetectedObject.moving_object.baseInfo.dimension.length.ImplValue = 4.28; // [m]
            newDetectedObject.moving_object.baseInfo.dimension.width.ImplValue = 1.82; // [m]
            newDetectedObject.moving_object.baseInfo.dimension.height.ImplValue = 1.28; // [m]

            newDetectedObject.moving_object.candidate[0].probability.ImplValue = 1; // [%]
            newDetectedObject.moving_object.candidate[0].type.ImplValue = 2; //0: Undefined 1: Unknown 2: Vehicle 3: Pedestrian
            newDetectedObject.moving_object.candidate[0].vehicle_classification.type.ImplValue = 3; // 1: Other 3: CompactCar 6: Delivery Van

            //Existence Probability hardcoded
            newDetectedObject.moving_object.header.existence_probability.ImplValue = 0.95; // [%]
            radar.SetDetectedObjectCompleted.Call(1, true);
        }
    }

    [OnChange(typeof(CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.dtct))]
    public void OnT00DtctUpdate()
    {

        _ADAS.DataModel.IDetectedMovingObject newDetectedObject = null;

        if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T00.dtct.Value == 0)
        {
            newDetectedObject = GetOrCreateMovingObject(1);

            //measurement state other
            newDetectedObject.moving_object.header.measurement_state.ImplValue = 0;
            radar.SetDetectedObjectCompleted.Call(1, true);
        }
    }

    [OnChange(typeof(CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.RefPnt.ds.x))]
    public void OnTO1Update()
    {
        _ADAS.DataModel.IDetectedMovingObject newDetectedObject = null;

        //Only Create Detected Object if Sensor Object is detected by CarMakerIbject Sensor
        if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.dtct.Value == 1)
        {
            //Hardcoded Id 2
            newDetectedObject = GetOrCreateMovingObject(2);
            if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.dtct.Value == 1)
            {

                //measurement state detected
                newDetectedObject.moving_object.header.measurement_state.ImplValue = 2;

                newDetectedObject.moving_object.baseInfo.position.x.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.RefPnt.ds.x.Value; // [m]
                newDetectedObject.moving_object.baseInfo.position.y.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.RefPnt.ds.y.Value; // [m]
                newDetectedObject.moving_object.baseInfo.position.z.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.RefPnt.ds.z.Value; // [m]

                newDetectedObject.moving_object.baseInfo.velocity.x.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.RefPnt.dv.x.Value; // [m]
                newDetectedObject.moving_object.baseInfo.velocity.y.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.RefPnt.dv.y.Value; // [m]
                newDetectedObject.moving_object.baseInfo.velocity.z.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.RefPnt.dv.z.Value; // [m]

                //Dimension hardcoded
                newDetectedObject.moving_object.baseInfo.dimension.length.ImplValue = 3.233; // [m]
                newDetectedObject.moving_object.baseInfo.dimension.width.ImplValue = 1.525; // [m]
                newDetectedObject.moving_object.baseInfo.dimension.height.ImplValue = 1.645; // [m]

                newDetectedObject.moving_object.candidate[0].probability.ImplValue = 1; // [%]
                newDetectedObject.moving_object.candidate[0].type.ImplValue = 2; //0: Undefined 1: Unknown 2: Vehicle 3: Pedestrian
                newDetectedObject.moving_object.candidate[0].vehicle_classification.type.ImplValue = 1; // 1: Other 3: CompactCar 6: Delivery Van

                //Existence Probability hardcoded
                newDetectedObject.moving_object.header.existence_probability.ImplValue = 0.95; // [%]
                radar.SetDetectedObjectCompleted.Call(2, true);
            }
        }
    }

    [OnChange(typeof(CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.dtct))]
    public void OnT01DtctUpdate()
    {

        _ADAS.DataModel.IDetectedMovingObject newDetectedObject = null;

        if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T01.dtct.Value == 0)
        {
            newDetectedObject = GetOrCreateMovingObject(2);
            //measurement state other
            newDetectedObject.moving_object.header.measurement_state.ImplValue = 0;
            radar.SetDetectedObjectCompleted.Call(2, true);
        }
    }

    [OnChange(typeof(CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.RefPnt.ds.x))]
    public void OnTO2Update()
    {
        //Hardcoded Id 3
        var result = radar.HasDetectedObject.Call(3);
        _ADAS.DataModel.IDetectedMovingObject newDetectedObject = null;

        if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.dtct.Value == 1)
        {
            //Only Create Detected Object if Sensor Object is detected by CarMakerIbject Sensor
            newDetectedObject = GetOrCreateMovingObject(3);

            //measurement state detected
            newDetectedObject.moving_object.header.measurement_state.ImplValue = 2;

            newDetectedObject.moving_object.baseInfo.position.x.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.RefPnt.ds.x.Value; // [m]
            newDetectedObject.moving_object.baseInfo.position.y.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.RefPnt.ds.y.Value; // [m]
            newDetectedObject.moving_object.baseInfo.position.z.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.RefPnt.ds.z.Value; // [m]

            newDetectedObject.moving_object.baseInfo.velocity.x.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.RefPnt.dv.x.Value; // [m]
            newDetectedObject.moving_object.baseInfo.velocity.y.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.RefPnt.dv.y.Value; // [m]
            newDetectedObject.moving_object.baseInfo.velocity.z.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.RefPnt.dv.z.Value; // [m]

            //Dimension hardcoded
            newDetectedObject.moving_object.baseInfo.dimension.length.ImplValue = 0.49; // [m]
            newDetectedObject.moving_object.baseInfo.dimension.width.ImplValue = 0.60; // [m]
            newDetectedObject.moving_object.baseInfo.dimension.height.ImplValue = 1.82; // [m]

            newDetectedObject.moving_object.candidate[0].probability.ImplValue = 1; // [%]
            newDetectedObject.moving_object.candidate[0].type.ImplValue = 3; //0: Undefined 1: Unknown 2: Vehicle 3: Pedestrian
            newDetectedObject.moving_object.candidate[0].vehicle_classification.type.ImplValue = 1; // 1: Other 3: CompactCar 6: Delivery Van

            //Existence Probability hardcoded
            newDetectedObject.moving_object.header.existence_probability.ImplValue = 0.95; // [%]
            radar.SetDetectedObjectCompleted.Call(3, true);
        }
    }

    [OnChange(typeof(CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.dtct))]
    public void OnT02DtctUpdate()
    {
        _ADAS.DataModel.IDetectedMovingObject newDetectedObject = null;

        if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T02.dtct.Value == 0)
        {
            newDetectedObject = GetOrCreateMovingObject(3);

            //measurement state other
            newDetectedObject.moving_object.header.measurement_state.ImplValue = 0;
            radar.SetDetectedObjectCompleted.Call(3, true);
        }
    }

    [OnChange(typeof(CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.RefPnt.ds.x))]
    public void OnTO3Update()
    {
        _ADAS.DataModel.IDetectedMovingObject newDetectedObject = null;
        // Hardcoded Id 4
        if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.dtct.Value == 1)
        {
            //Only Create Detected Object if Sensor Object is detected by CarMakerIbject Sensor
            newDetectedObject = GetOrCreateMovingObject(4);

            newDetectedObject.moving_object.header.measurement_state.ImplValue = 2;
            newDetectedObject.moving_object.baseInfo.position.x.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.RefPnt.ds.x.Value; // [m]
            newDetectedObject.moving_object.baseInfo.position.y.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.RefPnt.ds.y.Value; // [m]
            newDetectedObject.moving_object.baseInfo.position.z.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.RefPnt.ds.z.Value; // [m]

            newDetectedObject.moving_object.baseInfo.velocity.x.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.RefPnt.dv.x.Value; // [m]
            newDetectedObject.moving_object.baseInfo.velocity.y.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.RefPnt.dv.y.Value; // [m]
            newDetectedObject.moving_object.baseInfo.velocity.z.ImplValue = CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.RefPnt.dv.z.Value; // [m]

            //Dimension hardcoded
            newDetectedObject.moving_object.baseInfo.dimension.length.ImplValue = 6.95; // [m]
            newDetectedObject.moving_object.baseInfo.dimension.width.ImplValue = 1.94; // [m]
            newDetectedObject.moving_object.baseInfo.dimension.height.ImplValue = 2.70; // [m]

            newDetectedObject.moving_object.candidate[0].probability.ImplValue = 1; // [%]
            newDetectedObject.moving_object.candidate[0].type.ImplValue = 2; //0: Undefined 1: Unknown 2: Vehicle 3: Pedestrian
            newDetectedObject.moving_object.candidate[0].vehicle_classification.type.ImplValue = 3; // 1: Other 3: CompactCar 6: Delivery Van

            //Existence Probability hardcoded
            newDetectedObject.moving_object.header.existence_probability.ImplValue = 0.95; // [%]

            radar.SetDetectedObjectCompleted.Call(4, true);
        }


    }


    [OnChange(typeof(CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.dtct))]
    public void OnT03DtctUpdate()
    {

        _ADAS.DataModel.IDetectedMovingObject newDetectedObject = null;

        if (CarMaker.Sensor.Object.Vhcl.Radar.Obj.T03.dtct.Value == 0)
        {
            newDetectedObject = GetOrCreateMovingObject(4);

            //measurement state other
            newDetectedObject.moving_object.header.measurement_state.ImplValue = 0;
            radar.SetDetectedObjectCompleted.Call(4, true);
        }
    }

}