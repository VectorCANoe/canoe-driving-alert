using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;

using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;


public class InputMeasuredECG : MeasurementScript
{
    private static bool simulationModelActive = false;

    private static bool wasSimulationWithoutArrhytmiaRunning = false;
    private static bool wasSimulationWithArrhythmiaRunning = false;


    //Variables for ECG data with arrhythmia
    private static Timer sampleTimerWithArrhythmia = null;
    private static int[] ecg_with_arrhytmia_recorded_samples_array = null;

    private static int inputFrequencyECGWithArrhythmia = 0;
    private static int ecg_sample_offset_with_arrhythmia = 0;

    //Variables for ECG data without arrhythmia
    private static Timer sampleTimerWithoutArrhythmia = null;
    private static int[] ecg_without_arrhytmia_recorded_samples_array = null;

    private static int inputFrequencyECGWithoutArrhythmia = 0;
    private static int ecg_sample_offset_without_arrhythmia = 0;

    //Variables for ECG emergency data snippet

    private static Timer sampleTimerEmergency = null;
    private static int[] ecg_emergency_sample_array = null;

    private const int inputFrequencyEmergencySnippet = 200;
    private static int ecg_emergency_sample_offset = 0;

    /// <summary>
    /// Called before measurement start to perform necessary initializations,
    /// e.g. to create objects. During measurement, few additional objects
    /// should be created to prevent garbage collection runs in time-critical
    /// simulations.
    /// </summary>
    public override void Initialize()
    {
        ecg_sample_offset_with_arrhythmia = 0;
        string ecg_sample_record_with_arrhythmia_file_text = System.IO.File.ReadAllText(@"TestData/Input/SampleData_200_Hz/Record13.txt");
        string[] splitted_sample_record_with_arrhythmia_string = ecg_sample_record_with_arrhythmia_file_text.Split(',');
        ecg_with_arrhytmia_recorded_samples_array = Array.ConvertAll(splitted_sample_record_with_arrhythmia_string, int.Parse);
        string input_freq_string_with_arrhythmia = "200";
        inputFrequencyECGWithArrhythmia = int.Parse(input_freq_string_with_arrhythmia);


        simulationModelActive = false;

        sampleTimerWithArrhythmia = new Timer(sampleTimerHandlerWithArrhythmia);
        sampleTimerWithArrhythmia.AutoReset = true;
        double time_between_samples_in_ms_with_arrhythmia = ((double)1 / inputFrequencyECGWithArrhythmia) * 1000;
        sampleTimerWithArrhythmia.Interval = new TimeSpan(0, 0, 0, 0, (int)(time_between_samples_in_ms_with_arrhythmia + 0.5));


        ecg_sample_offset_without_arrhythmia = 0;
        string ecg_sample_record_without_arrhythmia_file_text = System.IO.File.ReadAllText(@"TestData/Input/SampleData_200_Hz/Record2.txt");
        string[] splitted_sample_record_without_arrhythmia_string = ecg_sample_record_without_arrhythmia_file_text.Split(',');
        ecg_without_arrhytmia_recorded_samples_array = Array.ConvertAll(splitted_sample_record_without_arrhythmia_string, int.Parse);
        string input_freq_string_without_arrhythmia = "200";
        inputFrequencyECGWithoutArrhythmia = int.Parse(input_freq_string_without_arrhythmia);


        sampleTimerWithoutArrhythmia = new Timer(sampleTimerHandlerWithoutArrhythmia);
        sampleTimerWithoutArrhythmia.AutoReset = true;
        double time_between_samples_in_ms_without_arrhythmia = ((double)1 / inputFrequencyECGWithoutArrhythmia) * 1000;
        sampleTimerWithoutArrhythmia.Interval = new TimeSpan(0, 0, 0, 0, (int)(time_between_samples_in_ms_without_arrhythmia + 0.5));

        ecg_emergency_sample_offset = 0;
        string ecg_emergency_sample_record_file_text = System.IO.File.ReadAllText(@"TestData/Input/Artificial_ECG_Data_200_Hz/Record13_Snippet.txt");
        string[] splitted_emergency_sample_record_string = ecg_emergency_sample_record_file_text.Split(',');
        ecg_emergency_sample_array = Array.ConvertAll(splitted_emergency_sample_record_string, int.Parse);

        sampleTimerEmergency = new Timer(sampleTimerHandlerEmergencySnippet);
        sampleTimerEmergency.AutoReset = true;
        double time_between_samples_emergency = ((double)1 / inputFrequencyEmergencySnippet) * 1000;
        sampleTimerEmergency.Interval = new TimeSpan(0, 0, 0, 0, (int)(time_between_samples_emergency + 0.5));
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

    [OnChange(SampleDataControl.SampleDataControl.MemberIDs.startSendingSampleDataToSUT)]
    public void startSampleInputToSUT()
    {
        if (!simulationModelActive)
        {
            simulationModelActive = true;
        }
        else
        {
            return;
        }

        sampleTimerEmergency.Stop();

        SampleDataControl.SampleDataControl.isEmergencySimulationRunning = false;

        if (SampleDataControl.SampleDataControl.simulationECGType.ImplValue == (uint)SampleDataControl.ECGType.With_Arrhythmia)
        {
            wasSimulationWithArrhythmiaRunning = true;
            sampleTimerWithArrhythmia.Start();
        }
        else
        {
            wasSimulationWithoutArrhytmiaRunning = true;
            sampleTimerWithoutArrhythmia.Start();
        }
    }

    [OnChange(SampleDataControl.SampleDataControl.MemberIDs.stopSendingSampleDataToSUT)]
    public void stopSampleInputToSUT()
    {
        if (simulationModelActive)
        {
            simulationModelActive = false;
        }
        else
        {
            return;
        }
        wasSimulationWithArrhythmiaRunning = false;
        wasSimulationWithoutArrhytmiaRunning = false;
        sampleTimerWithArrhythmia.Stop();
        sampleTimerWithoutArrhythmia.Stop();
    }

    [OnChange(SampleDataControl.SampleDataControl.MemberIDs.simulationECGType)]
    public void changeSimulationMode()
    {
        if (!simulationModelActive && !SampleDataControl.SampleDataControl.isEmergencySimulationRunning) return;

        if (SampleDataControl.SampleDataControl.simulationECGType.ImplValue == 0)
        {
            sampleTimerWithArrhythmia.Stop();
            sampleTimerEmergency.Stop();
            simulationModelActive = true;
            SampleDataControl.SampleDataControl.isEmergencySimulationRunning = false;
            wasSimulationWithArrhythmiaRunning = false;
            wasSimulationWithoutArrhytmiaRunning = true;
            sampleTimerWithoutArrhythmia.Start();
        }
        else
        {
            sampleTimerWithoutArrhythmia.Stop();
            sampleTimerEmergency.Stop();
            simulationModelActive = true;
            SampleDataControl.SampleDataControl.isEmergencySimulationRunning = false;
            wasSimulationWithArrhythmiaRunning = true;
            wasSimulationWithoutArrhytmiaRunning = false;
            sampleTimerWithArrhythmia.Start();
        }
    }


    [OnChange(SampleDataControl.SampleDataControl.MemberIDs.simulateEmergency)]
    public void simulateEmergency()
    {
        sampleTimerWithArrhythmia.Stop();
        sampleTimerWithoutArrhythmia.Stop();
        simulationModelActive = false;
        SampleDataControl.SampleDataControl.isEmergencySimulationRunning = true;

        sampleTimerEmergency.Start();
    }

    [OnChange(SampleDataControl.SampleDataControl.MemberIDs.stopSimulatingEmergency)]
    public void stopSimulateEmergency()
    {
        SampleDataControl.SampleDataControl.isEmergencySimulationRunning = false;
        sampleTimerEmergency.Stop();

        if (wasSimulationWithArrhythmiaRunning)
        {
            simulationModelActive = true;
            sampleTimerWithArrhythmia.Start();
            return;
        }

        if (wasSimulationWithoutArrhytmiaRunning)
        {
            simulationModelActive = true;
            sampleTimerWithoutArrhythmia.Start();
            return;
        }
    }


    public static void sampleTimerHandlerWithArrhythmia(object sender, ElapsedEventArgs e)
    {
        if (!simulationModelActive) { return; }
        if (ecg_sample_offset_with_arrhythmia < ecg_with_arrhytmia_recorded_samples_array.Length)
        {

            //Sending ECG sample value
            SmartECG.SmartECG_IO.ecgAmplitude = ecg_with_arrhytmia_recorded_samples_array[ecg_sample_offset_with_arrhythmia];

            ecg_sample_offset_with_arrhythmia++;

        }
        else
        {
            ecg_sample_offset_with_arrhythmia = 0;
            SmartECG.SmartECG_IO.ecgAmplitude = ecg_with_arrhytmia_recorded_samples_array[ecg_sample_offset_with_arrhythmia];

            ecg_sample_offset_with_arrhythmia++;
        }
    }

    public static void sampleTimerHandlerWithoutArrhythmia(object sender, ElapsedEventArgs e)
    {
        if (!simulationModelActive) { return; }
        if (ecg_sample_offset_without_arrhythmia < ecg_without_arrhytmia_recorded_samples_array.Length)
        {

            //Sending ECG sample value
            SmartECG.SmartECG_IO.ecgAmplitude = ecg_without_arrhytmia_recorded_samples_array[ecg_sample_offset_without_arrhythmia];

            ecg_sample_offset_without_arrhythmia++;
        }
        else
        {
            ecg_sample_offset_without_arrhythmia = 0;
            SmartECG.SmartECG_IO.ecgAmplitude = ecg_without_arrhytmia_recorded_samples_array[ecg_sample_offset_without_arrhythmia];

            ecg_sample_offset_without_arrhythmia++;
        }
    }

    public static void sampleTimerHandlerEmergencySnippet(object sender, ElapsedEventArgs e)
    {
        if (ecg_emergency_sample_offset < ecg_emergency_sample_array.Length)
        {

            //Sending ECG sample value
            SmartECG.SmartECG_IO.ecgAmplitude = ecg_emergency_sample_array[ecg_emergency_sample_offset];

            ecg_emergency_sample_offset++;
        }
        else
        {
            ecg_emergency_sample_offset = 0;
            SmartECG.SmartECG_IO.ecgAmplitude = ecg_emergency_sample_array[ecg_emergency_sample_offset];
            ecg_emergency_sample_offset++;
        }
    }
}