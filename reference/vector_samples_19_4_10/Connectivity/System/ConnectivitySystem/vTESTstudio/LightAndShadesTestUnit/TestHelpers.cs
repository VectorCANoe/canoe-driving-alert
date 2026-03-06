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
public class RoomControlTester
{
    [Export]
    public static void setLight(LightSimulation.Control.buttonStateLight state)
    {
        LightSimulation.Control.manualControl.buttonLight.ImplValue = (uint)state;
    }

    [Export]
    public static void checkLightState(int expected)
    {
        var expectedBool = expected == 0 ? false : true;
        if (expectedBool != LightSimulation.RoomActions.output.roomData.lights)
        {
            Report.TestStepFail("Lights", "Light is not in the expected state");
        }
        else
        {
            Report.TestStepPass("Lights", "Light is in the expected state");
        }
    }

    [Export]
    public static void setShades_east(LightSimulation.Control.buttonStateShades state)
    {
        LightSimulation.Control.manualControl.buttonShades_east.ImplValue = (uint)state;
    }

    [Export]
    public static void setShades_west(LightSimulation.Control.buttonStateShades state)
    {
        LightSimulation.Control.manualControl.buttonShades_west.ImplValue = (uint)state;
    }
}