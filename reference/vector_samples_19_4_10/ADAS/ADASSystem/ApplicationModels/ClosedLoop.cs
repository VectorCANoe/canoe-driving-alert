using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class ClosedLoop : MeasurementScript
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

    /// <summary>Callback called on update of the ADAS algorithm output object</summary>
    [OnUpdate(OutputSimpleAlgorithm.MemberIDs.isWarningActive)]
    public void OnUpdateOutputSimpleAlgorithm()
    {
        if (OutputSimpleAlgorithm.isWarningActive.ImplValue == 1)
        {
            SingleTrack_DriverAssistanceCANoe.Parameters.DYNA4_Signal_Access.ExternalFunctionOutput.Active.Value_.Value = 1;

            // Send the values to the DYNA4 scenario -> Closed Loop 
            SingleTrack_DriverAssistanceCANoe.Parameters.DYNA4_Signal_Access.ExternalFunctionOutput.LimitsActive.Value_.Value = 1;
            SingleTrack_DriverAssistanceCANoe.Parameters.DYNA4_Signal_Access.ExternalFunctionOutput.LowerLimitBrakePress.Value_.Value = 0.75 * DYNA4ExternalFunctionInput.MaxMainBrakePress.Value;//  Brake
            SingleTrack_DriverAssistanceCANoe.Parameters.DYNA4_Signal_Access.ExternalFunctionOutput.UpperLimitTrq.Value_.Value = 0;    // No Throttle

        }
        else // Not Active
        {
            SingleTrack_DriverAssistanceCANoe.Parameters.DYNA4_Signal_Access.ExternalFunctionOutput.Active.Value_.Value = 0;
        }
    }
}