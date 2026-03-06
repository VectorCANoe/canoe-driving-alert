using System;
using System.Collections.ObjectModel;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using Vector.CANoe.TFS;
using Vector.CANoe.VTS;

using System.Xml.Linq;
using System.Xml;
using System.Linq;
using System.IO;

[TestClass]
public class MyTestClass
{
    [Export]
    [TestFunction]
    public static void count_variations()
    {
        int count = SysPars.Roadworks_ParameterSet.GetStructList().Count;
        parameterVariation.totalIterations.Value = count - 1;
    }

    [Export]
    [TestFunction]
    public static void replace_parameters(int iteration, string scenarioPath)
    {
        var parameterSetStructList = SysPars.Roadworks_ParameterSet.GetStructList();
        var parameterSet = parameterSetStructList.ElementAt(iteration); ;
        Directory.GetCurrentDirectory();
        XDocument xdoc = XDocument.Load(scenarioPath);
        var parameterDeclarations = xdoc.Elements("OpenScenario").Single().Elements("ParameterDeclarations").Single().Elements();
        foreach (XElement parameter in parameterDeclarations)
        {
            if (parameter.Attribute("name").Value == "brake_target_speed")
            {
                parameter.Attribute("value").Value = parameterSet.brake_target_speed.GetValue().ToString();
            }

            if (parameter.Attribute("name").Value == "ego_initial_speed")
            {
                parameter.Attribute("value").Value = parameterSet.ego_initial_speed.GetValue().ToString();
            }
        }
        Report.TestStep("Performing variation " + (iteration + 1) + " of " + SysPars.Roadworks_ParameterSet.GetStructList().Count + ".");
        Report.TestStep("Ego Vehicle Initial Speed is : " + parameterSet.ego_initial_speed.GetValue().ToString() + " m/s");
        Report.TestStep("Brake Rarget Speed is : " + parameterSet.brake_target_speed.GetValue().ToString() + " m/s");
        xdoc.Save(scenarioPath);
    }
}