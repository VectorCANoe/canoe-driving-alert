# -----------------------------------------------------------------------------
# Example: Test Feature Set via Python COM API
# 
# Requirements: 
#  - install module pywin32: pip install pywin32
#
# This sample demonstrates how to load and start the test modules and test 
# configurations via COM API using a Python script.
# The script uses the included PythonBasicEmpty.cfg configuration but the  
# wrapper class is working also with any other CANoe configuration containing   
# test modules and test configurations. 
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
        # TestConfigs property to access test configurations
        self.TestConfigs = []
        # TestModules property to access test modules
        self.TestModules = [] 

    def LoadTestSetup(self, testsetup):
        self.TestSetup = self.App.Configuration.TestSetup
        path = os.path.join(self.ConfigPath, testsetup)
        testenv = self.TestSetup.TestEnvironments.Add(path)
        testenv = CastTo(testenv, "ITestEnvironment2")
        self.TraverseTestItem(testenv, lambda testmodule: self.TestModules.append(CanoeTestModule(testmodule)))
    
    def LoadTestConfiguration(self, testcfgname, listoftestunits):
        """ Adds a test configuration and initialize it with a list of existing test units """
        testconfiguration = self.App.Configuration.TestConfigurations.Add()
        testconfiguration.Name = testcfgname
        testunits = testconfiguration.TestUnits
        testunits = CastTo(testconfiguration.TestUnits, "ITestUnits2")
        for i in listoftestunits:
            testunits.Add(i)
        # append TestConfig testconfiguration to TestConfigs
        self.TestConfigs.append(CanoeTestConfiguration(testconfiguration))

    def Start(self): 
        if not self.Running():
            self.Measurement.Start()
            self.WaitForStart()

    def Stop(self):
        if self.Running():
            self.Measurement.Stop()
            self.WaitForStop()
       
    def RunTestModules(self):
        """ starts all test modules and waits for all of them to finish """
        # start all test modules
        for testmodule in self.TestModules:
            testmodule.Start()
        # wait for test modules to stop
        while not all([not testmodule.Enabled or testmodule.IsDone() for testmodule in self.TestModules]):
            DoEvents()

    def RunTestConfigs(self):
        """ starts all test configurations and waits for all of them to finish """
        # start all test configurations
        for testconfiguration in self.TestConfigs:
            testconfiguration.Start()
            DoEventsUntil(lambda: testconfiguration.IsDone())
            
        # wait for test configurations to stop
        while not all([not testconfiguration.Enabled or testconfiguration.IsDone() for testconfiguration in self.TestConfigs]):
            DoEvents()

    def TraverseTestItem(self, parent, testf):
        for test in parent.TestModules: 
            testf(test)
        for folder in parent.Folders: 
            self.TraverseTestItem(folder, testf)

class CanoeApplicationEvents(object):
    """Handler for CANoe Application events"""
    def OnOpen(self, FullName):
        print("Configuration: "+FullName+" is opened")
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

class CanoeTestModule:
    """Wrapper class for CANoe TestModule object"""
    def __init__(self, testmodule):
        self.testmodule = testmodule
        self.Events = DispatchWithEvents(testmodule, CanoeTestEvents)
        self.Name = testmodule.Name
        self.IsDone = lambda: not self.Events.Running
        self.Enabled = testmodule.Enabled
    def Start(self):
        if self.testmodule.Enabled:
            self.testmodule.Start()
            self.Events.WaitForStart()

class CanoeTestConfiguration:
    """Wrapper class for a CANoe Test Configuration object"""
    def __init__(self, testconfiguration):        
        self.testconfiguration = testconfiguration
        self.Name = testconfiguration.Name
        self.Events = DispatchWithEvents(testconfiguration, CanoeTestEvents)
        self.IsDone = lambda: not self.Events.Running
        self.Enabled = testconfiguration.Enabled
        self.Running=None
    def Start(self):
        if self.testconfiguration.Enabled:
            self.testconfiguration.Start()
            self.Events.WaitForStart()


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
app.Load('CANoeConfig\\PythonBasicEmpty.cfg')

# add test modules to the configuration
app.LoadTestSetup('TestEnvironments\\Test Environment.tse')

# add test configurations to the configuration
app.LoadTestConfiguration('TestConfiguration vTESTstudio', ['TestUnits\\PythonBasicTest vTESTstudio\\TestConfiguration\\EasyTest\\EasyTest.vtuexe'])
app.LoadTestConfiguration('TestConfiguration YAML', ['TestUnits\\TestUnit yaml\\TestEnvironment.vtestunit.yaml'])

# start the measurement
app.Start()    

# run the test modules
app.RunTestModules()

# run the test configurations
app.RunTestConfigs()

# wait for a keypress to stop the measurement
print("Press any key to stop the measurement ...")
while not msvcrt.kbhit():
    DoEvents()

# stop the measurement
app.Stop()
busy_wait(2)