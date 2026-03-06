using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Demo.Wpf.Distance.Interfaces;

namespace Demo.Wpf.Distance
{
    /// <summary>
    /// Interaction logic for DistanceControlView.xaml
    /// </summary>
    internal partial class DistanceControlView : UserControl, IDistanceControlView
    {
        #region Fields
        
        private readonly IDistanceControlViewModel mViewModel;
        private Point? mStartPosition;
        private Int32? mStartDistance;
        private Double mFactor;

        #endregion

        #region Constructor
        /// <summary>
        /// Constructor for initializing the view
        /// </summary>
        /// <param name="viewModel">View model for data bindings</param>
        public DistanceControlView(IDistanceControlViewModel viewModel)
        {
            mViewModel = viewModel ?? throw new ArgumentNullException(nameof(viewModel));

            this.DataContext = mViewModel;

            InitializeComponent();
        }
        #endregion

        #region UI Handling
        /// <summary>
        /// Handles start of value change
        /// </summary>
        private void UIElement_OnMouseDown(Object sender, MouseButtonEventArgs e)
        {
            if (!mViewModel.IsEnabled)
                return;

            // Store start values
            mStartPosition = e.GetPosition(this);
            mStartDistance = mViewModel.Distance;

            // Getting a Factor (UI px per distance)
            mFactor = (this.ActualWidth - CarA.ActualWidth - CarB.ActualWidth) / mViewModel.MaxDistance;

            // Capture mouse that it even works outside the control
            Mouse.Capture((IInputElement)sender);
        }

        /// <summary>
        /// Handles end of value change
        /// </summary>
        private void UIElement_OnMouseUp(Object sender, MouseButtonEventArgs e)
        {
            if (!mViewModel.IsEnabled)
                return;

            // Initiate sending the new value to CANoe
            mViewModel.SendValue();
            
            // Release mouse capture and startPosition
            Mouse.Capture(null);
            mStartPosition = null;
            mStartDistance = null;
        }

        /// <summary>
        /// Proceeds value change
        /// </summary>
        private void UIElement_OnMouseMove(Object sender, MouseEventArgs e)
        {
            // Check conditions to move
            if (!mViewModel.IsEnabled || e.LeftButton != MouseButtonState.Pressed)
                return;
            if (mStartDistance is null || mStartPosition is null)
                return;

            // get actual mouse point
            var actualPoint = e.GetPosition(this);

            // Calculate distance delta
            var movedUiDistance = actualPoint.X - mStartPosition.Value.X;
            var movedDistance = movedUiDistance / mFactor;

            // Round and check new distance Value
            var newDistance = Convert.ToInt32(Math.Round(mStartDistance.Value + movedDistance));
            if (newDistance < 0 && newDistance > mViewModel.MaxDistance)
                return;

            // Set new distance to view model
            mViewModel.Distance = newDistance;
        }
        #endregion
    }
}
