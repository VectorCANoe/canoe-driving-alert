# Example: TestFeatureSet
#
# This script demonstrates the usage of some COM-functions to control a 
# test setup.
#
# Exact description of the script:
# 1) First test configuration is chosen.
# 2) Check if the selected test configuration has already a verdict
#    a) if no verdict is available
#       - show information
#       - Start measurement
#       - Start test configuration
#    b) if verdict is available
#       - show information 
# 3) The test units of the selected test configuration 
#    are displayed
# 4) All passed and all failed testcases are listed
# 5) All passed testcases are disabled
# 6) The test configuration is started again
# 7) The verdict of the test configuration is shown
# 8) All failed testcases are listed
#
#
# The display is done in the Write-Window of the configuration.  
#
#-----------------------------------------------------------------------------
# Copyright (c) 2024 by Vector Informatik GmbH.  All rights reserved.

import time, os
from win32com.client import *
import win32com.client 
from win32com.client.connect import *
import msvcrt

# -----------------------------------------------------------------------------
# Output to console
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# script error: output to console and exit script
# -----------------------------------------------------------------------------

def displayConsoleMessageError(message):
    #Displays a message box with a custom message and thereafter exits the script
    displayConsoleMessage(message+"\nPress Enter to end the script")
    exit(1) 

# -----------------------------------------------------------------------------
# Exception handling
# -----------------------------------------------------------------------------

def exception_handling(err_num, msg_descr):
    if err_num != 0:
        if not msg_descr or msg_descr == "":
            msg_descr = "No error message description available"  # Default message if msg_descr is empty
        error_message = (
            f"Error type:{err_num} {msg_descr}\n"
            f"Invalid CANoe installation?\n"
            f"The script is aborted!"
        )
        displayConsoleMessage(error_message + "\nPress Enter to end the script")
        exit(1)

# -----------------------------------------------------------------------------
# Returns all items of the first test configuration
# -----------------------------------------------------------------------------

def GetAllItems(element, engageString):
    subElementsCount=0
    try:
        subElementsCount=element.Elements.Count 
    except Exception as e:
        exception_handling(type(e), "Items in the first test configuration couldn`t be accessed")

    if subElementsCount!=0:
        for i in range(subElementsCount):
            subElement=element.Elements.Item(i+1)
            WriteWindow.Output(engageString + subElement.Caption)
            
            engageString += "    "
            GetAllItems(subElement, engageString)
            engageString = engageString[:-4]

    subElementsCount=None
    subElement=None

# -----------------------------------------------------------------------------
#Goes through all test cases of a test configuration.
#If "disabled" is true, all test cases with verdict "verdict" are disabled.
#If "disabled" is false, then the names of the testcases with verdict "verdict"
#are written to the write window.
# -----------------------------------------------------------------------------
  
def GetAllTestcasesWithVerdict(element, verdict, disabled):
    subElementsCount=0
  
    try:
      subElementsCount=element.Elements.Count
    except Exception as e:
      exception_handling(type(e), "Items in the first test configuration couldn`t be accessed")
      e=None
  
    if subElementsCount!=0:
        for i in range(1, subElementsCount+1):
            subElement=element.Elements.Item(i) 
            verdictSubElement=0
            verdictSubElement=subElement.Verdict
            if verdictSubElement==verdict:
                if disabled==False:
                    WriteWindow.Output(f"    {subElement.Caption}")
                else:
                    subElement.Enabled=False
            
            GetAllTestcasesWithVerdict(subElement, verdict, disabled)
    
    subElementsCount=None
    subElement=None
    verdictSubElement=None

# -----------------------------------------------------------------------------
# Event Handlers
# -----------------------------------------------------------------------------

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
    Running=False
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
    Running=False
    reason = 0
    def OnStart(self):
        TestConfigurationEvents.reason = 0
        TestConfigurationEvents.Running = True
        print("< TestConfiguration started >")
    def OnStop(self, reason):
        TestConfigurationEvents.reason = reason
        TestConfigurationEvents.Running = False
        print("< TestConfiguration stopped >")           

#------------------------------------------------------------------------------------------------------------------------
#Main:
#------------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Start CANoe
# -----------------------------------------------------------------------------
# connect to CANoe

try:
    App = win32com.client.DispatchEx('CANoe.application')
    WithEvents(App, CanoeApplicationEvents)
    WithEvents(App.Measurement, CanoeMeasurementEvents)
except Exception as e:
    print(f"Error opening CANoe: {e}")
    exception_handling(e.errno, "CANoe run failure")

cfgdirectory = os.path.dirname(os.path.dirname(__file__))
cfgdirectory = os.path.join(cfgdirectory,'CentralLockingSystem.cfg')

#Opening CANoe configuration
try:
    App.Open(cfgdirectory)
except Exception as e:
    displayConsoleMessage(f"Error opening configuration: {e}\nPress Enter to end the script")
    exit()
busy_wait(1)


busy=1
while busy == 1:
    if len(App.Configuration.Name) == 0:
        displayConsoleMessage("No CANoe configuration is opened\nPress Enter to continue")
    else:
        busy=0
        busy_wait(0.3)

WriteWindow = App.UI.Write
try:
    WriteWindow.Output("TFS Example: TestFeatureSet Example is started")
except Exception as e:
    exception_handling(type(e), "Error writing output")

#-----------------------------------------------------------------------------
#Get first test configuration
#-----------------------------------------------------------------------------

try:
    #get the number of all test configurations
    testconfigCount=App.Configuration.TestConfigurations.Count
    if testconfigCount==0:
        displayConsoleMessageError("The current configuration does not contain any test configurations. The script is aborted")
        exit()
except Exception as e:
    exception_handling(type(e), "Error trying to access App.Configuration.TestConfigurations.Count")

currentTestConfig = App.Configuration.TestConfigurations.Item(1)
currentTestConfig = win32com.client.CastTo(currentTestConfig, 'ITestConfiguration9')

WithEvents(currentTestConfig, TestConfigurationEvents)

#-----------------------------------------------------------------------------
#Get verdict of first test configuration
#Write the structure of the test configuration in the write window
#List all passed and failed test cases in the write window
#-----------------------------------------------------------------------------
  
if currentTestConfig.Verdict == 0:
    
    displayConsoleMessage("\nTFS Example: The verdict of the first test configuration is not available.\n\n"
      "Therefore the script starts the test configuration.\n"
      "Afterwards the structure of the test configuration\n"
      "and the verdicts of all test cases are displayed in the write window.\nPress Enter to continue")
    
    if not App.Measurement.Running:
        #Compiling CAPL and starting measurement
        try:
            App.CAPL.Compile()
        except Exception as e:
            exception_handling(type(e),"CAPL compile failure")
        
        try:
            App.Measurement.Start()
            while not CanoeMeasurementEvents.Running:
                DoEvents()
        except Exception as e:
            exception_handling(type(e),"Start of measurement failed")

    
    currentTestConfig.Start()
    busy_wait(2)
        
    #Wait until test configuration is stopped
    while TestConfigurationEvents.Running == True or TestConfigurationEvents.reason == 1 or TestConfigurationEvents.reason == 2 :
        if TestConfigurationEvents.reason == 1:
            displayConsoleMessage("Test configuration was stopped by the user\nThe script will exit\nPress Enter to end the script")
            exit()
        elif TestConfigurationEvents.reason == 2:
            displayConsoleMessage("Test configuration was stopped by measurement stop\nThe script will exit\nPress Enter to end the script")
            exit()
        DoEvents()

    busy_wait(2)
else:
    displayConsoleMessage("\nTFS Example: The first test configuration has already been executed.\n\n"
      "The structure of the test configuration and the verdicts\n"
      "of all test cases will be displayed in the write window.\nPress Enter to continue")
     
#iterate through all test configuration items (test units, test groups, test fixtures, test sequences and testcases)
WriteWindow.Output("")
WriteWindow.Output("TFS Example: Test structure of the current test configuration '{}':".format(currentTestConfig.Name))
WriteWindow.Output("")

GetAllItems(currentTestConfig,"")

#List the passed and failed test cases
WriteWindow.Output("")
WriteWindow.Output("TFS Example: List of the passed test cases:")
GetAllTestcasesWithVerdict(currentTestConfig, 1, False)

WriteWindow.Output("")
WriteWindow.Output("TFS Example: List of the failed test cases")
GetAllTestcasesWithVerdict(currentTestConfig, 2, False)
WriteWindow.Output("")

#-----------------------------------------------------------------------------
#Disable all testcases with verdict "passed"
#-----------------------------------------------------------------------------

GetAllTestcasesWithVerdict(currentTestConfig, 1, True)

displayConsoleMessage("\nTFS Example: All test cases with verdict 'passed' are disabled by the script.\n"
      "Please review the selection of the test cases.\n\n"
      "Press Enter to continue and start the test configuration again")

#-----------------------------------------------------------------------------
#Start the current test configuration again
#-----------------------------------------------------------------------------

if not App.Measurement.Running:
    try:
        App.CAPL.Compile()
    except Exception as e:
        exception_handling(type(e),"CAPL compile failure")
        
    try:
        App.Measurement.Start()
        while not CanoeMeasurementEvents.Running:
            DoEvents()
    except Exception as e:
        exception_handling(type(e),"Start of measurement failed")

WriteWindow.Output("TFS Example: Start the current test configuration again")
WriteWindow.Output("")

currentTestConfig.Start()
busy_wait(2)

#resetting TestConfigurationEvents.reason
TestConfigurationEvents.reason == 0

#Wait until test configuration is stopped
while TestConfigurationEvents.Running == True or TestConfigurationEvents.reason == 1 or TestConfigurationEvents.reason == 2 :
    if TestConfigurationEvents.reason == 1:
        displayConsoleMessage("\nTest configuration was stopped by the user\nThe script will exit\nPress Enter to end the script")
        exit()
    elif TestConfigurationEvents.reason == 2:
        displayConsoleMessage("\nTest configuration was stopped by measurement stop\nThe script will exit\nPress Enter to end the script")
        exit()
    DoEvents()

#-----------------------------------------------------------------------------
#Display the verdict of the test configuration
#-----------------------------------------------------------------------------

WriteWindow.Output("")

if currentTestConfig.Verdict==0:
    stringVerdict = "Verdict not available"
elif currentTestConfig.Verdict==1:
    stringVerdict = "PASSED"
elif currentTestConfig.Verdict==2:
    stringVerdict = "FAILED"

WriteWindow.Output(f"TFS Example: Verdict of the test configuration is: {stringVerdict}")

displayConsoleMessage(f"\nTFS Example: Verdict of the test configuration is: {stringVerdict}\n\n"
      "The script is finished.\n"
      "Its sequence is documented in the write window.\nPress Enter to end the script")

WriteWindow.Output("")
WriteWindow.Output("TFS Example: List of failed test cases:")
GetAllTestcasesWithVerdict(currentTestConfig, 2, False)

#-----------------------------------------------------------------------------
#Finish the script
#-----------------------------------------------------------------------------   

WriteWindow.Output("")
WriteWindow.Output("TFS Example: TestFeatureSet Example finished.")