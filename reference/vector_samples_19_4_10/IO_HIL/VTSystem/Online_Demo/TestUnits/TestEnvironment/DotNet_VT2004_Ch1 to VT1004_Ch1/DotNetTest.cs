/*
 * Copyright (c) Vector Informatik GmbH. All rights reserved.
 * 
 * Source file description:
 * This file shows how to use the VTSystem from .NET testcases.
 * 
 * Creation date and author:
 * 2010-10-22 Brock, Boris (Bbr)
 * */

using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Threading;
using Vector.CANoe.TFS;
using Vector.CANoe.VTS;
using NetworkDB;

[TestClass]
public class DotNetTest
{
    /// Testcase for voltage generation and measurement

	[Export]
    [TestCase]
    public static void VoltageGenerationAndMeasurementTest(double voltage)
    {
        // Interface to the VTSystem modules and channels
        IVTSystem vts = VTSystem.Instance;


        // Add testcase name and description
        Vector.CANoe.TFS.Report.TestCaseTitle("Voltage generation and measurement test at " + voltage.ToString() + " Volts.");
        Vector.CANoe.TFS.Report.TestCaseDescription("Testing voltage generation and measurement at " + voltage.ToString() + " Volts.");


        // Step 1: Activate voltage generation on the VT2004 module (channel 1)

        // Get the channel interfaces
        IVT2004Channel Stimulus_Ch1 = vts.GetChannel("Stimulus_Ch1") as IVT2004Channel;
        IVT1004Channel Load_Ch1 = vts.GetChannel("Load_Ch1") as IVT1004Channel;

        // Set simulation mode to voltage generation and the output curve type to be a constant
        Stimulus_Ch1.SetStimulationMode(StimulationMode.Voltage, CurveType.Constant);

        // Choose an output voltage
        Stimulus_Ch1.Voltage.Value = voltage;

        // Start generating the signal
        Stimulus_Ch1.StartStimulation();


        // Step 2: perform the actual test

        // Wait 100 ms to make sure the above settings take effect
        Vector.CANoe.Threading.Execution.Wait(100);

        // Check if a voltage of +- 1V around given parameter can be measured
        if (Math.Abs(voltage - Load_Ch1.Cur.Value) > 1.0)
        {
            // Test failed. No voltage or a wrong voltage was measured
            Vector.CANoe.TFS.Report.TestStepFail("No voltage or a wrong voltage (" + Load_Ch1.Cur.Value + "V) was measured");
        }//end if
        else
        {
            Vector.CANoe.TFS.Report.TestStepPass("");
        }
    }


    /// Testcase for PWM generation and measurement
    [Export]
    [TestCase]
    public static void PWMGenerationAndMeasurement(double frequency)
    {
        // Interface to the VTSystem modules and channels
        IVTSystem vts = VTSystem.Instance;  

        // Add testcase name and description
        Vector.CANoe.TFS.Report.TestCaseTitle("PWM generation and measurement test at " + frequency.ToString() + " Hz.");
        Vector.CANoe.TFS.Report.TestCaseDescription("Testing PWM generation and measurement at " + frequency.ToString() + " Hz.");

        // Step 1: Activate PWM generation on the VT2004 module (channel 1)

        // Get the channel interfaces
        IVT2004Channel Stimulus_Ch1 = vts.GetChannel("Stimulus_Ch1") as IVT2004Channel;
        IVT1004Channel Load_Ch1 = vts.GetChannel("Load_Ch1") as IVT1004Channel;

        // Set simulation mode to voltage generation and the output curve type to be a PWM signal
        Stimulus_Ch1.SetStimulationMode(StimulationMode.Voltage, CurveType.PWM);


        // Specify the PWM signal (frequency, low and high voltage, duty cycle)
        Stimulus_Ch1.PWMFreq.Value = frequency;
        Stimulus_Ch1.PWMVoltageHigh.Value = 5.0;
        Stimulus_Ch1.PWMVoltageLow.Value = 0.0;
        Stimulus_Ch1.PWMDC.Value = 50;

        // Start generating the signal
        Stimulus_Ch1.StartStimulation();


        // Step 2: Activate PWM measurement on the VT1004 module (channel 1)

        // Set the threshold voltage to 3V
        Load_Ch1.PWMThreshold.Value = 3.0;

        // Set the duration of each measurement
        Load_Ch1.PWMMeasurementDuration.Value = 0.05;


        // Step 3: perform the actual test

        // Wait 500 ms to make sure the above settings take effect
        Vector.CANoe.Threading.Execution.Wait(500);


        // Check if the right frequency can be measured (with a tolerance of 5%)
        double allowedDeviation = 0.05;
        if ((frequency > Load_Ch1.PWMFreq.Value * (1.0 + allowedDeviation)) ||
            (frequency < Load_Ch1.PWMFreq.Value * (1.0 - allowedDeviation)))
        {
            // Test failed. No frequency or a wrong frequency was measured
            Vector.CANoe.TFS.Report.TestStepFail("No frequency or a wrong frequency (" + Load_Ch1.PWMFreq.Value.ToString() + "Hz) was measured");
        }//end if
        else
        {
            Vector.CANoe.TFS.Report.TestStepPass("");
        }
    }
}
