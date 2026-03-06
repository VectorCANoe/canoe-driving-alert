using System;
using System.Text;
using System.IO;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using Vector.CANoe.Runtime;
using Vector.Tools;

public class HttpRequestsHighLevel : MeasurementScript
{
    public override void Initialize()
    {
        Application.Panels.Local.ClientControlAddUser.name.Value = "John Doe";
        Application.Panels.Local.ClientControlAddUser.user_id.Value = 1;

        Application.Panels.Local.ClientControlGetUser.user_id.Value = 1;

        Application.Panels.Local.ClientControlDeleteUser.user_id.Value = 1;
    }


    [OnChange(Application.Panels.Local.ClientControlAddUser.MemberIDs.execute)]
    public void ExecuteLocalAddUser()
    {
        if (Application.Panels.Local.ClientControlAddUser.execute.Value == 1
            && Application.Panels.Local.ClientControlAddUser.mode.SymbValue == Application.Panels.HTTPBindingMode.USE_HIGH_LEVEL)
        {
            using var response = Application.Datatypes.Local.UserInformation.CreateInstance();
            Application.Panels.Local.ClientControlAddUser.response.Assign(response);
            using var requestData = Application.Datatypes.Local.UserInformation.CreateInstance();
            requestData.user_id.Value = Application.Panels.Local.ClientControlAddUser.user_id;
            requestData.name = Application.Panels.Local.ClientControlAddUser.name.Value;

            Application.HighLevel.LocalClient.AddUser.CallAsync(requestData, responseItem =>
            {
                Application.Panels.Local.ClientControlAddUser.response.user_id = responseItem.user_id;
                Application.Panels.Local.ClientControlAddUser.response.name = responseItem.name;
            });
        }
    }

    [OnChange(Application.Panels.Local.ClientControlGetUser.MemberIDs.execute)]
    public void ExecuteLocalGetUser()
    {
        if (Application.Panels.Local.ClientControlGetUser.execute.Value == 1
            && Application.Panels.Local.ClientControlGetUser.mode.SymbValue == Application.Panels.HTTPBindingMode.USE_HIGH_LEVEL)
        {
            using var response = Application.Datatypes.Local.UserInformation.CreateInstance();
            Application.Panels.Local.ClientControlGetUser.response.Assign(response);
            var user_id = Application.Panels.Local.ClientControlGetUser.user_id;

            Application.HighLevel.LocalClient.GetUser.CallAsync(user_id, responseItem =>
            {
                Application.Panels.Local.ClientControlGetUser.response.user_id = responseItem.user_id;
                Application.Panels.Local.ClientControlGetUser.response.name = responseItem.name;
            });
        }
    }

    [OnChange(Application.Panels.Local.ClientControlDeleteUser.MemberIDs.execute)]
    public void ExecuteLocalDeleteUser()
    {
        if (Application.Panels.Local.ClientControlDeleteUser.execute.Value == 1
            && Application.Panels.Local.ClientControlDeleteUser.mode.SymbValue == Application.Panels.HTTPBindingMode.USE_HIGH_LEVEL)
        {
            var user_id = Application.Panels.Local.ClientControlDeleteUser.user_id.Value;

            Application.HighLevel.LocalClient.DeleteUser.CallAsync(user_id);
        }
    }
}
