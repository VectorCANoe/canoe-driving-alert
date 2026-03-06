using System;
using System.ComponentModel;

namespace Demo.Wpf.Easy
{
    public class DataRow : INotifyPropertyChanged
    {
        public DataRow(String description, Int32 value)
        {
            this.Description = description;
            this.Value = value;
        }

        public event PropertyChangedEventHandler PropertyChanged;

        #region Description Property (INotifyPropertyChanged)

        private String mDescription;
        public String Description
        {
            get
            {
                return mDescription;
            }
            set
            {
                mDescription = value;
                NotifyPropertyChanged("Description");
            }
        }

        #endregion

        #region Value Property (INotifyPropertyChanged)

        private Int32 mValue;
        public Int32 Value
        {
            get
            {
                return mValue;
            }
            set
            {
                mValue = value;
                NotifyPropertyChanged("Value");
            }
        }

        #endregion

        protected void NotifyPropertyChanged(String propertyName)
        {
            if (this.PropertyChanged != null)
            {
                this.PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }

    }
}
