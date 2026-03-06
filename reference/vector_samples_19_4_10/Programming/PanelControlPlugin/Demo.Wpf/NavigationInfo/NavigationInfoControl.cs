using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Media;
using Demo.Wpf.NavigationInfo.Interfaces;
using Vector.PanelControlPlugin.Wpf;

namespace Demo.Wpf.NavigationInfo
{
    public class NavigationInfoControl : IPluginControl, IProvidesForegroundColor, IProvidesBackgroundColor, IProvidesMultiSymbolBinding, IProvidesEnabled
    {
        #region Fields

        private readonly INavigationInfoControlViewModel mViewModel;
        private Color mControlForeColor = Colors.Black;
        private Color mControlBackColor = Colors.White;
        private Dictionary<String, IExchangeSymbolValue> mSymbolValues;

        private const Int32 cDestinationLength = 100;

        #endregion

        #region Constants

        private const String Distance = "Distance";
        private const String Destination = "Destination";

        #endregion

        #region Constructor

        public NavigationInfoControl()
        {
            mViewModel = new NavigationInfoControlViewModel();
            this.View = new NavigationInfoControlView(mViewModel);

            mViewModel.ValueUpdated += ViewModelOnValueUpdated;
        }

        #endregion

        #region Implementation of IPluginControl

        /// <summary>
        /// This method is called, when the panel is loaded in CANoe/CANalyzer.
        /// </summary>
        public void Initialize()
        {
        }

        /// <summary>
        /// Returns the control, which actually shall be shown in the panel.
        /// </summary>
        public FrameworkElement View { get; }

        /// <summary>
        /// Returns the name of the plugin control, which is shown in the toolbox of the panel designer.
        /// </summary>
        public String Name => "Navigation Info Control";

        /// <summary>
        /// Returns the glyph for the plugin control, which is displayed in the toolbox of the panel designer.
        /// </summary>
        public ImageSource Glyph
        {
            get
            {
                var resourceDictionary = new ResourceDictionary
                {
                    Source = new Uri("pack://application:,,,/Demo_WPF;component/Resources/Glyph.xaml", UriKind.Absolute)
                };

                return resourceDictionary["UserControlNavInfo_Icon16DrawingImage"] as ImageSource;

            }
        }

        /// <summary>
        /// Property to set the plugin control visible or invisible.
        /// This method can be called via CAPL, to control the display of controls.
        /// </summary>
        public Boolean Visible
        {
            get => mViewModel.IsVisible;
            set => mViewModel.IsVisible = value;
        }

        #endregion

        #region Implementation of IProvidesForegroundColor

        /// <summary>
        /// Property to set or get the foreground color of the plugin control.
        /// This method can be called via CAPL, to control the display of controls.
        /// </summary>
        public Color ForegroundColor
        {
            get => mControlForeColor;
            set
            {
                mControlForeColor = value;
                mViewModel.TextColor = new SolidColorBrush(value);
            }
        }

        #endregion

        #region Implementation of IProvidesBackgroundColor

        /// <summary>
        /// Property to set or get the background color of the plugin control.
        /// This method can be called via CAPL, to control the display of controls.
        /// </summary>
        public Color BackgroundColor
        {
            get => mControlBackColor;
            set
            {
                mControlBackColor = value;
                mViewModel.BackgroundColor = new SolidColorBrush(value);
            }
        }

        #endregion

        #region Implementation of IProvidesMultiSymbolBinding

        public Dictionary<String, IExchangeSymbolValue> SymbolValues
        {
            get => mSymbolValues;
            set
            {
                if (value == mSymbolValues)
                    return;

                if (!(mSymbolValues is null))
                {
                    mSymbolValues[Distance].ValueChanged -= DistanceSymbolValueOnValueChanged;
                    mSymbolValues[Destination].ValueChanged -= DestinationSymbolValueOnValueChanged;
                }

                mSymbolValues = value;

                mSymbolValues[Distance].ValueChanged += DistanceSymbolValueOnValueChanged;
                mSymbolValues[Destination].ValueChanged += DestinationSymbolValueOnValueChanged;
            }
        }

        public Dictionary<String, ExchangeSymbolDataType> SupportedDataProperties { get; } 
            = new Dictionary<String, ExchangeSymbolDataType>()
            {
                {Distance, ExchangeSymbolDataType.ULong}, 
                {Destination, ExchangeSymbolDataType.String}
            };

        #endregion

        #region Implementation of IProvidesEnabled

        /// <summary>
        /// Property to enable or disable the plugin control.
        /// This property is called, when the DisplayOnly-property is set in the property grid of the panel designer.
        /// This method can be called via CAPL, to control the display/behavior of controls.
        /// </summary>
        public Boolean Enabled
        {
            get => mViewModel.IsEnabled;
            set => mViewModel.IsEnabled = value;
        }

        #endregion

        #region Helpers

        /// <summary>
        /// This Method is called if the bound symbol "Distance" value has been updated
        /// </summary>
        private void DistanceSymbolValueOnValueChanged(Object sender, EventArgs e)
        {
            mViewModel.Distance = (this.SymbolValues[Distance].Value is UInt32 value ? value : 0).ToString();
        }

        /// <summary>
        /// This Method is called if the bound symbol "Distance" value has been updated
        /// </summary>
        private void DestinationSymbolValueOnValueChanged(Object sender, EventArgs e)
        {
            mViewModel.Destination = this.SymbolValues[Destination].Value is String value ? value : String.Empty;
        }

        /// <summary>
        /// This Method is used to update the value in CANoe after the user changed it on the control
        /// </summary>
        /// <param name="sender">Sending viewModel</param>
        /// <param name="e">Empty event arguments</param>
        private void ViewModelOnValueUpdated(Object sender, EventArgs e)
        {
            if (mSymbolValues[Distance].SymbolDataType == ExchangeSymbolDataType.ULong &&
                UInt32.TryParse(mViewModel.Distance, out var distance))
            {
                mSymbolValues[Distance].Value = distance;
            }

            if (mSymbolValues[Destination].SymbolDataType == ExchangeSymbolDataType.String)
            {
                mSymbolValues[Destination].Value = mViewModel.Destination;
            }
        }

        #endregion
    }
}
