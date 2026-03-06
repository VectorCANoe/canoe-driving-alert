using System;

namespace Demo.Wpf.Distance
{
    /// <summary>
    /// Data transfer object for serializing and deserializing of control properties
    /// </summary>
    public class DistanceControlDto
    {
        public Int32 MaxDistance { get; set; }

        public String Unit { get; set; }
    }
}
