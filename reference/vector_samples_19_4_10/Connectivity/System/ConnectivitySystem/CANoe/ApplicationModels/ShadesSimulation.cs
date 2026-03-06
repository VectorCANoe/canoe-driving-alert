using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class ShadesSimulation : MeasurementScript
{
    [OnUpdate(LightSimulation.RoomActions.output.MemberIDs.roomData)]
    public void animateShades()
    {
        if (LightSimulation.RoomActions.output.roomData.shades_east)
        {
            closeShadesEast();
        }
        if (!LightSimulation.RoomActions.output.roomData.shades_east)
        {
            openShadesEast();
        }
        if (LightSimulation.RoomActions.output.roomData.shades_west)
        {
            closeShadesWest();
        }
        if (!LightSimulation.RoomActions.output.roomData.shades_west)
        {
            openShadesWest();
        }
    }

    private const int numberOfShadeStates = 9;
    private TimeSpan animationTimeSpan = new TimeSpan(0, 0, 0, 0, 50);

    private Timer animationTimerEastClose = null;
    private int numberOfStepsToCloseEast = 0;

    private Timer animationTimerEastOpen = null;
    private int numberOfStepsToOpenEast = 0;

    private Timer animationTimerWestClose = null;
    private int numberOfStepsToCloseWest = 0;

    private Timer animationTimerWestOpen = null;
    private int numberOfStepsToOpenWest = 0;

    void closeShadesEast()
    {
        if (animationTimerEastClose == null && LightSimulation.RoomActions.output.shadesEastAnimationState.Value < numberOfShadeStates - 1)
        {
            animationTimerEastClose = new Timer(this.closeShadesEastByOneStep);
            animationTimerEastClose.Interval = animationTimeSpan;
            animationTimerEastClose.Start();
        }
    }

    void closeShadesEastByOneStep(object o, ElapsedEventArgs e)
    {
        if (numberOfStepsToCloseEast < numberOfShadeStates - 1 && LightSimulation.RoomActions.output.shadesEastAnimationState.Value < numberOfShadeStates - 1)
        {
            ++LightSimulation.RoomActions.output.shadesEastAnimationState.Value;
            ++numberOfStepsToCloseEast;
        }
        else
        {
            animationTimerEastClose.Stop();
            animationTimerEastClose = null;
            numberOfStepsToCloseEast = 0;
        }
    }

    void openShadesEast()
    {
        if (animationTimerEastOpen == null && LightSimulation.RoomActions.output.shadesEastAnimationState.Value > 0)
        {
            animationTimerEastOpen = new Timer(this.openShadesEastByOneStep);
            animationTimerEastOpen.Interval = animationTimeSpan;
            animationTimerEastOpen.Start();
        }
    }

    void openShadesEastByOneStep(object o, ElapsedEventArgs e)
    {
        if (numberOfStepsToOpenEast < numberOfShadeStates - 1 && LightSimulation.RoomActions.output.shadesEastAnimationState.Value > 0)
        {
            --LightSimulation.RoomActions.output.shadesEastAnimationState.Value;
            ++numberOfStepsToOpenEast;
        }
        else
        {
            animationTimerEastOpen.Stop();
            animationTimerEastOpen = null;
            numberOfStepsToOpenEast = 0;
        }
    }

    void closeShadesWest()
    {
        if (animationTimerWestClose == null && LightSimulation.RoomActions.output.shadesWestAnimationState.Value < numberOfShadeStates - 1)
        {
            animationTimerWestClose = new Timer(this.closeShadesWestByOneStep);
            animationTimerWestClose.Interval = animationTimeSpan;
            animationTimerWestClose.Start();
        }
    }

    void closeShadesWestByOneStep(object o, ElapsedEventArgs e)
    {
        if (numberOfStepsToCloseWest < numberOfShadeStates - 1 && LightSimulation.RoomActions.output.shadesWestAnimationState.Value < numberOfShadeStates - 1)
        {
            ++LightSimulation.RoomActions.output.shadesWestAnimationState.Value;
            ++numberOfStepsToCloseWest;
        }
        else
        {
            animationTimerWestClose.Stop();
            animationTimerWestClose = null;
            numberOfStepsToCloseWest = 0;
        }
    }

    void openShadesWest()
    {
        if (animationTimerWestOpen == null && LightSimulation.RoomActions.output.shadesWestAnimationState.Value > 0)
        {
            animationTimerWestOpen = new Timer(this.openShadesWestByOneStep);
            animationTimerWestOpen.Interval = animationTimeSpan;
            animationTimerWestOpen.Start();
        }
    }

    void openShadesWestByOneStep(object o, ElapsedEventArgs e)
    {
        if (numberOfStepsToOpenWest < numberOfShadeStates - 1 && LightSimulation.RoomActions.output.shadesWestAnimationState.Value > 0)
        {
            --LightSimulation.RoomActions.output.shadesWestAnimationState.Value;
            ++numberOfStepsToOpenWest;
        }
        else
        {
            animationTimerWestOpen.Stop();
            animationTimerWestOpen = null;
            numberOfStepsToOpenWest = 0;
        }
    }
}