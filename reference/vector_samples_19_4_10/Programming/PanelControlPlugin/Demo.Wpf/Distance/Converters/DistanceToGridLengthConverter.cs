using System;
using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace Demo.Wpf.Distance.Converters
{
    public class DistanceToGridLengthConverter : IValueConverter
    {
        #region Implementation of IValueConverter

        public Object Convert(Object value, Type targetType, Object parameter, CultureInfo culture)
        {
            if(value is Int32 intDistance)
                return new GridLength(intDistance, GridUnitType.Star);

            return Binding.DoNothing;
        }

        public Object ConvertBack(Object value, Type targetType, Object parameter, CultureInfo culture)
        {
            throw new NotSupportedException();
        }

        #endregion
    }
}
