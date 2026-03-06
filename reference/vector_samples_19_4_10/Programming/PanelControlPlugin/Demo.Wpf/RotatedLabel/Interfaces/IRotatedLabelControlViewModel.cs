using System;

namespace Demo.Wpf.RotatedLabel.Interfaces
{
    internal interface IRotatedLabelControlViewModel
    {
        String Text { get; set; }
        Double Angle { get; set; }
    }
}