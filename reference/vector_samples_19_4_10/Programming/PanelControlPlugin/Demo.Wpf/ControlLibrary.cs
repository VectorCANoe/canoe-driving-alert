using System;
using System.Windows;
using System.Windows.Media;
using Vector.PanelControlPlugin.Wpf;

namespace Demo.Wpf
{
    public class ControlLibrary : IPluginLibrary
    {
        #region Implementation of IPluginLibrary

        /// <summary>
        /// Returns the name of the plugin control library as it shall be shown in the toolbox of the panel designer.
        /// </summary>
        public String Name => "WPF DemoLibrary";

        /// <summary>
        /// Returns an icon, which shall be shown in the toolbox of the panel designer.
        /// Return null, if no image shall be shown. In this case, the name of the library is shown.
        /// </summary>
        public ImageSource Glyph
        {
            get
            {
                var resourceDictionary = new ResourceDictionary
                {
                    Source = new Uri("pack://application:,,,/Demo_WPF;component/Resources/Glyph.xaml", UriKind.Absolute)
                };

                return resourceDictionary["UserToolBox_Icon16DrawingImage"] as ImageSource;
            }
        }

        #endregion
    }
}
