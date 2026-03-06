using System;
using Vector.Tools;
using Vector.CANoe.Runtime;


// Import communication model
using DataTypes;
using Participants;



public class Drive_Master_Model : MeasurementScript
{
    // Update Dashboard with velocity
    [OnChange(typeof(SysVars.Vehicle.Velocity))]
    public void OnVelocity()
    {        
        Drive_Master.Dashboard.Velocity_Info.Set.CallAsync(SysVars.Vehicle.Velocity.Value);
    }
    

    // Update Dashboard with event data received from LIDAR_Front
    [OnUpdate((LIDAR_Front.MemberIDs.Object))]
    public void OnObjectFront()
    {
        using var collision_info = Collision_Info.CreateInstance();
        if (Drive_Master.LIDAR_Front.Object.Distance <= 100)
        {
            if (Drive_Master.LIDAR_Front.Object.Classification.SymbValue == Object_Classification_Enum.VEHICLE)
            {
                collision_info.MessageStr = "Vehicle: " + Drive_Master.LIDAR_Front.Object.Distance.ToString() + "m";
                collision_info.Lamp.Value = 1;
                collision_info.Warn_Level.Value = 11 - (uint)(Math.Floor(Drive_Master.LIDAR_Front.Object.Distance * 0.1));
            }
            else if (Drive_Master.LIDAR_Front.Object.Classification.SymbValue == Object_Classification_Enum.OBSTACLE)
            {
                collision_info.MessageStr = "Obstacle: " + Drive_Master.LIDAR_Front.Object.Distance.ToString() + "m";
                collision_info.Lamp.Value = 1;
                collision_info.Warn_Level.Value = 11 - (uint)(Math.Floor(Drive_Master.LIDAR_Front.Object.Distance * 0.1));
            }
            else if (Drive_Master.LIDAR_Front.Object.Classification.SymbValue == Object_Classification_Enum.PEDESTRIAN)
            {
                collision_info.MessageStr = "Pedestrian: " + Drive_Master.LIDAR_Front.Object.Distance.ToString() + "m";
                collision_info.Lamp.Value = 1;
                collision_info.Warn_Level.Value = 11 - (uint)(Math.Floor(Drive_Master.LIDAR_Front.Object.Distance * 0.1));
            }
            else if (Drive_Master.LIDAR_Front.Object.Classification.SymbValue == Object_Classification_Enum.NO_OBJECT)
            {
                collision_info.MessageStr = "";
                collision_info.Lamp.Value = 0;
                collision_info.Warn_Level.Value = 0;
            }
        }
        else
        {
            collision_info.Warn_Level.Value = 0;
        } 
        collision_info.Distance.Value = Drive_Master.LIDAR_Front.Object.Distance;
        Drive_Master.Dashboard.Collision_Info_Front.Set.CallAsync(collision_info);
    }


    // Update Dashboard with event data received from LIDAR_Rear
    [OnUpdate((LIDAR_Rear.MemberIDs.Object))]
    public void OnObjectRear()
    {
        using var collision_info = Collision_Info.CreateInstance();
        if (Drive_Master.LIDAR_Rear.Object.Distance <= 100)
        {
            if (Drive_Master.LIDAR_Rear.Object.Classification.SymbValue == Object_Classification_Enum.VEHICLE)
            {
                collision_info.MessageStr = "Vehicle: " + Drive_Master.LIDAR_Rear.Object.Distance.ToString() + "m";
                collision_info.Lamp.Value = 1;
                collision_info.Warn_Level.Value = 11 - (uint)(Math.Floor(Drive_Master.LIDAR_Rear.Object.Distance * 0.1));
            }
            else if (Drive_Master.LIDAR_Rear.Object.Classification.SymbValue == Object_Classification_Enum.OBSTACLE)
            {
                collision_info.MessageStr = "Obstacle: " + Drive_Master.LIDAR_Rear.Object.Distance.ToString() + "m";
                collision_info.Lamp.Value = 1;
                collision_info.Warn_Level.Value = 11 - (uint)(Math.Floor(Drive_Master.LIDAR_Rear.Object.Distance * 0.1));
            }
            else if (Drive_Master.LIDAR_Rear.Object.Classification.SymbValue == Object_Classification_Enum.PEDESTRIAN)
            {
                collision_info.MessageStr = "Pedestrian: " + Drive_Master.LIDAR_Rear.Object.Distance.ToString() + "m";
                collision_info.Lamp.Value = 1;
                collision_info.Warn_Level.Value = 11 - (uint)(Math.Floor(Drive_Master.LIDAR_Rear.Object.Distance * 0.1));
            }
            else if (Drive_Master.LIDAR_Rear.Object.Classification.SymbValue == Object_Classification_Enum.NO_OBJECT)
            {
                collision_info.MessageStr = "";
                collision_info.Lamp.Value = 0;
                collision_info.Warn_Level.Value = 0;
            }
        }
        else
        {
            collision_info.Warn_Level.Value = 0;
        }      
        collision_info.Distance.Value = Drive_Master.LIDAR_Rear.Object.Distance;
        Drive_Master.Dashboard.Collision_Info_Rear.Set.CallAsync(collision_info);
    }
    

    //Update Navigation Information with data from Backend
    [OnTimer(1000)]
    public void OnNavigationTimer()
    {
        using var navigation_info = Navigation_Info.CreateInstance();
        var result = Drive_Master.Backend.navigation_info;
        navigation_info.MainDestination.Destination = result.MainDestination.Destination + ": " + result.MainDestination.Distance.Value.ToString() + "km";
        navigation_info.MainDestination.Distance.Value = result.MainDestination.Distance.Value;
        navigation_info.POIs.Length = result.POIs.Length;

        for (int i = 0; i < navigation_info.POIs.Length; i++)
        {
            navigation_info.POIs[i].Category.Value = result.POIs[i].Category;
            if (result.POIs[i].Category.Value > 0)
            {
                navigation_info.POIs[i].MessageStr = result.POIs[i].MessageStr + ": " + result.POIs[i].Distance.Value.ToString() + "km";
            }
            else
            {
                navigation_info.POIs[i].MessageStr = "";
            }
        }
        Drive_Master.Dashboard.Navigation_Info.Set.CallAsync(navigation_info);
    }
 

    // Reagiere auf Method Call Control
    [OnCall(Mirror_Driver.MemberIDs.AdjustMirror)]
    public string AdjustMirror(MirrorParametersStruct MirrorParameter)
    {
        //0:unfolded 
        //1:folded
        if (0 == MirrorParameter.Mirror_Folded.Value)
            SysVars.MirrorPanel.AdjustAndFold.Fold.Value = 0;
        else
            SysVars.MirrorPanel.AdjustAndFold.Fold.Value = 1;

        //0:heat is off
        //1:heat is on
        if (0 == MirrorParameter.Heat_OnOff.Value)
            SysVars.MirrorPanel.Heat.Value = 0;
        else
            SysVars.MirrorPanel.Heat.Value = 1;

        //save the valid direction in a system variable
        SysVars.MirrorPanel.AdjustAndFold.AdjustPosition.Value = MirrorParameter.Direction.ImplValue;
        if (1 == SysVars.MirrorPanel.AdjustAndFold.Fold.Value) //mirror is fold
        {
            SysVars.MirrorPanel.MirrorSwitch.Value = 0;
            return "Mirror is folded in.";
        }
        else //mirror is unfold - show the correct mirror position
        {
            SysVars.MirrorPanel.MirrorSwitch.Value = SysVars.MirrorPanel.AdjustAndFold.AdjustPosition.Value + 1;
            return "ok";
        }
    }    
} 