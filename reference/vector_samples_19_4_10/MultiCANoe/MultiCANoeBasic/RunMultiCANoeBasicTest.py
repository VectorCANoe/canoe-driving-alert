
# -----------------------------------------------------------------------------
# Example: Multi CANoe Basic via Python COM API
#
# Requirements:
#  - set the can.ini property SingleCOMCLient' to value 1, otherwise there will only be one CANoe Instance
#  - make sure the CANoe configs are not already openend
#
# This sample demonstrates how to load and start the test modules and test
# via COM API using a Python script.
# The script uses the CoordinatorConfig.cfg and the AgentConfiguration.cfg configuration but the
# wrapper class is working also with any other CANoe configuration containing
# test modules and test configurations.
# -----------------------------------------------------------------------------
# Copyright (c) 2025 by Vector Informatik GmbH.  All rights reserved.
# -----------------------------------------------------------------------------


from win32com.client import *
from win32com.client.connect import *

import pythoncom, os, time


class CanoeSync(object):
    """Wrapper class for CANoe Application object, managing configuration, measurement, and test execution."""

    Started = False  # Indicates if measurement has started
    Stopped = False  # Indicates if measurement has stopped
    ClusterState = 0  # Tracks MultiCANoe cluster state
    TestConfigResult = 0  # Stores the result of the test configuration
    ConfigPath = ""  # Path to the configuration file
    CANoeMinorVersion = 0  # Minor version of CANoe
    eVerdicts = {  # Mapping of verdict codes to readable strings
        0:'cVerdictNotAvailable',
        1:'cVerdictPassed',
        2:'cVerdictFailed',
        3:'cVerdictNone',
        4:'cVerdictInconclusive'
    }

    def __init__(self):
        app = DispatchEx('CANoe.Application') # Create CANoe COM object
        ver = app.Version
        print('Loaded CANoe version ', 
          ver.major, '.',
          ver.minor, '.',
          ver.Build, '...', sep='')
        CanoeSync.CANoeMinorVersion = ver.minor
        self.App = app
        self.ConfigPath = ""
        self.ConfigFullName = ""
        self.Measurement = app.Measurement
        self.Measurement4 = CastTo(self.App.Measurement, "IMeasurement4") # Extended measurement interface
        WithEvents(self.App, CanoeApplicationEvents)
        WithEvents(self.App.Measurement, CanoeMeasurementEvents)
        DoEvents()
    
    def GetCANoeMinorVersion(self):
        return CanoeSync.CANoeMinorVersion
    
    def GetConfigurationName(self):
        return self.App.Configuration.Name
    
    def EnableWriteWindowOutputFile(self, filename, tabindex = 1):
        self.App.UI.Write.EnableOutputFile(filename, tabindex)

    def OutputTextOnWriteWindow(self, text):
        self.App.UI.Write.Output(text)

    def SetSimulatedBus(self, value):
        if value:
            self.App.Configuration.OnlineSetup.WorkingMode = 1
        else:
            self.App.Configuration.OnlineSetup.WorkingMode = 0

    def ChangeChannelMappingName(self, name):
        self.App.ChannelMappingName = name
    def Running(self):
        return self.Measurement.Running
    def WaitForStart(self, timeToWaitInSeconds = 20):
        return DoEventsUntil(lambda: CanoeSync.Started, timeToWaitInSeconds)
    def WaitForStop(self, timeToWaitInSeconds = 5):
        return DoEventsUntil(lambda: CanoeSync.Stopped, timeToWaitInSeconds)

    def WaitForClusterStateIncomplete(self, timeToWaitInSeconds = 5):
        return DoEventsUntil(lambda: CanoeSync.ClusterState == 0, timeToWaitInSeconds)
    def WaitForClusterStateInvalid(self, timeToWaitInSeconds = 5):
        return DoEventsUntil(lambda: CanoeSync.ClusterState == 1, timeToWaitInSeconds)
    def WaitForClusterStateConnected(self, timeToWaitInSeconds = 5):
        return DoEventsUntil(lambda: CanoeSync.ClusterState == 2, timeToWaitInSeconds)
    def WaitForClusterStateStarting(self, timeToWaitInSeconds = 5):
        return DoEventsUntil(lambda: CanoeSync.ClusterState == 3, timeToWaitInSeconds)
    def WaitForClusterStateRunning(self, timeToWaitInSeconds = 10):
        return DoEventsUntil(lambda: CanoeSync.ClusterState == 5, timeToWaitInSeconds)
    def WaitForClusterStateStopping(self, timeToWaitInSeconds = 5):
        return DoEventsUntil(lambda: CanoeSync.ClusterState == 4, timeToWaitInSeconds)

    def GetTestConfigResult(self):
        return CanoeSync.TestConfigResult

    def SetModified(self, modified):
        retries = 3
        for attempt in range(retries):
          try:
            self.App.Configuration.Modified = modified
            return
          except Exception as err:
              print(f"Attempt {attempt + 1}: Setting self.App.Configuration.Modified = {modified} failed: {err}")
              time.sleep(1) # Wait for 1 second before retrying

    def Load(self, cfgPath, withEvents = True):
        cfg = os.path.dirname(os.path.realpath(__file__))
        cfgFullName = os.path.join (cfg, cfgPath)
        print(cfgFullName)
        self.ConfigFullName = cfgFullName
        self.App.Open(cfgFullName)
        self.Configuration = self.App.Configuration
        if(withEvents):
            WithEvents(self.Configuration.MultiCANoe, MultiCANoeEvents)
        # TestConfigs property to access test configurations
        self.TestConfigs = []
        self.TestEnvironments = []
        self.TestModules = []
        DoEvents()

        return cfgFullName in self.Configuration.FullName

    def LoadTestConfiguration(self):
        """ Adds a test configuration and initialize it with a list of existing test units """
        testConfigurations = self.App.Configuration.TestConfigurations

        for tc in testConfigurations:
            # append TestConfig tc to self.TestConfigs
            self.TestConfigs.append(CanoeTestConfiguration(tc))

    def RunTestConfigs(self):
        """ starts all test configurations and waits for all of them to finish"""
        # start all test configurations
        for tc in self.TestConfigs:
            tc.Start()
        # wait for test modules to stop
        while not all([not tc.Enabled or tc.IsDone() or len(tc.TestUnits) == 0 for tc in self.TestConfigs]):
            DoEvents()

        return self.GetTestConfigResult()

    def LoadTestEnvironments(self):
        """ Gets the TestEnvironments objects and its containing list of existing test modules """ 
        testEnvironments = self.App.Configuration.TestSetup.TestEnvironments

        for testEnvironment in testEnvironments:
            self.TestEnvironments.append(testEnvironment)

    def RunTestEnvironments(self, moduleNames = None):
        """ starts test modules within each TestEnvironment object and waits for all of them to finish, only run specific modules if a list is provided"""  
        verdicts = {}

        for testEnvironment in self.TestEnvironments:
            testEnvironmentCasted = CastTo(testEnvironment, "ITestEnvironment2")  
            for testModule in testEnvironmentCasted.TestModules:
                tsTestModule = TSTestModule(testModule)
                if not moduleNames or tsTestModule.Name in moduleNames:
                    self.TestModules.append(tsTestModule)

                    # starts all test modules within the test environment
                    tsTestModule.Start()

        # wait for test modules to stop
        while not all([not testModule.Enabled or testModule.IsDone() for testModule in self.TestModules]):
            DoEvents() 
        # here we are sure the test modules has finished execution
        for testModule in self.TestModules:
            verdicts[testModule.Name] = testModule.Verdict()

        return verdicts

    def Start(self, timeToWaitInSeconds = 20): 
        DoEvents()
        if not self.Running():
            self.Measurement.Start()
            return self.WaitForStart(timeToWaitInSeconds)  

    def Stop(self):
        DoEvents()
        if self.Running():
            self.Measurement.Stop()
            CanoeSync.Started = False
            return self.WaitForStop()

    def StopEx(self):
        DoEvents()
        if self.Running():
            self.Measurement4.StopEx()
            CanoeSync.Started = False
            return self.WaitForStop()
        
    def StopExWithoutWaiting(self):
        DoEvents()
        if self.Running():
            self.Measurement4.StopEx()
            CanoeSync.Started = False

    def ConnectToRTServer(self, serverAdress):
        self.App.Configuration.DistributedMode.RTServer = serverAdress
        self.App.Configuration.DistributedMode.Connect

    def SetSystemVariable(self, nameSpace, variableName, variableValue):
        self.App.System.Namespaces.Item(nameSpace).Variables.Item(variableName).Value = variableValue
        
    def GetSystemVariable(self, nameSpace, variableName):
        return self.App.System.Namespaces.Item(nameSpace).Variables.Item(variableName).Value

    def Quit(self):
        retries = 3
        for attempt in range(retries):
          try:
            DoEvents()
            self.App.Quit()
            return
          except Exception as err:
              print(f"Attempt {attempt + 1}: Call App.Quit() failed: {err}")
              time.sleep(1) # Wait for 1 second before retrying

class CanoeApplicationEvents(object):
    """Handler for CANoe Application events"""
    def OnOpen(self, FullName):
        print("Configuration: "+FullName+" is opened")

    def OnQuit(self):
        print("CANoe is quit")

class CanoeMeasurementEvents(object):
    """Handler for CANoe Measurement events"""
    def OnStart(self):
        CanoeSync.Started = True
        CanoeSync.Stopped = False
    def OnStop(self): 
        CanoeSync.Started = False
        CanoeSync.Stopped = True

class TSTestModule:
    """Wrapper for a single test module in CANoe."""
    def __init__(self, testModule):
        self.testModule = testModule
        self.Name = testModule.Name
        self.Events = DispatchWithEvents(testModule, TestModuleEvents)
        self.IsDone = lambda: self.Events.stopped
        self.Enabled = testModule.Enabled

    def Verdict(self):
        return self.testModule.Verdict

    def Start(self):
        self.testModule.Start()


class CanoeTestConfiguration:
    """Wrapper class for a CANoe Test Configuration object"""
    def __init__(self, tc):        
        self.tc = tc
        self.Name = tc.Name
        self.Events = DispatchWithEvents(tc, CanoeTestEvents)
        self.ReportEvents = DispatchWithEvents(tc.Report, CanoeTestReportEvents)
        self.IsDone = lambda: self.Events.stopped
        self.Enabled = tc.Enabled

    def Start(self):
        DoEvents()
        if self.tc.Enabled:
            self.tc.Start()


class CanoeTestEvents:
    """Handles events for the test configuration lifecycle."""
    def __init__(self):
        self.started = False
        self.stopped = False
        self.verdict = False
        self.WaitForStart = lambda: DoEventsUntil(lambda: self.started)
        self.WaitForStop = lambda: DoEventsUntil(lambda: self.stopped)
        self.WaitForVerdictChange = lambda: DoEventsUntil(lambda: self.verdict)

    def OnStart(self):
        self.started = True
        self.stopped = False        

    def OnStop(self, reason):
        self.started = False
        self.stopped = True 

    def OnVerdictChanged(self, verdict):
        self.verdict = True
        CanoeSync.TestConfigResult = verdict


class CanoeTestReportEvents:
    """Utility class to handle the test events"""
    def __init__(self):
        self.generated = False
        self.WaitForGenerated = lambda: DoEventsUntil(lambda: self.generated)
    def OnGenerated(self, success, sourceFullPath, generatedFullPath):
        self.generated = True
        if not success:
            print("could not generate test report")


class TestModuleEvents:
    """Utility class to handle the test module events"""
    def __init__(self):
        self.started = False
        self.stopped = False        
        self.generated = False
        self.WaitForStart = lambda: DoEventsUntil(lambda: self.started)
        self.WaitForStop = lambda: DoEventsUntil(lambda: self.stopped)
        self.WaitForGenerated = lambda: DoEventsUntil(lambda: self.generated)
    def OnStart(self):
        self.started = True
        self.stopped = False
    def OnStop(self, reason):
        self.started = False
        self.stopped = True
    def OnReportGenerated(self, success, sourceFullName, generatedFullName):
        self.generated = True
        if not success:
            print("could not generate test module report")

class MultiCANoeEvents(object):
    """Handler for MultiCANoe events"""
    def OnClusterStateChanged(self, state):
        CanoeSync.ClusterState = state

def DoEvents():
    # Processes any pending COM messages (e.g., events from CANoe)
    pythoncom.PumpWaitingMessages()
    
    # Adds a short delay to avoid busy-waiting and reduce CPU usage
    time.sleep(.1)

def DoEventsUntil(cond, timeToWaitInSeconds):
    counter = 1  
    # Loop until the condition is met or timeout is reached
    while not cond() and counter <= (timeToWaitInSeconds * 10):
        DoEvents()  # Process events and wait briefly
        counter += 1
    
    # Return True if condition was met within the time limit, False otherwise
    return not (counter > timeToWaitInSeconds * 10)


def main():
    # in can.ini the property SingleCOMCLient has to be 1
    # otherwise there will only be one CANoe Instance 

    # make sure the CANoe configs are not already openend
    coordinator = CanoeSync()
    print("--- open coordinator ---")
    coordinator.Load("CoordinatorConfig.cfg")

    agent = CanoeSync()
    print("--- open agent ---")
    agent.Load("AgentConfig.cfg")


    # # please make sure the device has the same CANoe version
    # print("--- connect agent to RT Server ---")
    # agent.ConnectToRTServer("192.168.0.17")

    # # remove existing agents and add it such that the IP adress is correct
    # coordinator.App.Configuration.MultiCANoe.CoordinatorConfiguration.ParticipatingAgents.RemoveAll()
    # coordinator.App.Configuration.MultiCANoe.CoordinatorConfiguration.ParticipatingAgents.Add("Agent1@192.168.0.17:2810")


    print("--- wait for connection ---")
    is_connected = coordinator.WaitForClusterStateConnected()
    if not is_connected:
        raise AssertionError("MultiCANoe Cluster state is not connected within 5 seconds")

    print("--- start measurement ---")
    coordinator.Start()

    print("--- wait for ClusterStateRunning ---")
    is_running = coordinator.WaitForClusterStateRunning()
    if not is_running:
        raise AssertionError("MultiCANoe Cluster state is not running within 5 seconds")

    print("--- load tests ---")
    coordinator.LoadTestEnvironments()

    print("--- start tests ---")
    coordinator.RunTestEnvironments()

    # usually the function RunTestEnvironments waits until all tests are finished, but in this SampleConfig, the tests are loaded one after another and are only done when the system variable SuccessfulTestModules is 2
    print("--- wait until tests are finished ---")
    DoEventsUntil(lambda :coordinator.GetSystemVariable("MultiCANoe::Control::Test", "SuccessfulTestModules") == 2, 60*5)

    # print the verdicts of the test module 
    for testModule in coordinator.TestModules:
            print(f"Verdict of module {testModule.Name} is {coordinator.eVerdicts[testModule.Verdict()]}")

    print("--- stop the measurement ---")
    coordinator.Stop()

    print("--- close CANoe instances")
    coordinator.SetModified(False) # as the config may have changed, on closing the program asks to save, with this canoe instance ignores that the config was changed
    coordinator.Quit()
    agent.Quit()


if __name__ == "__main__":
    main()