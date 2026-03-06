#-----------------------------------------------------------------------------
# This Python Script uses the CANoe COM-API
# It starts CANoe, activates and runs all test units in all test configurations
# gathers the summary verdict and returns (errorlevel) the number of failed test configurations
# It outputs information on stdout and into a log file
# requires 2 parameters:
#  1st: path to CANoe configuration to use (it will not store changes in this file)
#  2nd: path to log file (any writeable text file path+name). It will rewrite the file on every run.
#-----------------------------------------------------------------------------
# Copyright (c) 2024 by Vector Informatik GmbH. All rights reserved.

import time, os
import sys
from win32com.client import *
import win32com.client
import win32com.client
import win32com.client
from win32com.client.connect import *
import msvcrt
from datetime import datetime

#Declaring Variables
CfgFilePath = None
LogFilePath = None
CanoeApp = None
Configuration = None
MeasurementRunning = None
ReportGenerated = None
LastTestResult = None
TestResults = None
TestConfigurations = None
TestConfiguration = None
TestUnit = None
FSO = None

# -----------------------------------------------------------------------------
# Creating a Message Box
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

def GetStopReasonText(reason):
    if reason==0:
        reasonText="Ended normally"
    elif reason==1:
        reasonText="User aborted"
    elif reason==2:
        reasonText="General error"
    elif reason==3:
        reasonText="Verdict impact"
    else:
        reasonText=f"Unknown reason: {reason}"
        print("< measurement stopped >")

    return reasonText

# -----------------------------------------------------------------------------
# Event Handlers
# -----------------------------------------------------------------------------

#Handler for CANoe.Application Events
class CanoeApplicationEvents(object):   
    """Handler for CANoe Application events"""
    def OnOpen(self, FullName):
        print("Configuration: " + FullName + " is opened")
    def OnQuit(self):
        print("CANoe is quit")

#Event Handler for CANoe.Application.Meassurement Events
class CanoeMeasurementEvents(object):
    """Handler for CANoe Measurement events"""
    Running = None
    def OnInit(self):
        pass
    def OnStart(self): 
        CanoeMeasurementEvents.Running = True
    def OnStop(self): 
        CanoeMeasurementEvents.Running = False
    def OnExit(self):
        pass

#Handler for CANoe.Application.Configuration.TestConfigurations.TestConfiguration Events
class TestConfigurationEvents(object):
    Running=False
    reason=0
    def OnStart(self):
        TestConfigurationEvents.reason = 0
        TestConfigurationEvents.Running = True  
    def OnStop(self,reason):
        TestConfigurationEvents.reason = reason
        TestConfigurationEvents.Running = False
        LogEntry(f"TestConfiguration - Stopped  -> {GetStopReasonText(TestConfigurationEvents.reason)}")
        print(f"TestConfiguration - Stopped  -> {GetStopReasonText(TestConfigurationEvents.reason)}")

def exception_handling(err_num, msg_descr):
    if err_num != 0:
        if not msg_descr or msg_descr == "":
            msg_descr = "No error message description available"  # Default message if msg_descr is empty
        error_message = (
            f"Error type:{err_num} {msg_descr}\n"
            f"Invalid CANoe installation?\n"
            f"The script is aborted!")
        print(error_message)
        exit(1)

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class TestItem:
    def __init__(self, name, result):
        self.name = name
        self.result = result

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def LogEntry(entry):
    global logFileObj
    global LogFilePath
    try:
        with open(LogFilePath, 'a') as logFileObj:
            logFileObj.write("\n"+entry)
    except Exception as e:
        exception_handling(type(e), "Error trying to write to the log file")

#rem -----------------------------------------------------------------------------------------------------   
def StopMeasurement():
    MeasurementRunning=CANoeApp.Measurement.Running
    if MeasurementRunning==True:
        CANoeApp.Measurement.StopEx()
        WaitFor(CanoeMeasurementEvents,"Running", False)

#rem -----------------------------------------------------------------------------------------------------
def StartMeasurement():
    MeasurementRunning=CANoeApp.Measurement.Running
    if not MeasurementRunning:
        CANoeApp.Measurement.Start()
        WaitFor(CanoeMeasurementEvents,"Running",True)

#rem -----------------------------------------------------------------------------------------------------
def GetVerdictText(verdict):
    if verdict==1:
        return "Passed"
    elif verdict == 2:
        return "Failed"
    elif verdict == 3:
        return "None"
    elif verdict == 4:
        return "Inconclusive"
    elif verdict == 5:
        return "Error in testsystem"
    else:
        return "Not available"

#rem -----------------------------------------------------------------------------------------------------
def CountExecutableElements(element,level,failed):
    if level==0:
        element= win32com.client.CastTo(element, 'ITestConfiguration9')
    executableElements=0
    for child in element.Elements:
        if (child.Type==4 or child.Type==5) and child.Verdict!=0:
            if failed:
                if child.Verdict!=1 and child.Verdict!=3:
                    executableElements=executableElements+1                 
            else:
                executableElements=executableElements+1
        executableElements=executableElements+CountExecutableElements(child, level+1,failed)
    
    return executableElements

#rem -----------------------------------------------------------------------------------------------------
def WaitFor(object,attr,state):
    i=0
    while getattr(object,attr)!=state:
        busy_wait(1)
        if i==100:
            displayConsoleMessage("Error, CANoe Event didn`t arise after more than 100s\nPress Enter to end the script")
            exit()
        i+=1 
    

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
#Creating FileSystemObject
FSO=os

#taking in the arguments from the .bat file
if len(sys.argv) == 3:
    CfgFilePath=sys.argv[1]
    LogFilePath=sys.argv[2]
else:
    print("Provide following arguments: CANoeConfigPath LogFilePath")
    print("Sample: AutomaticTest.py '..\\Cfg\\TestConfig.cfg' 'logs\\TestConfig.log'")
    print("")

if CfgFilePath == None or LogFilePath == None:
    displayConsoleMessage("Provide the following arguments: CANoeConfigPath LogFilePath\nThis script can also be started with StartAutomaticTests.bat when testing the CentralLockingSystem configuration\n\nPress Enter to end the script")
    exit()

#Setting up for writing of the log file, also see LogEntry() which is used to write to the log
try:
    LogFilePath=os.path.join(os.path.dirname(__file__),LogFilePath)
    print(f"The Log file is beeing written to: {LogFilePath}")
    if os.path.exists(LogFilePath):
        with open(LogFilePath, 'w') as logFileObj:
            logFileObj.write("")  # Emptying the file

    # Writing the initial log entries
    LogEntry("------------------------------------------------------------")
    LogEntry(f"Test started: {datetime.now()}")
    LogEntry("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print(f"Test started: {datetime.now()}")
    print("------------------------------------------------------------")
except Exception as e:
    print(f"Error regarding log file: {e}")

#Starting CANoe
try:
    CANoeApp=win32com.client.DispatchEx("CANoe.Application")
except Exception as e:
    exception_handling(type(e), "Error Starting CANoe")
Configuration=CANoeApp.Configuration
TestResults={}

#connecting measurement to measurement events
WithEvents(CANoeApp.Measurement, CanoeMeasurementEvents)

#Stopping measurement in case it`s allready running, see function definition
StopMeasurement()

#opening the configuration
path = os.path.abspath(__file__)
configpath = os.path.join(os.path.dirname(os.path.dirname(path)),CfgFilePath)
if not os.path.exists(configpath) or not CANoeApp.Configuration.FullName == configpath:
    try:
        CANoeApp.Open(configpath)
    except Exception as e:
        exception_handling(type(e), "Error opening the configuration")
    busy_wait(1)
LogEntry(f"CFG: {configpath}")
print(f"CFG: {configpath}")

LogEntry("*********** Activate and compile all test units ***********")
LogEntry(f"Compile all nodes of configuration: {CANoeApp.Configuration.Name}")
print("*********** Activate and compile all test units ***********")
print(f"Compile all nodes of configuration: {CANoeApp.Configuration.Name}")

StopMeasurement() #Stopping measurement in case it`s allready running, see function definition
CANoeApp.Configuration.CompileAndVerify()

name = "StandartTests"
retries = 1
while not LastTestResult and retries>0:
    LastTestResult=True
    LogEntry("")
    LogEntry(f"Running {name}...")
    LogEntry("")
    print("")
    print(f"Running {name}...")
    print("")

    StopMeasurement()

    TestConfigurations=CANoeApp.Configuration.TestConfigurations

    for TestConfiguration in TestConfigurations:
        TestConfiguration.Enabled=True
        TestConfigurationReport=TestConfiguration.Report
        TestConfigurationReport = win32com.client.CastTo(TestConfigurationReport, 'ITestConfigurationReport4')
        TestConfigurationReport.UseJointReport=True

        for TestUnit in TestConfiguration.TestUnits:
            TestUnit = win32com.client.CastTo(TestUnit, 'ITestUnit4')
            TestUnit.Enabled=True
            TestUnit.Report.Enabled=True

    StartMeasurement()
    
    #executing the test configurations
    if TestConfigurations.Count>0:
        LogEntry("")
        LogEntry("********************* Execution of all test configurations *********************")
        LogEntry(f"Found {TestConfigurations.Count} test configuration(s)")
        print("")
        print("********************* Execution of all test configurations *********************")
        print(f"Found {TestConfigurations.Count} test configuration(s)")

        for TestConfiguration in TestConfigurations:
            LogEntry("")
            LogEntry(f"---------- Executing TestConfiguration: '{TestConfiguration.Name}' ----------")
            print("")
            print(f"---------- Executing TestConfiguration: '{TestConfiguration.Name}' ----------")

            if TestConfiguration.Enabled:
                LogEntry(f"- executing test configuration: '{TestConfiguration.Name}'")
                print(f"- executing test configuration: '{TestConfiguration.Name}'")

                #attaching Testconfiguration to event handlers
                WithEvents(TestConfiguration,TestConfigurationEvents)
                TestConfigurationReport=TestConfiguration.Report
                TestConfigurationReport = win32com.client.CastTo(TestConfigurationReport, 'ITestConfigurationReport4')

                ReportGenerated=False
                TestConfiguration.Start()
                WaitFor(TestConfigurationEvents,"Running",True)
            

                while TestConfigurationEvents.Running:
                    DoEvents()

                LogEntry(f"     --> Verdict: {GetVerdictText(TestConfiguration.Verdict)}. Number of test cases/unsuccessful test cases: {CountExecutableElements(TestConfiguration,0,False)}/{CountExecutableElements(TestConfiguration,0,True)}")
                print(f"     --> Verdict: {GetVerdictText(TestConfiguration.Verdict)}. Number of test cases/unsuccessful test cases: {CountExecutableElements(TestConfiguration,0,False)}/{CountExecutableElements(TestConfiguration,0,True)}")

                if TestConfiguration.Verdict!=1 and TestConfiguration.Verdict!=3:
                    LogEntry("")
                    print("")
                    LastTestResult=False
            else:
                LogEntry(f" - will NOT run disabled test configuration: '{TestConfiguration.Name}'")
                print(f" - will NOT run disabled test configuration: '{TestConfiguration.Name}'")

        LogEntry(f"---------- Execution of TestConfiguration: '{TestConfiguration.Name}' finished ----------")
        print(f"---------- Execution of TestConfiguration: '{TestConfiguration.Name}' finished ----------")


    LogEntry("")
    LogEntry("********************* Execution of all test configurations finished ********************* ")

    #stoping measurement, if its still running
    StopMeasurement()       
    retries = retries-1

result = TestItem(name,LastTestResult)
TestResults[len(TestResults)]={'Result':result.result, 'Name':result.name}

StopMeasurement()
CANoeApp.Configuration.Modified = False

#Writing testresults to the log file
failed = False
LogEntry("")
LogEntry("------------------------------------------------------------")
LogEntry("TEST RESULTS")
LogEntry("------------------------------------------------------------")
print("")
print("------------------------------------------------------------")
print("TEST RESULTS")
print("------------------------------------------------------------")
for key in TestResults.keys():
    res = None
    if TestResults[key]['Result']:
        res = "PASSED"
    else:
        res = "Failed"
        failed = True
    LogEntry(f"{res}    {TestResults[key]['Name']}")
    print(f"{res}    {TestResults[key]['Name']}")
LogEntry("------------------------------------------------------------")
print("------------------------------------------------------------")
if failed:
    LogEntry("Test contains errors")
    print("Test contains errors")
else:
    LogEntry("Test finished succesfully")
    print("Test finished succesfully")
LogEntry("------------------------------------------------------------")
print("------------------------------------------------------------")

failed = 0

for key in TestResults.keys():
    if not TestResults[key]['Result']:
        failed=failed + 1
    
if failed > 0:
    LogEntry(f"GetScriptResult: found {failed} failed test(s).")
    print(f"GetScriptResult: found {failed} failed test(s).")
    

sys.exit(failed)