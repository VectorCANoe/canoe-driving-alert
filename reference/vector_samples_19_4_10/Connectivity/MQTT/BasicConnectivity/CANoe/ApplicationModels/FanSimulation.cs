using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using NetworkDB;
using NetworkDB._SystemDataTypes;
using System.Collections.Generic;
using IServiceProvider = Vector.CANoe.Runtime.IServiceProvider;
using System.Diagnostics;
using System.Collections.Concurrent;
using System.IO;
using System.Text;

public class FanSimulation : MeasurementScript
{
    private const int mCountTemperatureSensors = 4;
    private long[] mLastTemperatureValues = new long[mCountTemperatureSensors];

    private Timer mFanSpeedAnimationTimer;

    private const int mMaxRpmFan = 6000; // 6000 min-1
    private const int mMinRpmFan = 0;    // 0 min-1

    private long mLastFanSpeed = 0;
    private long mCurrFanSpeed = 0;

    private long mLastAvgValue = 0;

    public override void Start()
    {
        for (int i = 0; i < mCountTemperatureSensors; ++i)
        {
            mLastTemperatureValues[i] = 0;
        }
        mLastAvgValue = ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value;
    }

    public void OnElapsedTimer(object sender, ElapsedEventArgs eventArgs)
    {
        int newState = ClimateSimulation.PanelSettings.PanelSetting.FanState.Value + 1;

        if (newState > 6 || newState < 0)
        {
            newState = 1;
        }
        ClimateSimulation.PanelSettings.PanelSetting.FanState.Value = newState;
    }

    private void ConfigureTimer()
    {
        if (mCurrFanSpeed == 0 && mFanSpeedAnimationTimer != null)
        {
            mFanSpeedAnimationTimer.Stop();
        }
        else if (mLastFanSpeed != mCurrFanSpeed || mFanSpeedAnimationTimer == null)
        {
            if (mCurrFanSpeed > 0)
            {
                double timeInterval = (60 * 1000) / mCurrFanSpeed;

                if (mFanSpeedAnimationTimer == null)
                {
                    mFanSpeedAnimationTimer = new Timer(new EventHandler<ElapsedEventArgs>(OnElapsedTimer))
                    {
                        AutoReset = true,
                        Interval = TimeSpan.FromMilliseconds(timeInterval)
                    };
                    mFanSpeedAnimationTimer.Start();
                }
                else
                {
                    mFanSpeedAnimationTimer.Stop();
                    mFanSpeedAnimationTimer.Interval = TimeSpan.FromMilliseconds(timeInterval);
                    mFanSpeedAnimationTimer.Start();
                }
            }
        }

        mLastFanSpeed = mCurrFanSpeed;
    }

    private void CalculateAvg()
    {
        long avgTemperature = 0;

        for (int i = 0; i < mCountTemperatureSensors; ++i)
        {
            avgTemperature += mLastTemperatureValues[i];
        }

        avgTemperature /= mCountTemperatureSensors;

        ClimateSimulation.FanSimulation.Fan1.ProvidedAvgTemperature.Value = avgTemperature;
    }

    private void CalculateNewRotationSpeed()
    {
        long diff = 0;

        if (ClimateSimulation.FanSimulation.Fan1.ProvidedAvgTemperature.Value > ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value)
        {
            diff = ClimateSimulation.FanSimulation.Fan1.ProvidedAvgTemperature.Value - mLastAvgValue;
            mCurrFanSpeed += (diff * 150);
            mLastAvgValue = ClimateSimulation.FanSimulation.Fan1.ProvidedAvgTemperature.Value;
            ClimateSimulation.FanSimulation.Fan1.ProvidedRotationSpeed.Value = mCurrFanSpeed;
        }
        else
        {
            ClimateSimulation.FanSimulation.Fan1.ProvidedRotationSpeed.Value = 0;
            mCurrFanSpeed = 0;
            mLastAvgValue = ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value;
        }
    }

    [OnUpdate(ClimateSimulation.FanSimulation.Fan1.MemberIDs.ConsumedTemperature1)]
    public void OnConsumedTemperatureMemberUpdated()
    {
        mLastTemperatureValues[0] = ClimateSimulation.FanSimulation.Fan1.ConsumedTemperature1.Value;
        CalculateAvg();
        CalculateNewRotationSpeed();
        ConfigureTimer();
    }

    [OnUpdate(ClimateSimulation.FanSimulation.Fan1.MemberIDs.ConsumedTemperature2)]
    public void OnConsumedTemperatureMemberUpdated1()
    {
        mLastTemperatureValues[1] = ClimateSimulation.FanSimulation.Fan1.ConsumedTemperature2.Value;
        CalculateAvg();
        CalculateNewRotationSpeed();
        ConfigureTimer();
    }

    [OnUpdate(ClimateSimulation.FanSimulation.Fan1.MemberIDs.ConsumedTemperature3)]
    public void OnConsumedTemperatureMemberUpdated2()
    {
        mLastTemperatureValues[2] = ClimateSimulation.FanSimulation.Fan1.ConsumedTemperature3.Value;
        CalculateAvg();
        CalculateNewRotationSpeed();
        ConfigureTimer();
    }

    [OnUpdate(ClimateSimulation.FanSimulation.Fan1.MemberIDs.ConsumedTemperature4)]
    public void OnConsumedTemperatureMemberUpdated3()
    {
        mLastTemperatureValues[3] = ClimateSimulation.FanSimulation.Fan1.ConsumedTemperature4.Value;
        CalculateAvg();
        CalculateNewRotationSpeed();
        ConfigureTimer();
    }
}


