// Copyright (c) Vector Informatik GmbH. All rights reserved.

using ASAM.XIL.Interfaces.Testbench.MAPort;
using ASAM.XIL.Interfaces.Testbench.MAPort.Enum;
using System.Collections.Generic;
using System;
using ASAM.XIL.Interfaces.Testbench.Common.ValueContainer.Enum;


namespace XILAPIServer
{

    public class MAPortVariableInfo : IMAPortVariableInfo
    {

        public IList<string> AvailableTasks
        {
            get
            {
                throw new NotImplementedException();
            }
        }

        public DataType DataType {get; set;}

        public string Name {get; set;}

        public bool Readable {get; set;}

        public bool Writeable {get; set;}

        public ulong XSize {get; set;}

        public ulong YSize {get; set;}

        public bool IsReadable(MAPortState state)
        {
            return Readable;
        }

        public bool IsWriteable(MAPortState state)
        {
            return Writeable;
        }
	}

}