using System;
using System.Windows.Input;

namespace Demo.Wpf.Helper
{
    internal class RelayCommand : ICommand
    {
        private readonly Action<Object> mExecute;
        private readonly Predicate<Object> mCanExecute;

        public event EventHandler CanExecuteChanged
        {
            add => CommandManager.RequerySuggested += value;
            remove => CommandManager.RequerySuggested -= value;
        }

        public RelayCommand(Action<Object> execute, Predicate<Object> canExecute = null)
        {
            mExecute = execute ?? throw new ArgumentNullException(nameof(execute));
            mCanExecute = canExecute;
        }

        public Boolean CanExecute(Object parameter)
        {
            return mCanExecute == null || mCanExecute(parameter);
        }

        public virtual void Execute(Object parameter)
        {
            mExecute(parameter);
        }
    }
}
