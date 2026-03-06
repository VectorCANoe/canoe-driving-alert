# -----------------------------------------------------------------------------
# Example: Diagnostics via Python COM API
# 
# Requirements: 
#  - install module pywin32: pip install pywin32
#
# This sample demonstrates how to perform diagnostic tests via COM API
# using a Python script.
# 
# Limitations:
#  - the script does not wait for test reports to be finished. If the test
#    reports are enabled, they may run in the background even after the test is 
#    finished
# -----------------------------------------------------------------------------
# Copyright (c) 2025 by Vector Informatik GmbH.  All rights reserved.
# -----------------------------------------------------------------------------

import time, os, msvcrt
from enum import Enum
from win32com.client import *
from win32com.client.connect import *


def DoEvents():
    pythoncom.PumpWaitingMessages()

def DoEventsUntil(cond):
    while not cond():
        DoEvents()

# use this helper function instead of time.sleep() to avoid "Server Busy" error; dt in seconds
def busy_wait(dt):       
    current_time = time.time()
    while (time.time() < current_time+dt):
        pythoncom.PumpWaitingMessages()

class CanoeSync(object):
    """Wrapper class for CANoe Application object"""
    Started = False
    Stopped = False
    ConfigPath = ""
    def __init__(self):
        app = DispatchEx('CANoe.Application')    
        ver = app.Version
        print('Loaded CANoe version ', 
            ver.major, '.', 
            ver.minor, '.', 
            ver.Build, '...', sep='')
        self.App = app
        self.Measurement = app.Measurement
        WithEvents(self.App, CanoeApplicationEvents)
        WithEvents(self.App.Measurement, CanoeMeasurementEvents)

    def Running(self):
        return self.Measurement.Running
    def WaitForStart(self):
        return DoEventsUntil(lambda: CanoeSync.Started)    
    def WaitForStop(self):
        return DoEventsUntil(lambda: CanoeSync.Stopped)

    def Load(self, cfgPath):
        # make sure current configuration has no modified flag
        self.App.Configuration.Modified = False
        # Compute absolute path to the configuration. In this sample, the configuration is located relative to the script file.
        cfg = os.path.dirname(os.path.realpath(__file__))
        cfg = os.path.join (cfg, cfgPath)
        print('Opening: ', cfg)
        self.ConfigPath = os.path.dirname(cfg)
        busy_wait(1)
        self.App.Open(cfg)
        self.Configuration = self.App.Configuration

    def Start(self): 
        if not self.Running():
            self.Measurement.Start()
            self.WaitForStart()

    def Stop(self):
        if self.Running():
            self.Measurement.Stop()
            self.WaitForStop()
       
    def RunTestConfigs(self):
        """ starts all test configurations and waits for all of them to finish """
        # start all test configurations
        for tc in self.Configuration.TestConfigurations:
            testconfiguration = CastTo(tc, "ITestConfiguration3")
            testconfiguration.Start()
            DoEventsUntil(lambda: testconfiguration.Running)
            print("Test configuration '"+testconfiguration.Caption+"' is running, please wait...", end="")
            DoEventsUntil(lambda: not testconfiguration.Running)
            print("finished!")

    def TraverseTestItem(self, parent, testf):
        for test in parent.TestModules: 
            testf(test)
        for folder in parent.Folders: 
            self.TraverseTestItem(folder, testf)

    def ReadSerialNumber(self, networkName, ecuQualifier):
        """ reads serial number """
        nw = self.App.Networks(networkName)
        ecu= nw.Devices(ecuQualifier)
        diag=ecu.Diagnostic
        print("Reading serial number from '"+ecuQualifier+"'!")
        req=diag.CreateRequest('SerialNumber_Read')
        req.Send()
        DoEventsUntil(lambda: not req.Pending)
        if req.Responses.Count == 0:
            print("No Response received!")
        else:
            for k in range (req.Responses.Count):
                resp=req.Responses(k+1)
                if resp.Positive:
                    serialNumber=resp.GetParameter('SerialNumber', 1)
                    print("Positive Response #"+str(k+1)+" received, Serial number="+str(serialNumber)+".")
                else:
                    print("Negative Response #"+str(k+1)+" received with response code "+str(resp.ResponseCode)+"!")
                
class CanoeApplicationEvents(object):
    """Handler for CANoe Application events"""
    def OnOpen(self, FullName):
        print("Configuration: '"+FullName+"' is opened")
    def OnQuit(self):
        print("CANoe is quit")

class CanoeMeasurementEvents(object):
    """Handler for CANoe Measurement events"""
    def OnInit(self):
        print("< measurement init >")
    def OnStart(self): 
        CanoeSync.Started = True
        CanoeSync.Stopped = False
        print("< measurement started >")
    def OnStop(self): 
        CanoeSync.Started = False
        CanoeSync.Stopped = True
        print("< measurement stopped >")
    def OnExit(self):
        print("< measurement exit >")

class StopReason(Enum):
    cStopReasonEnd=0
    cStopReasonUserAbort=1
    cStopReasonGeneralError=2
    cStopReasonVerdictImpact=3

class CanoeTestEvents:
    """Utility class to handle the test events"""
    def __init__(self):
        self.Running=False
        self.WaitForStart = lambda: DoEventsUntil(lambda: self.Running)
        self.WaitForStop = lambda: DoEventsUntil(lambda: not self.Running)
    def OnStart(self):     
        self.Running = True
        print("<", self.Name, " started >")
    def OnStop(self, reason):
        self.Running = False
        reason=StopReason(reason)
        print("<", self.Name, " stopped with reason: "+reason.name+" >")

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
app = CanoeSync()

# load the sample configuration
app.Load('..\\UDSSystem.cfg')

# start the measurement
app.Start()    

# Send a phsysical request and evaluate response
app.ReadSerialNumber('CAN1', 'DoorFL')

# Send a functional request and evaluate responses
app.ReadSerialNumber('CAN1', 'FunctionalGroup')

# run the test configurations
app.RunTestConfigs()

# wait for a keypress to stop the measurement
print("Press any key to stop the measurement ...")
while not msvcrt.kbhit():
    DoEvents()

# stop the measurement
app.Stop()
busy_wait(2)