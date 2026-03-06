using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Xml.Serialization;
using Demo.Wpf.Distance.Interfaces;
using Vector.PanelControlPlugin.Wpf;

namespace Demo.Wpf.Distance
{
    public class DistanceControl : IPluginControl, IProvidesForegroundColor, IProvidesBackgroundColor, IProvidesSymbolBinding, IProvidesEnabled, IProvidesProperties
    {
        #region Fields
        private IDistanceControlViewModel mViewModel;
        private IExchangeSymbolValue mSymbolValue;
        private Color mControlBackColor = Colors.Transparent;
        private Color mControlForeColor = Colors.Black;
        #endregion
        
        #region Constructor
        /// <summary>
        /// Constructor for the control
        /// Initializes viewModel and view
        /// </summary>
        public DistanceControl()
        {
            mViewModel = new DistanceControlViewModel();
            this.View = new DistanceControlView(mViewModel);

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
        public String Name => "Distance Control";

        /// <summary>
        /// Returns the glyph for the plugin control, which is displayed in the toolbox of the panel designer.
        /// </summary>
        public ImageSource Glyph {
            get
            {
                var resourceDictionary = new ResourceDictionary
                {
                    Source = new Uri("pack://application:,,,/Demo_WPF;component/Resources/Glyph.xaml", UriKind.Absolute)
                };

                return resourceDictionary["UserControlDistance_Icon16DrawingImage"] as ImageSource;

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

        #region Implementation of IProvidesSymbolBinding

        /// <summary>
        /// This property is for exchanging the symbol value.
        /// </summary>
        public IExchangeSymbolValue SymbolValue
        {
            get => mSymbolValue;
            set
            {
                if (value == mSymbolValue)
                    return;

                if (!(mSymbolValue is null))
                    mSymbolValue.ValueChanged -= SymbolValueOnValueChanged;

                mSymbolValue = value;

                mSymbolValue.ValueChanged += SymbolValueOnValueChanged;
            }
        }

        /// <summary>
        /// Returns the data types, which are supported by the plugin control
        /// </summary>
        public ExchangeSymbolDataType SupportedDataTypes => ExchangeSymbolDataType.Long;

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

        #region Implementation of IProvidesProperties

        /// <summary>
        /// Serializes all supported properties and returns the serialization string in the out parameter.
        /// </summary>
        /// <param name="serializationString">serialized properties</param>
        /// <returns>true, if serialization was successful, otherwise false</returns>
        public Boolean SerializeSupportedProperties(out String serializationString)
        {
            // Transfer the Values from the ViewModel to a DataTransferObject
            var dto = new DistanceControlDto() { MaxDistance = mViewModel.MaxDistance, Unit = mViewModel.Unit };

            serializationString = String.Empty;

            // Serializing the DataTransferObject to XML
            using (StringWriter stringWriter = new StringWriter())
            {
                XmlSerializer serializer = new XmlSerializer(typeof(DistanceControlDto));
                serializer.Serialize(stringWriter, dto);
                serializationString = stringWriter.ToString();
            }

            return true;
        }

        /// <summary>
        /// Deserializes the supported properties from the given string.
        /// </summary>
        /// <param name="serializationString">serialized properties</param>
        /// <returns>true, if deserialization was successful, otherwise false</returns>

        public Boolean DeserializeSupportedProperties(String serializationString)
        {
            if (String.IsNullOrWhiteSpace(serializationString))
                return false;

            // Deserialize the XML String to create a DataTransferObject
            using (StringReader stringReader = new StringReader(serializationString))
            {
                XmlSerializer serializer = new XmlSerializer(typeof(DistanceControlDto));
                var dto = (DistanceControlDto)serializer.Deserialize(stringReader);

                // Updating the parameters at the ViewModel
                mViewModel.MaxDistance = dto.MaxDistance;
                mViewModel.Unit = dto.Unit;
            }

            return true;
        }

        /// <summary>
        /// Returns the list of property names, which are supported by the plugin control, i.e.
        /// the list of properties, which can be configured in the property grid of the 
        /// panel designer.
        /// </summary>
        public IList<String> SupportedProperties => new List<String>()
        {
            nameof(this.Unit),
            nameof(this.MaxDistance),
        };

        #endregion

        #region Properties
        // User editable properties that should be displayed in the property grid.

        [Category("Specification")]
        [DisplayName("Max. Distance")]
        public Int32 MaxDistance
        {
            get => mViewModel.MaxDistance;
            set => mViewModel.MaxDistance = value;
        }

        [Category("UI")]
        [DisplayName("Unit")]
        public String Unit
        {
            get => mViewModel.Unit;
            set => mViewModel.Unit = value;
        }

        #endregion

        #region Helpers

        /// <summary>
        /// This Method is called if the bound symbol value has been updated
        /// </summary>
        private void SymbolValueOnValueChanged(Object sender, EventArgs e)
        {
            if (this.SymbolValue.SymbolDataType != ExchangeSymbolDataType.Long)
                return;

            mViewModel.Distance = this.SymbolValue.Value is Int32 int32 ? int32 : mViewModel.MaxDistance / 2;
        }

        /// <summary>
        /// This Method is used to update the value in CANoe after the user changed it on the control
        /// </summary>
        /// <param name="sender">Sending viewModel</param>
        /// <param name="e">Empty event arguments</param>
        private void ViewModelOnValueUpdated(Object sender, EventArgs e)
        {
            if (mSymbolValue.SymbolDataType == ExchangeSymbolDataType.Long)
            {
                this.SymbolValue.Value = mViewModel.Distance;
            }
        }

        #endregion
    }
}
