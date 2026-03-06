// Copyright (c) Vector Informatik GmbH. All rights reserved.

#region Usings

using System;
using System.Collections.Generic;
using ASAM.XIL.Interfaces.Testbench.MAPort;
using ASAM.XIL.Interfaces.Testbench.MAPort.Enum;
using ASAM.XIL.Interfaces.Testbench.Common.SignalGenerator;
using ASAM.XIL.Interfaces.Testbench.Common.Capturing;
using ASAM.XIL.Interfaces.Testbench.Common.ValueContainer.Enum;
using ASAM.XIL.Interfaces.Testbench.Common.ValueContainer;
using ASAM.XIL.Interfaces.Testbench.Common.MetaInfo;
using ASAM.XIL.Interfaces.Testbench.Common.TargetScript;
using ASAM.XIL.Implementation.Testbench.Common.ValueContainer;

#endregion

namespace XILAPIServer
{
  internal class MAPort : IMAPort
  {
    #region Members

    private const string ReadableVarName = "XILServer/MAPort.TestVariableReadable";

    private const string WriteableVarName = "XILServer/MAPort.TestVariableWriteable";

    private double mTestValue;

    #endregion

    #region Constructors

    public MAPort()
    {
      State = MAPortState.eDISCONNECTED;
    }

    #endregion

    #region IMAPort Implementation

    public IMAPortConfig Configuration { get; private set; }

    public void Configure(IMAPortConfig config, bool forceConfig)
    {
    }

    public DataType GetDataType(string variableName)
    {
      return DataType.eFLOAT;
    }

    public IMAPortVariableInfo GetVariableInfo(string variableName)
    {
      var readable = IsReadable(variableName);
      
      return new MAPortVariableInfo
      {
        DataType = DataType.eFLOAT,
        Readable = readable,
        Writeable = !readable,
        Name = variableName,
      };
    }

    public bool IsReadable(string variableName)
    {
      return variableName == ReadableVarName;
    }

    public bool IsWritable(string variableName)
    {
      return variableName == WriteableVarName;
    }

    public IMAPortConfig LoadConfiguration(string filepath)
    {
      return null;
    }

    public IBaseValue Read(string variableName)
    {
      if (variableName == ReadableVarName)
      {
        return new FloatValue(mTestValue);
      }

      return null;
    }

    public IList<IBaseValue> ReadSimultaneously(IList<string> variableNames, string taskName)
    {
        IList<IBaseValue> ret = new List<IBaseValue>();
        for (int i = 0; i < variableNames.Count; ++i)
        {
            ret.Add(new FloatValue(mTestValue));
        }
        return ret;
    }

    public void StartSimulation()
    {
      State = MAPortState.eSIMULATION_RUNNING;
    }

    public MAPortState State { get; private set; }

    public void StopSimulation()
    {
      State = MAPortState.eSIMULATION_STOPPED;
    }

    public IList<ITaskInfo> TaskInfos
    {
      get { return null; }
    }

    public IList<string> VariableNames
    {
      get { return new[] { ReadableVarName, WriteableVarName }; }
    }

    public SimultaneousLevel SimultaneousLevel { get; }
    public IMAPortBreakpoint Breakpoint { get; set; }
    public double SimulationStepSize { get; }

    public void Write(string variableName, IBaseValue value)
    {
      if (variableName == WriteableVarName)
      {
        mTestValue = (value as IFloatValue).Value + 1.0;
      }
    }

    public void Disconnect()
    {
      State = MAPortState.eDISCONNECTED;
    }


    public string Name { get; set; }

    #endregion

    #region Not Implemented

    public void DownloadParameterSets(IList<string> filepaths)
    {
      throw new NotImplementedException();
    }

    public IList<string> CheckVariableNames(IList<string> variableNames)
    {
      throw new NotImplementedException();
    }

    public void WriteSimultaneously(IList<string> variableNames, IList<IBaseValue> values, string taskName)
    {
      throw new NotImplementedException();
    }

    public void PauseSimulation()
    {
      throw new NotImplementedException();
    }

    public void Dispose()
    {
    }

    public ITargetScript CreateTargetScript()
    {
      throw new NotImplementedException();
    }

    public void WaitForBreakpoint(double timeout)
    {
      throw new NotImplementedException();
    }

    public IList<string> TaskNames
    {
      get { throw new NotImplementedException(); }
    }

    public double DAQClock
    {
      get { throw new NotImplementedException(); }
    }

    public ICapture CreateCapture(string taskName)
    {
      throw new NotImplementedException();
    }

    public ISignalGenerator CreateSignalGenerator()
    {
      throw new NotImplementedException();
    }

    #endregion
  }
}