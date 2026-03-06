# This Python Script starts and controls the CANSystem-Demo using System Variables
# The Variable IgnitionSwitch is assigned to the System Variable IgnitionSwitch
# The Variable Pedal is assigned to the System Variable PedalPressure_Gas
#-----------------------------------------------------------------------------
# Copyright (c) 2025 by Vector Informatik GmbH.  All rights reserved.

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
    Running = None
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
App = win32com.client.DispatchEx('CANoe.Application')
Measurement = App.Measurement
WithEvents(App, CanoeApplicationEvents)
WithEvents(App.Measurement, CanoeMeasurementEvents)

# stop measurement if one is still running
if Measurement.Running:
    Measurement.StopEx()
    while CanoeMeasurementEvents.Running:
        DoEvents()

busy_wait(1)

try:
    relpath = "CANSystem.cfg"
    FullPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),relpath)
    if not os.path.isfile(FullPath):
        raise FileNotFoundError(f"File not found: {FullPath}")
    # load the sample configuration
    App.Open(FullPath)
    busy_wait(1)

except Exception as e:
    errstring=f"Error opening configuration!\nError code: 0x{e.errno if hasattr(e, 'errno') else 'N/A'}\nSource: {type(e).__name__}\n"
    displayConsoleMessage(errstring)
    exit()

systemCAN = App.System
if systemCAN is None: 
    displayConsoleMessage('System object not found...')
    exit()

# access the system variable Ignition Switch
namespaces = systemCAN.Namespaces
nsIL = namespaces("IL")
IL_Vars = nsIL.Variables
IgnitionSwitch=IL_Vars("IgnitionSwitch")

# access the system variable PedalPosition
namespaces = systemCAN.Namespaces
nsPowerTrain = namespaces("PowerTrain")
powerTrainVars = nsPowerTrain.Variables
Pedal=powerTrainVars("PedalPressure_Gas")

# create a Panel object
Panels=App.Configuration.GeneralSetup.PanelSetup.Panels(0)
# assign the Control Panel to the Engine Panel object
Engine=Panels("Control")
Panels=None

# start the measurement
if not Measurement.Running:
    Measurement.Start()
    while not CanoeMeasurementEvents.Running:
        DoEvents()

if Engine is None:
    displayConsoleMessage("", "No Engine panel available")
else:
    Engine.Visible = False
    busy_wait(6)
    Engine.Visible = True
    Engine = None

# starting the car by turning the ignition switch
for IgnitionPosition in range(3):
    IgnitionSwitch.Value=IgnitionPosition
    busy_wait(0.5)

busy_wait(2)

for count in range(3):
    Pedal.Value=1
    busy_wait(3)
    Pedal.Value=0
    busy_wait(3)

busy_wait(6)

# stop the measurement
if Measurement.Running:
    Measurement.Stop()
    while CanoeMeasurementEvents.Running:
        DoEvents()

print("Environment script is done...")









        
    
