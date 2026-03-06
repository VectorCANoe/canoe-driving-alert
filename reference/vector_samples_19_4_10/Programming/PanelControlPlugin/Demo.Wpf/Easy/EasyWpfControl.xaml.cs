using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using Vector.PanelControlPlugin.Wpf;

namespace Demo.Wpf.Easy
{
    public partial class EasyWpfControl : UserControl, IPluginControl, IProvidesForegroundColor, IProvidesBackgroundColor, IProvidesSymbolBinding, IProvidesEnabled, IProvidesProperties, INotifyPropertyChanged

    {
        #region Members

        // symbol value for exchanging the value between CANoe and plugin control and vice versa
        IExchangeSymbolValue mSymbolValue = null;

        private String mDescription = "Description";
        ObservableCollection<DataRow> mData = new ObservableCollection<DataRow>();

        #endregion

        #region construction, initalization
        public EasyWpfControl()
        {
            InitializeComponent();

            mItems.ItemsSource = mData;
            UpdateData();
        }
        #endregion

        #region IPluginControl Members

        /// <summary>
        /// This method is called, when the panel is loaded in CANoe/CANalyzer.
        /// </summary>
        public void Initialize()
        { }

        /// <summary>
        /// Returns the name of the plugin control, which is shown in the toolbox of the panel designer.
        /// </summary>
        public new String Name => "Easy WPF Control";

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

                return resourceDictionary["UserControlWPF_Icon16DrawingImage"] as ImageSource;
            }
        }

        /// <summary>
        /// Returns the control, which actually shall be shown in the panel.
        /// </summary>
        public FrameworkElement View => this;

        /// <summary>
        /// Property to set the plugin control visible or invisible.
        /// This method can be called via CAPL, to control the display of controls.
        /// </summary>
        public Boolean Visible
        {
            get => base.Visibility == Visibility.Visible;
            set => base.Visibility = value ? Visibility.Visible : Visibility.Hidden;
        }
        #endregion

        #region Implementation of IProvidesSymbolBinding

        public ExchangeSymbolDataType SupportedDataTypes
        {
            get { return ExchangeSymbolDataType.LongArray; }
        }

        /// <summary>
        /// This property is for exchanging the symbol value.
        /// </summary>
        public IExchangeSymbolValue SymbolValue
        {
            get
            {
                return mSymbolValue;
            }
            set
            {
                if (!(mSymbolValue is null))
                    mSymbolValue.ValueChanged -= OnRxValue;

                mSymbolValue = value;

                mSymbolValue.ValueChanged += OnRxValue;
            }
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
            Boolean returnValue = true;
            serializationString = "";

            // provide a serialization for all properties supported by the plugin control
            // (without the properties ControlBackColor, ControlForeColor, Enabled and Visible)
            // the following examples show two different possibilities:
            // 1st: for a simple string property
            // 2nd: for a property, which has a TypeConverter
            // Take care, that the deserialization is implemented accordingly.

            // property "Description"
            serializationString += this.Description.ToString();
            serializationString += ";";

            return returnValue;
        }

        /// <summary>
        /// Deserializes the supported properties from the given string.
        /// </summary>
        /// <param name="serializationString">serialized properties</param>
        /// <returns>true, if deserialization was successful, otherwise false</returns>
        public Boolean DeserializeSupportedProperties(String serializationString)
        {
            Boolean returnValue = true;

            // =====>
            // provide a serialization for all properties supported by the plugin control
            // (without the properties ControlBackColor, ControlForeColor, Enabled and Visible)

            String[] propertyValues = serializationString.Split(new Char[] { ';' });

            if (propertyValues.Any())
            {
                this.Description = propertyValues[0];
            }
            // <=====

            return returnValue;
        }

        /// <summary>
        /// Returns the list of property names, which are supported by the plugin control, i.e.
        /// the list of properties, which can be configured in the property grid of the 
        /// panel designer.
        /// </summary>
        public IList<String> SupportedProperties => new List<String>()
        {
            nameof(this.Description),
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
            get => base.IsEnabled;
            set => base.IsEnabled = value;
        }

        #endregion

        #region Implementation of IProvidesBackgroundColor

        /// <summary>
        /// Property to set or get the background color of the plugin control.
        /// This method can be called via CAPL, to control the display of controls.
        /// </summary>
        public Color BackgroundColor
        {

            get
            {
                var brush = base.Background as SolidColorBrush;
                return Color.FromArgb(brush.Color.A, brush.Color.R, brush.Color.G, brush.Color.B);
            }
            set => base.Background = new SolidColorBrush(Color.FromArgb(value.A, value.R, value.G, value.B));
        }

        #endregion

        #region Implementation of IProvidesForegroundColor

        /// <summary>
        /// Property to set or get the foreground color of the plugin control.
        /// This method can be called via CAPL, to control the display of controls.
        /// </summary>
        public Color ForegroundColor
        {
            get
            {
                var brush = this.Foreground as SolidColorBrush;
                return Color.FromArgb(brush.Color.A, brush.Color.R, brush.Color.G, brush.Color.B);
            }
            set => this.Foreground = new SolidColorBrush(Color.FromArgb(value.A, value.R, value.G, value.B));
        }

        #endregion

        #region Properties

        // implement all properties of the plugin control, which shall be configured in the 
        // property grid of the paneldesigner

        [Category("WPF Control Settings")]
        [DisplayName("Description")]
        public String Description
        {
            get
            {
                return mDescription;
            }
            set
            {
                mDescription = value;
                UpdateData();
            }
        }


        #endregion

        #region Rx/Tx values

        /// <summary>
        /// Actions which are necessary, when a new value is received from CANoe.
        /// The received value is in this-value and must be sent to the plugin control.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        void OnRxValue(Object sender, EventArgs e)
        {
            try
            {
                UpdateData();
            }
            catch (Exception)
            {
            }
        }

        private void UpdateData()
        {
            List<Int32> array = GetArrayFromCANoe();

            GenerateData(array);
        }

        private List<Int32> GetArrayFromCANoe()
        {
            var array = this.SymbolValue?.SymbolDataType == ExchangeSymbolDataType.LongArray &&
                        this.SymbolValue.Value is IEnumerable<Int32> value ?
                value.ToList() :
                new List<Int32> { 10, 20, 30 };
            return array;
        }

        private void GenerateData(List<Int32> array)
        {
            mData.Clear();
            for (Int32 i = 0; i < array.Count(); i++)
            {
                mData.Add(new DataRow(this.Description + "[" + i.ToString() + "]", array[i]));
            }
        }

        private void Button_Click(Object sender, RoutedEventArgs e)
        {
            SendValue(sender);
        }

        void SendValue(Object sender)
        {
            if (mSymbolValue == null ||
                mSymbolValue.SymbolDataType != ExchangeSymbolDataType.LongArray)
                return;

            List<Int32> newArrayValue = GetArrayFromCANoe();

            for (Int32 i = 0; i < newArrayValue.Count; i++)
            {
                // Value.SymbolDataType depends on the symbol data type of the assigned symbol.
                // It is given from the CANoe database and must not be changed.

                // Put the value from the plugin control to Value.LongValue.
                newArrayValue[i] = mData[i].Value;
            }
            mSymbolValue.Value = newArrayValue;
        }

        #endregion

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(String propertyName)
        {
            this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
