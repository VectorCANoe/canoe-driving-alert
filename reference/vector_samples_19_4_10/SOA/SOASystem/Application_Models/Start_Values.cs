using System;
using Vector.Tools;
using Vector.CANoe.Runtime;

// Import communication model
using Participants;
using DataTypes;

public class Start_Values : MeasurementScript
{

    public override void Start()
    {
        // Set default values for backend navigation method
        Backend.navigation_info.MainDestination.Destination = "Weilimdorf";
        Backend.navigation_info.MainDestination.Distance.Value = 10;
        Backend.navigation_info.POIs.Length = 3;

        Backend.navigation_info.POIs[0].Category.SymbValue = Category_Enum.WARN;
        Backend.navigation_info.POIs[0].Distance.Value = 10;
        Backend.navigation_info.POIs[0].MessageStr = "Roadworks";

        Backend.navigation_info.POIs[1].Category.SymbValue = Category_Enum.INFO;
        Backend.navigation_info.POIs[1].Distance.Value = 20;
        Backend.navigation_info.POIs[1].MessageStr = "Gas Station";

        Backend.navigation_info.POIs[2].Category.SymbValue = Category_Enum.INFO;
        Backend.navigation_info.POIs[2].Distance.Value = 30;
        Backend.navigation_info.POIs[2].MessageStr = "Restaurant";

        // Set defaults for LIDAR providers
        LIDAR_Front.Object.Value.Distance.Value = 100;
        LIDAR_Front.Object.Value.Classification.SymbValue = Object_Classification_Enum.NO_OBJECT;
        LIDAR_Rear.Object.Value.Distance.Value = 100;
        LIDAR_Rear.Object.Value.Classification.SymbValue = Object_Classification_Enum.NO_OBJECT;
    }
}