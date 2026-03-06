using System;
using System.Windows.Controls;
using Demo.Wpf.NavigationInfo.Interfaces;

namespace Demo.Wpf.NavigationInfo
{
    /// <summary>
    /// Interaction logic for NavigationInfoControlView.xaml
    /// </summary>
    internal partial class NavigationInfoControlView : UserControl
    {
        private readonly INavigationInfoControlViewModel mViewModel;

        public NavigationInfoControlView(INavigationInfoControlViewModel viewModel)
        {
            mViewModel = viewModel ?? throw new ArgumentNullException(nameof(viewModel));
            this.DataContext = mViewModel;

            InitializeComponent();
        }
    }
}
