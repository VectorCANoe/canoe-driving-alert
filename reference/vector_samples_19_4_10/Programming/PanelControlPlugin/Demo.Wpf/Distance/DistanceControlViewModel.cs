using System;
using System.ComponentModel;
using System.Windows.Media;
using Demo.Wpf.Distance.Interfaces;

namespace Demo.Wpf.Distance
{
    internal class DistanceControlViewModel : INotifyPropertyChanged, IDistanceControlViewModel
    {
        private Int32 mDistance = 50;
        private Int32 mMaxDistance = 100;
        private String mUnit = "m";
        private Brush mBackgroundColor = Brushes.Transparent;
        private Brush mTextColor = Brushes.Black;
        private Boolean mIsEnabled = true;
        private Boolean mIsVisible = true;

        #region Properties

        /// <summary>
        /// Distance between both cars (bound value)
        /// </summary>
        public Int32 Distance
        {
            get => mDistance;
            set
            {
                mDistance = value;
                OnPropertyChanged(nameof(this.Distance));
                OnPropertyChanged(nameof(this.ReserveSpace));
                OnPropertyChanged(nameof(this.DisplayDistance));
            }
        }

        /// <summary>
        /// Maximum displayable space between both cars.
        /// </summary>
        public Int32 MaxDistance
        {
            get => mMaxDistance;
            set
            {
                mMaxDistance = value;
                OnPropertyChanged(nameof(this.MaxDistance));
                OnPropertyChanged(nameof(this.ReserveSpace));
            }
        }

        /// <summary>
        /// Unit to be shown behind the numeric value display
        /// </summary>
        public String Unit
        {
            get => mUnit;
            set
            {
                mUnit = value;
                OnPropertyChanged(nameof(this.Unit));
                OnPropertyChanged(nameof(this.DisplayDistance));
            }
        }

        /// <summary>
        /// Space that has to be empty to allow the distance to increase to MaxDistance
        /// </summary>
        public Int32 ReserveSpace => this.MaxDistance - this.Distance;

        /// <summary>
        /// Value to Display
        /// </summary>
        public String DisplayDistance => this.Distance.ToString() + " " + this.Unit;

        /// <summary>
        /// Defines the BackgroundColor of the control
        /// </summary>
        public Brush BackgroundColor
        {
            get => mBackgroundColor;
            set
            {
                mBackgroundColor = value;
                OnPropertyChanged(nameof(this.BackgroundColor));
            }
        }

        /// <summary>
        /// Defines the TextColor of the control
        /// </summary>
        public Brush TextColor
        {
            get => mTextColor;
            set
            {
                mTextColor = value;
                OnPropertyChanged(nameof(this.TextColor));
            }
        }

        /// <summary>
        /// Defines if the user interaction with the control is enabled
        /// </summary>
        public Boolean IsEnabled
        {
            get => mIsEnabled;
            set
            {
                mIsEnabled = value;
                OnPropertyChanged(nameof(this.IsEnabled));
            }
        }

        /// <summary>
        /// Defines if the control is visible or hidden
        /// </summary>
        public Boolean IsVisible
        {
            get => mIsVisible;
            set
            {
                mIsVisible = value;
                OnPropertyChanged(nameof(this.IsVisible));
            }
        }

        #endregion

        #region Methods & Events

        public void SendValue()
        {
            this.ValueUpdated?.Invoke(this, EventArgs.Empty);
        }

        public event EventHandler ValueUpdated;

        #endregion

        #region PropertyChanged

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(String propertyName)
        {
            this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        #endregion

        
    }
}
