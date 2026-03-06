# This Python Script starts and checks the CANSystem-Demo using Signals
# The Variable EngSpeed is assigned to the Signal EngSpeed of the message EngineData
# The Variable CarSpeed is assigned to the Signal CarSpeed of the message ABSdata
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

def ShowSignal(name, signal):
    try:
        displayConsoleMessage(f"The current {name} is {signal.Value}\nPress Enter to continue")
    
    except AttributeError:
        displayConsoleMessage(f"The current {name} is not available\nPress Enter to continue")

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
    FullPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), relpath)
    if not os.path.isfile(FullPath):
        raise FileNotFoundError(f"File not found: {FullPath}")
    # load the sample configuration
    App.Open(FullPath)
    busy_wait(1)

except Exception as e:
    errstring=f"Error opening configuration!\nError code: 0x{e.errno if hasattr(e, 'errno') else 'N/A'}\nSource: {type(e).__name__}\n"
    displayConsoleMessage(errstring +"\nPress Enter to end the script")
    exit()

systemCAN=App.System
if systemCAN is None: 
    displayConsoleMessage("System object not found...\nPress Enter to end the script")
    exit()


# start the measurement
if not Measurement.Running:
    Measurement.Start()
    while not CanoeMeasurementEvents.Running:                        
        DoEvents() 
            

busy_wait(3)

#Starting the visual sequence automation in the simulation
DrivingCycleSequence=App.Configuration.GeneralSetup.VisualSequenceSetup.VisualSequences.Item(1).Start()

#letting the simulation roll for three seconds
busy_wait(3)

# access signals on the bus
EngSpeed = App.Bus.GetSignal(1,"EngineData","EngSpeed")
CarSpeed = App.Bus.GetSignal(1,"ABSdata","CarSpeed")



busy_wait(5)

# show values EngSpeed and CarSpeed in console message
ShowSignal("EngSpeed", EngSpeed)
ShowSignal("CarSpeed", CarSpeed)

#Stopping the visual sequence automation simulation
DrivingCycleSequence=App.Configuration.GeneralSetup.VisualSequenceSetup.VisualSequences.Item(1).Stop()

# stop the measurement
if Measurement.Running:
    Measurement.StopEx()
    while CanoeMeasurementEvents.Running:
        DoEvents() 



busy_wait(2)

#removing the visual sequence from the configuration
App.Configuration.GeneralSetup.VisualSequenceSetup.VisualSequences.Remove(1)
print("Signal script is done...")




