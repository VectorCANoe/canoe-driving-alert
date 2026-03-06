  # This example shows some special features only available in the COM-Exporter.
  # The example can be used with the CANoe CANSystem - Demo.
  #
  #
  # The COM-Exporter has two special features used here:
  # 1. The batch export/conversion of more than one source files to the same 
  #    number of destination files (n to n) 
  # 2. The batch expor/conversion of more than one source file to one 
  #    destination file (n to 1)
  #
  # As source files the logging files configured in the first and a second logging
  # are used. 
  # The second logging block is added by this script, a automation visual sequence will be added and 
  # a log will be recorded. The second logging block will be removed at the end of the script
  #
  # Because by default the 2nd and 3rd logging block in the CANSystemDemo Demo
  # are not configured to start automatically the logging at measurement start 
  # you first have to make sure that logging files are created by:
  # 1. starting the logging blocks manually in measurement setup.
  # 2. changing the trigger configuration of the logging blocks.
  #----------------------------------------------------------------------------
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

# Displays a message in the console with a custom message.
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

# Stop measurement if one is still running
if Measurement.Running:
    Measurement.StopEx()
    while CanoeMeasurementEvents.Running:
        DoEvents()

busy_wait(1)

try:
    relpath="CANSystem.cfg"
    FullPath= os.path.join(os.path.dirname(os.path.dirname(__file__)), relpath)
    CSVfolder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "Logging")
    if not os.path.isfile(FullPath):
        raise FileNotFoundError(f"File not found: {FullPath}")
    
    # load the sample configuration 
    App.Open(FullPath)
    busy_wait(1)

except Exception as e:
    errstring=f"Error opening configuration!\nError code: 0x{e.errno if hasattr(e, 'errno') else 'N/A'}\nSource: {type(e).__name__}\n"
    displayConsoleMessage(errstring+"\nPress Enter to continue")
    exit()


# adding second logging block to configuration
SecondLoggingFile=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Logging\\CANoe_LogFile_2.blf")
App.Configuration.OnlineSetup.LoggingCollection.Add(SecondLoggingFile)


busy_wait(3)

# start the measurement
if not Measurement.Running:
    Measurement.Start()
    while not CanoeMeasurementEvents.Running:                        
        DoEvents() 
            
busy_wait(3)

# starting the visual sequence automation simulation
DrivingCycleSequence=App.Configuration.GeneralSetup.VisualSequenceSetup.VisualSequences.Item(1).Start()
print("Running visual sequence and recording log files for 25 seconds")

# waiting for 25seconds
busy_wait(25)

print("Ended visual sequence")

# stopping the visual sequence automation simulation
DrivingCycleSequence=App.Configuration.GeneralSetup.VisualSequenceSetup.VisualSequences.Item(1).Stop()

# stop the measurement
if Measurement.Running:
    Measurement.StopEx()
    while CanoeMeasurementEvents.Running:
        DoEvents() 

busy_wait(2)

# removing the visual sequence from the configuration
App.Configuration.GeneralSetup.VisualSequenceSetup.VisualSequences.Remove(1)

# Access the first and second Logging Block
Logging=App.Configuration.OnlineSetup.LoggingCollection(1)
Logging=win32com.client.CastTo(Logging, 'ILogging5')
Logging2=App.Configuration.OnlineSetup.LoggingCollection(2)
Logging2=win32com.client.CastTo(Logging2, 'ILogging5')
Exporter=Logging.Exporter

# Do n to n conversion
# Specify two source files and two logging files and start conversion.
Exporter.Sources.Clear()
Exporter.Sources.Add(Logging.FullName)
Exporter.Sources.Add(Logging2.FullName)

Exporter.Destinations.Clear()
Exporter.Destinations.Add(f"{CSVfolder}\\N_TO_N_1.asc")
Exporter.Destinations.Add(f"{CSVfolder}\\N_TO_N_2.asc")

Exporter.Load()
Exporter.Save(True)

displayConsoleMessage(f"The source files\n{Exporter.Sources(1)} and\n{Exporter.Sources(2)}\nwere successfully converted to\n..\\Logging\\N_TO_N_1.asc and\n..\\Logging\\N_TO_N_2.asc\n\nPress Enter to continue")

# Do n to 1 conversion.
# Two source files are specified. Now specify only one destination file.
Exporter.Destinations.Clear()
Exporter.Destinations.Add(f"{CSVfolder}\\N_TO_1.asc")

Exporter.Save(True)


displayConsoleMessage(f"The source files\n{Exporter.Sources(1)} and\n{Exporter.Sources(2)}\nwere successfully converted to\n..\\Logging\\N_TO_1.asc\n\nPress Enter to continue")

#Removing second logging block again
App.Configuration.OnlineSetup.LoggingCollection.Remove(2)

print("Logging Specials script done...")
