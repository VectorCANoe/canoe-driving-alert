using System;
using System.ComponentModel;
using System.Windows.Input;
using System.Windows.Media;
using Demo.Wpf.Helper;
using Demo.Wpf.NavigationInfo.Interfaces;

namespace Demo.Wpf.NavigationInfo
{
    internal class NavigationInfoControlViewModel : INotifyPropertyChanged, INavigationInfoControlViewModel
    {
        #region Fields

        private ICommand mSendCommand;
        private String mDestination;
        private String mDistance;
        private Brush mBackgroundColor = Brushes.White;
        private Brush mTextColor = Brushes.Black;
        private Boolean mIsEnabled = true;
        private Boolean mIsVisible = true;

        #endregion

        #region Properties

        public String Destination
        {
            get => mDestination;
            set
            {
                mDestination = value;
                OnPropertyChanged(nameof(this.Destination));
            }
        }

        public String Distance
        {
            get => mDistance;
            set
            {
                mDistance = value;
                OnPropertyChanged(nameof(this.Distance));
            }
        }

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

        #region Commands & Events

        public ICommand SendCommand => mSendCommand ?? (mSendCommand = new RelayCommand(Send, CanSend));

        private Boolean CanSend(Object obj)
        {
            return !(this.ValueUpdated is null);
        }

        private void Send(Object obj)
        {
            this.ValueUpdated?.Invoke(this, EventArgs.Empty);
        }

        public event EventHandler ValueUpdated;

        #endregion

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(String propertyName)
        {
            this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
