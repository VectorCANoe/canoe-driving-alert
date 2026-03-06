  # This example shows how to change the settings of an exporter.
  # The example can be used with the CANoe CANSystem - Demo.
  #
  #
  # The CSV settings will be changed programmatically and two CSV files with 
  # different settings will be created.
  #
  # The source file will be the logging file specified in the export dialog of
  # the logging block.
  #
 
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
    FullPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), relpath)
    CSVfolder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Logging")
    if not os.path.isfile(FullPath):
        raise FileNotFoundError(f"File not found: {FullPath}")
    # load the sample configuration    
    App.Open(FullPath)
    busy_wait(1)

except Exception as e:
    errstring=f"Error opening configuration!\nError code: 0x{e.errno if hasattr(e, 'errno') else 'N/A'}\nSource: {type(e).__name__}\n"
    displayConsoleMessage(errstring+"\nPress Enter to end the script")
    exit()

# Access the second Logging Block
Logging = App.Configuration.OnlineSetup.LoggingCollection(1)
Logging = win32com.client.CastTo(Logging, 'ILogging5')
Exporter = Logging.Exporter

# Load source file
Exporter.Load()

# Do CSV export with 1st settings
Exporter.Settings.CSVExt.ColumnSeparator = ";"
Exporter.Settings.CSVExt.DecimalSymbol = ","
Exporter.Settings.CSVExt.DecimalPlacesForSignalValue = 6
Exporter.Settings.CSVExt.DecimalPlacesForTimeChannel = 6
Exporter.Settings.CSVExt.TimeStampMode = 0
Exporter.Settings.CSVExt.ExportMode = 0

Exporter.Destinations.Clear()
Exporter.Destinations.Add(f"{CSVfolder}\\CSVSettings1.csv")

Exporter.Save(True)

# Do CSV export with 2nd settings
Exporter.Settings.CSVExt.ColumnSeparator = ";"
Exporter.Settings.CSVExt.DecimalSymbol = ","
Exporter.Settings.CSVExt.DecimalPlacesForSignalValue = 2
Exporter.Settings.CSVExt.DecimalPlacesForTimeChannel = 2
Exporter.Settings.CSVExt.TimeStampMode = 1
Exporter.Settings.CSVExt.ExportMode = 0

Exporter.Destinations.Clear()
Exporter.Destinations.Add(f"{CSVfolder}\\CSVSettings2.csv")

Exporter.Save(True)

displayConsoleMessage(f"\nThe logging file\n{Exporter.Sources(1)}\nwas successfully exported to \n..\\Logging\\CSVSettings1.csv and\n..\\Logging\\CSVSettings2.csv\n\nPress Enter to continue")

print("Logging Settings script done...")
