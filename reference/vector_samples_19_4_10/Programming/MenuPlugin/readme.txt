
Vector.MenuPlugin Changelog
===========================
1.2.2.0 (no API modifications; only internal changes):
* Minor changes in package

1.2.1.0 (no API modifications; only internal changes):
* Project converted to SDK style.
* Build directories have changed 

1.1.0.0:
* The Vector.MenuPlugin assembly now targets the framework 4.7. Please update your existing plugins to also target this framework version.

To start the demo
=================
Enter the path to 'MenuPluginDemo.dll' in the [GUI] section of can.ini:

[GUI] 
MenuPlugin = <path to Programming>\MenuPlugin\bin\release\net47\MenuPluginDemo.dll 

Note: You have to restart the application to display the button.


Vector.MenuPlugin API Description
=================================
Use the Vector.MenuPlugin API to display a custom button with multiple subitems in the ribbon bar. It is displayed on the 'Environment' page of the ribbon bar.
The menu commands can perform any user-defined action, e.g. to launch an application.
You need to create a .NET Framework component for this:
* The Vector.MenuPlugin.dll component must be referenced in the assembly. 
  Note: Add a reference to the newest version of Vector.MenuPlugin.dll which is located in the \Exec64 directory of your installation. 
        Do not use the DLL that is found in the lib folder of the Sample Configurations. 
        Ensure that Copy Local is set to 'No' (false) in the project settings.
        Your project must target .NET Framework 4.7 or newer.
* The IMenuPlugin and IMenuItem interfaces are defined in the Vector.MenuPlugin namespace. Create two classes that implement these interfaces. 
  Note: For details regarding the interfaces, refer to the Vector.MenuPlugin help file:
        <Path to your CANoe Sample Configurations>\Programming\MenuPlugin\Vector.MenuPlugin.chm
* Build your component. 
* The component path must be entered in the can.ini as described above. 




