using System;
using System.ComponentModel;
using Demo.Wpf.RotatedLabel.Interfaces;

namespace Demo.Wpf.RotatedLabel
{
    internal class RotatedLabelControlViewModel : INotifyPropertyChanged, IRotatedLabelControlViewModel
    {
        private String mText = "Text";
        private Double mAngle = 90;

        public String Text
        {
            get => mText;
            set
            {
                mText = value;
                OnPropertyChanged(nameof(this.Text));
            }
        }

        public Double Angle
        {
            get => mAngle;
            set
            {
                mAngle = value;
                OnPropertyChanged(nameof(this.Angle));
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(String propertyName)
        {
            this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
