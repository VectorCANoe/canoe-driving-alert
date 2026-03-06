using System;
using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace Demo.Wpf.Helper.Converters
{
    public class BooleanToVisibilityConverter : IValueConverter
    {
        #region Implementation of IValueConverter

        public Object Convert(Object value, Type targetType, Object parameter, CultureInfo culture)
        {
            if(value is Boolean boolVisibility)
                return boolVisibility ? Visibility.Visible : Visibility.Hidden;

            return Binding.DoNothing;
        }

        public Object ConvertBack(Object value, Type targetType, Object parameter, CultureInfo culture)
        {
            throw new NotSupportedException();
        }

        #endregion
    }
}