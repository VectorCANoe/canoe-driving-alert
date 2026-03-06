using System;
using System.Windows.Media;

namespace Demo.Wpf.Distance.Interfaces
{
    internal interface IDistanceControlViewModel
    {
        /// <summary>
        /// Distance between both cars (bound value)
        /// </summary>
        Int32 Distance { get; set; }

        /// <summary>
        /// Maximum displayable space between both cars
        /// </summary>
        Int32 MaxDistance { get; set; }

        /// <summary>
        /// Unit to be shown behind the numeric value display
        /// </summary>
        String Unit { get; set; }

        /// <summary>
        /// Space that has to be empty to allow the distance to increase to MaxDistance
        /// </summary>
        Int32 ReserveSpace { get; }

        /// <summary>
        /// Value to Display
        /// </summary>
        String DisplayDistance { get; }

        /// <summary>
        /// Defines the BackgroundColor of the control
        /// </summary>
        Brush BackgroundColor { get; set; }

        /// <summary>
        /// Defines the TextColor of the control
        /// </summary>
        Brush TextColor { get; set; }

        /// <summary>
        /// Defines if the user interaction with the control is enabled
        /// </summary>
        Boolean IsEnabled { get; set; }

        /// <summary>
        /// Defines if the control is visible or hidden
        /// </summary>
        Boolean IsVisible { get; set; }

        /// <summary>
        /// Transfers the values from the view model to the application
        /// </summary>
        void SendValue();

        /// <summary>
        /// Event is thrown on SendValue
        /// </summary>
        event EventHandler ValueUpdated;
    }
}