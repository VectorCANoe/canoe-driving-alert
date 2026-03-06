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

public class TemperatureSimulation : MeasurementScript
{
    private const int INC_TEMP_COUNTER = 4;
    private const int DEC_TEMP_COUNTER = 2;

    private Timer mPublishAnimationTimer;
    private Timer mAutomaticModeTimer;
    private int mIncTempCounter = INC_TEMP_COUNTER;
    private int mDecTempCounter = DEC_TEMP_COUNTER;
    private int minMiddleRange = 21;
    private int maxMiddleRange = 27;

    private int minHotRange = 27;
    // private int maxHotRange = 60;

    Random mRandomTempGenerator = new Random(33);

    public override void Start()
    {
        ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value = 20;
        minMiddleRange = (int)ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value + 1;
        maxMiddleRange = (int)(27.0 * ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value / 20.0);
        minHotRange = maxMiddleRange;

        InitSimulation();
    }

    [OnChange(ClimateSimulation.Setting.FanSettings.MemberIDs.ThresholdTurnOnFan)]
    public void AdjustRanges()
    {
        minMiddleRange = (int)ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value + 1;
        maxMiddleRange = (int)(27.0 * ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value / 20.0);
        minHotRange = maxMiddleRange;
    }

    #region Animation

    private void StartPubAnimation()
    {
        if (!mPublishAnimationTimer.Enabled)
        {
            mPublishAnimationTimer.Start();
        }
    }

    /// <summary>
    /// If upper left temperature changed set symbol to an value and start publish animation
    /// </summary>
    [OnUpdate(ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.MemberIDs.ProvidedTemperature)]
    public void OnProvidedTempChangedUpLeft()
    {
        if (ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.ProvidedTemperature.Value >= minMiddleRange && ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.ProvidedTemperature.Value < maxMiddleRange)
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateUpLeft.Value = 1;
        }
        else if (ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.ProvidedTemperature.Value >= minHotRange)
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateUpLeft.Value = 2;
        }
        else
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateUpLeft.Value = 0;
        }

        ClimateSimulation.PanelSettings.PanelSetting.TemperatureSensorPublishUpLeft.Value = 1;
        StartPubAnimation();
    }

    [OnUpdate(ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.MemberIDs.ProvidedTemperature)]
    public void OnProvidedTempChangedLoLeft()
    {
        if (ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.ProvidedTemperature.Value >= minMiddleRange && ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.ProvidedTemperature.Value < maxMiddleRange)
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateLoLeft.Value = 1;
        }
        else if (ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.ProvidedTemperature.Value >= minHotRange)
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateLoLeft.Value = 2;
        }
        else
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateLoLeft.Value = 0;
        }

        ClimateSimulation.PanelSettings.PanelSetting.TemperatureSensorPublishLoLeft.Value = 1;
        StartPubAnimation();
    }

    [OnUpdate(ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.MemberIDs.ProvidedTemperature)]
    public void OnProvidedTempChangedUpRight()
    {
        if (ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.ProvidedTemperature.Value >= minMiddleRange && ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.ProvidedTemperature.Value < maxMiddleRange)
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateUpRight.Value = 1;
        }
        else if (ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.ProvidedTemperature.Value >= minHotRange)
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateUpRight.Value = 2;
        }
        else
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateUpRight.Value = 0;
        }

        ClimateSimulation.PanelSettings.PanelSetting.TemperatureSensorPublishUpRight.Value = 1;
        StartPubAnimation();
    }

    [OnUpdate(ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.MemberIDs.ProvidedTemperature)]
    public void OnProvidedTempChangedLoRight()
    {
        if (ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.ProvidedTemperature.Value >= minMiddleRange && ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.ProvidedTemperature.Value < maxMiddleRange)
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateLoRight.Value = 1;
        }
        else if (ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.ProvidedTemperature.Value >= minHotRange)
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateLoRight.Value = 2;
        }
        else
        {
            ClimateSimulation.PanelSettings.PanelSetting.TemperatureStateLoRight.Value = 0;
        }

        ClimateSimulation.PanelSettings.PanelSetting.TemperatureSensorPublishLoRight.Value = 1;
        StartPubAnimation();
    }

    #endregion

    [OnChange(ClimateSimulation.PanelSettings.PanelSetting.MemberIDs.AutomaticMode)]
    public void OnAutomaticModeChanged()
    {
        if (ClimateSimulation.PanelSettings.PanelSetting.AutomaticMode.Value == 1)
        {
            ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.ProvidedTemperature.Value = ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value;
            ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.ProvidedTemperature.Value = ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value;
            ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.ProvidedTemperature.Value = ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value;
            ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.ProvidedTemperature.Value = ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value;
            mAutomaticModeTimer.Start();
        }
        else
        {
            mAutomaticModeTimer.Stop();
        }
    }

    private void IncrementNewValue(ref long newValue)
    {
        if (newValue < ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value)
        {
            newValue += mRandomTempGenerator.Next(5, 8);
        }
    }

    private void DecrementCurrValue(ref long newValue)
    {
        if (newValue >= ClimateSimulation.Setting.FanSettings.ThresholdTurnOnFan.Value)
        {
            newValue -= mRandomTempGenerator.Next(1, 2);
        }
    }

    public void InitSimulation()
    {
        mPublishAnimationTimer = new Timer(TimeSpan.FromMilliseconds(500),
              (object sender, ElapsedEventArgs args) =>
              {
                  ClimateSimulation.PanelSettings.PanelSetting.TemperatureSensorPublishUpLeft.Value = 0;
                  ClimateSimulation.PanelSettings.PanelSetting.TemperatureSensorPublishLoLeft.Value = 0;
                  ClimateSimulation.PanelSettings.PanelSetting.TemperatureSensorPublishUpRight.Value = 0;
                  ClimateSimulation.PanelSettings.PanelSetting.TemperatureSensorPublishLoRight.Value = 0;
              }
        );

        mAutomaticModeTimer = new Timer(TimeSpan.FromMilliseconds(1000),
              (object sender, ElapsedEventArgs args) =>
              {
                  long currValue;

                  --mIncTempCounter;
                  --mDecTempCounter;

                  if (mDecTempCounter == 0)
                  {
                      mDecTempCounter = DEC_TEMP_COUNTER;

                      long tempToChange = mRandomTempGenerator.Next(0, 4);

                      switch (tempToChange)
                      {
                          case 0:
                          {
                              currValue = ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.ProvidedTemperature.Value;
                              DecrementCurrValue(ref currValue);
                              ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.ProvidedTemperature.Value = currValue;
                              break;
                          }
                          case 1:
                          {
                              currValue = ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.ProvidedTemperature.Value;
                              DecrementCurrValue(ref currValue);
                              ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.ProvidedTemperature.Value = currValue;
                              break;
                          }
                          case 2:
                          {
                              currValue = ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.ProvidedTemperature.Value;
                              DecrementCurrValue(ref currValue);
                              ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.ProvidedTemperature.Value = currValue;
                              break;
                          }
                          case 3:
                          {
                              currValue = ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.ProvidedTemperature.Value;
                              DecrementCurrValue(ref currValue);
                              ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.ProvidedTemperature.Value = currValue;
                              break;
                          }
                          default:
                              break;
                      }
                  }

                  if (mIncTempCounter == 0)
                  {
                      mIncTempCounter = INC_TEMP_COUNTER;

                      long tempToChange = mRandomTempGenerator.Next(0, 3);

                      switch (tempToChange)
                      {
                          case 0:
                          {
                              currValue = ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.ProvidedTemperature.Value;
                              IncrementNewValue(ref currValue);
                              ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperLeft.ProvidedTemperature.Value = currValue;
                              break;
                          }
                          case 1:
                          {
                              currValue = ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.ProvidedTemperature.Value;
                              IncrementNewValue(ref currValue);
                              ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerLeft.ProvidedTemperature.Value = currValue;
                              break;
                          }
                          case 2:
                          {
                              currValue = ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.ProvidedTemperature.Value;
                              IncrementNewValue(ref currValue);
                              ClimateSimulation.TemperatureSimulation.TemperatureSensorUpperRight.ProvidedTemperature.Value = currValue;
                              break;
                          }
                          case 3:
                          {
                              currValue = ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.ProvidedTemperature.Value;
                              IncrementNewValue(ref currValue);
                              ClimateSimulation.TemperatureSimulation.TemperatureSensorLowerRight.ProvidedTemperature.Value = currValue;
                              break;
                          }
                          default:
                              break;
                      }
                  }
              }
        );
    }
}
