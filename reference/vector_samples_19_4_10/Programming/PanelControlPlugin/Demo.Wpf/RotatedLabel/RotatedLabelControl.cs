using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Xml.Serialization;
using Demo.Wpf.RotatedLabel.Interfaces;
using Vector.PanelControlPlugin.Wpf;

namespace Demo.Wpf.RotatedLabel
{
    public class RotatedLabelControl : IPluginControl, IProvidesProperties
    {
        #region Fields

        private readonly IRotatedLabelControlViewModel mViewModel;

        #endregion

        #region Constructor

        public RotatedLabelControl()
        {
            mViewModel = new RotatedLabelControlViewModel();
            this.View = new RotatedLabelControlView(mViewModel);
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
        public String Name => "Rotated Label Control";

        /// <summary>
        /// Returns the glyph for the plugin control, which is displayed in the toolbox of the panel designer.
        /// </summary>
        public ImageSource Glyph => null;

        /// <summary>
        /// Property to set the plugin control visible or invisible.
        /// This method can be called via CAPL, to control the display of controls.
        /// </summary>
        public Boolean Visible { get; set; }

        #endregion

        #region Properties
        // User editable properties that shall be displayed in the property grid.

        [Category("Display")]
        [DisplayName("Text")]
        public String Text
        {
            get => mViewModel.Text;
            set => mViewModel.Text = value;
        }

        [Category("Display")]
        [DisplayName("Rotation Angle")]
        public Double Angle
        {
            get => mViewModel.Angle;
            set => mViewModel.Angle = value;
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
            var dto = new RotatedLabelControlDto()
            {
                Text = mViewModel.Text,
                Angle = mViewModel.Angle,
            };

            serializationString = String.Empty;

            // Serializing the DataTransferObject to XML
            using (StringWriter stringWriter = new StringWriter())
            {
                XmlSerializer serializer = new XmlSerializer(typeof(RotatedLabelControlDto));
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
                XmlSerializer serializer = new XmlSerializer(typeof(RotatedLabelControlDto));
                var dto = (RotatedLabelControlDto)serializer.Deserialize(stringReader);

                // Updating the parameters at the ViewModel
                mViewModel.Text = dto.Text;
                mViewModel.Angle = dto.Angle;
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
            nameof(this.Text),
            nameof(this.Angle),
        };

        #endregion
    }
}
