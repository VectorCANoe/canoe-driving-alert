// Created by Brock, Boris (visbbr), 2020-01-30
// Copyright (c) Vector Informatik GmbH. All rights reserved.

#region Usings

using System;
using System.Threading;
using ASAM.XIL.Implementation.Testbench.Common.ValueContainer;
using ASAM.XIL.Implementation.TestbenchFactory.Testbench;
using ASAM.XIL.Interfaces.Testbench.Common.ValueContainer;
using ASAM.XIL.Interfaces.Testbench.MAPort;

#endregion

namespace XilApiClient
{
  class Program
  {
    /// <summary>
    ///   This method shows how to obtain a list of all available variables in the current CANoe configuration.
    /// </summary>
    /// <param name="maPort">The MAPort representing CANoe</param>
    static void ExampleGetVariables(IMAPort maPort)
    {
      Console.WriteLine("The following variables are available in CANoe:");

      foreach (var variable in maPort.VariableNames)
        Console.WriteLine(" - " + variable);
    }

    /// <summary>
    ///   This method shows how to read from a system variable of type Integer.
    /// </summary>
    /// <param name="maPort">The MAPort representing CANoe</param>
    static void ExampleRead(IMAPort maPort)
    {
      Console.WriteLine("Reading values of Test::Variable1:");
      for (int i = 0; i < 5; i++)
      {
        var curValue = maPort.Read("Test::Variable1") as IFloatValue;
        Console.WriteLine(" - " + curValue.Value);

        Thread.Sleep(500);
      }
    }

    /// <summary>
    ///   This method shows how to write to a system variable of type Integer.
    /// </summary>
    /// <param name="maPort">The MAPort representing CANoe</param>
    static void ExampleWrite(IMAPort maPort)
    {
      Console.WriteLine("Writing value of Test::Variable2:");
      for (int i = 0; i <= 100; i += 25)
      {
        maPort.Write("Test::Variable2", new IntValue(i));
        Console.WriteLine(" - Writing " + i);

        Thread.Sleep(500);
      }
    }

    /// <summary>
    ///   Here the initialization, configuration and shut down of the XIL API is shown.
    /// </summary>
    static void Main()
    {
      // Instantiate test bench
      var testBenchFactory = new TestbenchFactory();
      var testBench = testBenchFactory.CreateVendorSpecificTestbench(
        "Vector", // Must be "Vector" in order to use the Vector CANoe server
        Environment.Is64BitProcess ? "CANoe64" : "CANoe32", // The bitness of this client decides which assemblies to use
        "2.1.0"); // Version of the API to use. Currently "2.1.0" is recommended for use with CANoe

      // Instantiate MAPort and load the Vector specific configuration file
      var maPort = testBench.MAPortFactory.CreateMAPort("Example MA Port");
      maPort.Configure(maPort.LoadConfiguration("..\\..\\..\\..\\XIL API Configuration\\VectorMAPortConfigLightRPC.xml"), false);

      // Start the measurement in CANoe
      maPort.StartSimulation();

      // Perform different operations via the XIL API
      ExampleGetVariables(maPort);
      ExampleRead(maPort);
      ExampleWrite(maPort);

      // Stop the measurement in CANoe and Shut down the XIL API
      maPort.StopSimulation();
      maPort.Disconnect();
      maPort.Dispose();

      // Keep console open until RETURN is pressed
      Console.WriteLine("Done. Press RETURN to exit...");
      Console.ReadLine();
    }
  }
}