# -----------------------------------------------------------------------------
# Example: Central Locking System via Python COM API
# 
# This example shows the access to the Test Setup. 
# The script belongs to the CentralLockingSystem configuration.
# -----------------------------------------------------------------------------
# Copyright (c) 2024 by Vector Informatik GmbH.  All rights reserved.
# -----------------------------------------------------------------------------

import time, os
from win32com.client import *
from win32com.client.connect import *
import msvcrt

# Handler for CANoe.Application Events
class CanoeApplicationEvents(object):
    """Handler for CANoe Application events"""
    def OnOpen(self, FullName):
        print("Configuration: " + FullName + " is opened")
    def OnQuit(self):
        print("CANoe is quit")

# Handler for CANoe.Application.Meassurement Events
class CanoeMeasurementEvents(object):
    """Handler for CANoe Measurement events"""
    Running = False
    def OnInit(self):
        print("< measurement init >")
    def OnStart(self): 
        CanoeMeasurementEvents.Running = True
        print("< measurement started >")
    def OnStop(self): 
        CanoeMeasurementEvents.Running = False
        print("< measurement stopped >")
    def OnExit(self):
        print("< measurement exit >")

# Handler for CANoe.Application.Configuration.TestConfiguration.TestConfiguration Events
class TestConfigurationEvents(object):
    Running = False
    def OnStart(self):
        TestConfigurationEvents.Running = True
        print("< TestConfiguration started >")
    def OnStop(self,reason):
        TestConfigurationEvents.Running = False
        print("< TestConfiguration stopped >")

#------------------------------------------------------------------------------------------------------------------------
#Functions:
#------------------------------------------------------------------------------------------------------------------------
# Helper function for displayConsoleMessage
def clear_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()

def DoEvents():
    pythoncom.PumpWaitingMessages()

#Displays a message in the console with a custom message.
def displayConsoleMessage(message):
    clear_buffer()
    print(message)
    while not msvcrt.kbhit():
      DoEvents() 
    clear_buffer()

# use this helper function instead of time.sleep; dt in seconds
def busy_wait(dt):       
    current_time = time.time()
    while (time.time() < current_time+dt):
        pythoncom.PumpWaitingMessages()

#------------------------------------------------------------------------------------------------------------------------
#Main:
#------------------------------------------------------------------------------------------------------------------------
print("Starting the CANoe Application")
App = win32com.client.DispatchEx('CANoe.Application')
Measurement = App.Measurement
WithEvents(App, CanoeApplicationEvents)
WithEvents(App.Measurement, CanoeMeasurementEvents)

#If a CANoe Measurement is already running, it will be stopped
if Measurement.Running:
    Measurement.StopEx()
    while CanoeMeasurementEvents.Running:
        DoEvents()

cfgdirectory = os.path.dirname(os.path.dirname(__file__))
cfgdirectory = os.path.join(cfgdirectory,'CentralLockingSystem.cfg')

#Opening CANoe configuration
try:
    App.Open(cfgdirectory)
except Exception as e:
    displayConsoleMessage(f"Error opening configuration: {e}\nPress Enter to end the script")
    exit()
busy_wait(1)

Measurement         = App.Measurement
TestConfigurations  = App.Configuration.TestConfigurations
TestConfiguration   = App.Configuration.TestConfigurations.Item(1)
FirstTestUnit = App.Configuration.TestConfigurations.Item(1).TestUnits.Item(1)

# Casting the TestUnit Object in order to gain writing access to the .Enabled property
FirstTestUnit = win32com.client.CastTo(FirstTestUnit, 'ITestUnit4')
FirstTestUnit.Enabled = False

# Starting Mearuement and waiting for OnOpen Event
Measurement.Start()
while not CanoeMeasurementEvents.Running:
    DoEvents()

# Casting the Testconfiguration in order to gain the ability of accesing all it`s properties
TestConfiguration = win32com.client.CastTo(TestConfiguration, 'ITestConfiguration9')
WithEvents(TestConfiguration, TestConfigurationEvents)

TestConfiguration.Start()
while not TestConfigurationEvents.Running:
    DoEvents()

while TestConfigurationEvents.Running:
    DoEvents()

Measurement.Stop()
while CanoeMeasurementEvents.Running:
    DoEvents()

TMVerdict = TestConfiguration.Verdict
if TMVerdict == 0:
    displayConsoleMessage("\nVerdict not available\n\nPress Enter to continue")
elif TMVerdict == 1:
    displayConsoleMessage("\nVerdict Passed\n\nPress Enter to continue")
elif TMVerdict == 2:
    displayConsoleMessage("\nVerdict Failed\n\nPress Enter to continue")
elif TMVerdict == 3:
    displayConsoleMessage("\nVerdict None\n\nPress Enter to continue")
elif TMVerdict == 4:
    displayConsoleMessage("\nVerdict Inconclusive\n\nPress Enter to continue")
elif TMVerdict == 5:
    displayConsoleMessage("\nVerdict Error in testsystem\n\nPress Enter to continue")
else:
    displayConsoleMessage("\nError: Invalid Verdict Value\n\nPress Enter to continue")

print("CANoe Testsetup script is done...")

