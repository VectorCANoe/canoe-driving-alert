using System;
using System.Windows.Input;
using System.Windows.Media;

namespace Demo.Wpf.NavigationInfo.Interfaces
{
    internal interface INavigationInfoControlViewModel
    {
        /// <summary>
        /// Defines the value of the destination field
        /// </summary>
        String Destination { get; set; }

        /// <summary>
        /// Defines the value of the distance field
        /// </summary>
        String Distance { get; set; }

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
        ICommand SendCommand { get; }

        /// <summary>
        /// Event is thrown on SendValue
        /// </summary>
        event EventHandler ValueUpdated;
    }
}