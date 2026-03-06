using System;
using Vector.CANoe.Runtime;
using Vector.CANoe.Threading;
using Vector.CANoe.TFS;

// Import communication model
using DataTypes;
using Participants;


[TestClass]
public class Tester
{
    // Check propagation of detected objects from LIDAR_Front endpoint to Dashboard endpoint 
    [Export]
    [TestCase("Test_Collision_Info_Front")]
    public static void Test_Collision_Info_Front()
    {
        uint[] object_distance_test_values = {100U, 90U, 80U, 70U, 60U, 50U, 40U, 30U, 20U, 10U, 0U,
                                              0U, 10U, 20U, 30U, 40U, 50U, 60U, 70U, 80U, 90U, 100U};

        Report.TestCaseDescription("Check propagation of detected objects from LIDAR_Front endpoint to Dashboard endpoint");

        // Iterate classification enum values
        foreach (Object_Classification_Enum classification in Enum.GetValues(typeof(Object_Classification_Enum)))
        {
            foreach (uint distance in object_distance_test_values)
            {
                Execution.Wait(200);
                Report.TestStep("Propagate detected object", "Object: " + classification.ToString() + ", Distance: " + distance.ToString());
                LIDAR_Front.Object.Classification.SymbValue = classification;
                LIDAR_Front.Object.Distance = distance;
                // Wait for setter call from Drive_Master to Dashboard
                var wait_result = Dashboard.Collision_Info_Front.Set.WaitForNextCall(100);
                // Check for expected value (further checks omitted in this example)
                if (wait_result.Call.value.Distance != LIDAR_Front.Object.Distance)
                {
                    Report.TestStepFail("Check distance", "Unexpected value received: " + wait_result.Call.value.Distance.Value.ToString());
                }
                else
                {
                    Report.TestStepPass("Check distance", "Expected value received: " + wait_result.Call.value.Distance.Value.ToString());
                }
            }
        }
        LIDAR_Front.Object.Classification.SymbValue = Object_Classification_Enum.NO_OBJECT;
    }


    // Check propagation of detected objects from LIDAR_Rear endpoint to Dashboard endpoint 
    [Export]
    [TestCase("Test_Collision_Info_Rear")]
    public static void Test_Collision_Info_Rear()
    {
        uint[] object_distance_test_values = {100U, 90U, 80U, 70U, 60U, 50U, 40U, 30U, 20U, 10U, 0U,
                                              0U, 10U, 20U, 30U, 40U, 50U, 60U, 70U, 80U, 90U, 100U};

        Report.TestCaseDescription("Check propagation of detected objects from LIDAR_Rear endpoint to Dashboard endpoint");

        // Iterate classification enum values
        foreach (Object_Classification_Enum classification in Enum.GetValues(typeof(Object_Classification_Enum)))
        {
            foreach (uint distance in object_distance_test_values)
            {
                Execution.Wait(200);
                Report.TestStep("Propagate detected object", "Object: " + classification.ToString() + ", Distance: " + distance.ToString());
                LIDAR_Rear.Object.Classification.SymbValue = classification;
                LIDAR_Rear.Object.Distance = distance;
                // Wait for setter call from Drive_Master to Dashboard
                var wait_result = Dashboard.Collision_Info_Rear.Set.WaitForNextCall(100);
                // Check for expected value (further checks omitted in this example)
                if (wait_result.Call.value.Distance.Value != LIDAR_Rear.Object.Distance)
                {
                    Report.TestStepFail("Check distance", "Unexpected value received: " + wait_result.Call.value.Distance.Value.ToString());
                }
                else
                {
                    Report.TestStepPass("Check distance", "Expected value received: " + wait_result.Call.value.Distance.Value.ToString());
                }
            }
        }
        LIDAR_Rear.Object.Classification.SymbValue = Object_Classification_Enum.NO_OBJECT;
    }


    // Check propagation of navigation data from Backend endpoint to Dashboard endpoint
    [Export]
    [TestCase("Test_Navigation_Data")]
    public static void Test_Navigation_Data()
    {
        Report.TestCaseDescription("Check propagation of navigation data from Backend endpoint to Dashboard endpoint");

        Tuple<string, uint>[] destinations = {  Tuple.Create("Weilimdorf", 10U),
                                                Tuple.Create("Muenchen", 200U),
                                                Tuple.Create("Dortmund", 400U),
                                                Tuple.Create("Hannover", 500U),
                                                Tuple.Create("Berlin", 700U)  };

        Tuple<string, Category_Enum>[] pois =  {  Tuple.Create("Roadworks", Category_Enum.WARN),
                                                  Tuple.Create("Restaurant", Category_Enum.INFO),
                                                  Tuple.Create("Traffic Jam", Category_Enum.WARN),
                                                  Tuple.Create("Gas Station", Category_Enum.INFO),
                                                  Tuple.Create("Detour", Category_Enum.WARN)  };

        foreach (var destination in destinations)
        {
            var navigation_info = Navigation_Info.CreateInstance();
            navigation_info.MainDestination.Destination = destination.Item1;
            navigation_info.MainDestination.Distance = destination.Item2;

            navigation_info.POIs.Length = 3;
            Random random = new Random();
            uint poi_index = (uint)random.Next(pois.Length);

            for (int j = 0; j < navigation_info.POIs.Length; j++)
            {
                navigation_info.POIs[j].Distance = ((uint)j * 10U) + poi_index;
                navigation_info.POIs[j].MessageStr = pois[poi_index].Item1;
                navigation_info.POIs[j].Category.Value = pois[poi_index].Item2;
            }
            Backend.navigation_info.MainDestination.Assign(navigation_info.MainDestination);
            Backend.navigation_info.POIs.Assign(navigation_info.POIs);

            // wait for setter call from Dashboard 
            var wait_result = Dashboard.Navigation_Info.Set.WaitForNextCall(2000);
            // Check for expected value
            if (wait_result.Call.value.MainDestination.Distance != navigation_info.MainDestination.Distance)
            {
                Report.TestStepFail("Check distance", "Unexpected value received: " + wait_result.Call.value.MainDestination.Distance.ToString());
            }
            else
            {
                Report.TestStepPass("Check distance", "Expected value received: " + wait_result.Call.value.MainDestination.Distance.ToString());
            }
        }
    }


    // Check propagation of mirror data from Mirror_Driver endpoint to Console endpoint
    [Export]
    [TestCase("Test_Mirror_Driver")]
    public static void Test_Mirror_Driver()
    {
        Report.TestCaseDescription("Check propagation of mirror data from Mirror_Driver endpoint to Console endpoint");

        foreach (uint mirror_folded in Enum.GetValues(typeof(Mirror_Folded)))
        {
            foreach (uint mirror_heat in Enum.GetValues(typeof(Mirror_Heat)))
            {
                foreach (uint mirror_direction in Enum.GetValues(typeof(Mirror_Direction_Enum)))
                {
                    using var mirror_parameter = MirrorParametersStruct.CreateInstance();
                    mirror_parameter.Direction = (Mirror_Direction_Enum)mirror_direction;
                    mirror_parameter.Heat_OnOff = (Mirror_Heat)mirror_heat;
                    mirror_parameter.Mirror_Folded = (Mirror_Folded)mirror_folded;

                    var wait_result_console = Participants.Console.Mirror_Driver.AdjustMirror.CallAsync(mirror_parameter);

                    if (wait_result_console.MirrorParameter.Direction != (Mirror_Direction_Enum)mirror_direction)
                    {
                        Report.TestStepFail("Check direction", "Expected value received: " + mirror_direction.ToString());
                    }
                    else
                    {
                        Report.TestStepPass("Check direction", "Expected value received: " + mirror_direction.ToString());
                    }
                }
            }
        }
    }
}
