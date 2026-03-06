using System.Windows.Controls;
using Demo.Wpf.RotatedLabel.Interfaces;

namespace Demo.Wpf.RotatedLabel
{
    /// <summary>
    /// Interaction logic for RotatedLabelControlView.xaml
    /// </summary>
    internal partial class RotatedLabelControlView : UserControl, IRotatedLabelControlView
    {
        public RotatedLabelControlView(IRotatedLabelControlViewModel viewModel)
        {
            this.DataContext = viewModel;

            InitializeComponent();
        }
    }
}
