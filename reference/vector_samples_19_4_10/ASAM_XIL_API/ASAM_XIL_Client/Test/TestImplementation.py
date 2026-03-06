import vector.canoe
import vector.canoe.threading
import vector.canoe.tfs
from application_layer import XILServer

@vector.canoe.tfs.export
@vector.canoe.tfs.test_case
def SimpleTestCasePy():
    value = 6.5
    expectedValue = value + 1.0

    vector.canoe.tfs.Report.test_step("", f"Setting TestVariableWriteable to {value}")
    XILServer.MAPort.TestVariableWriteable = value

    vector.canoe.threading.wait_for_timeout(200)
    
    vector.canoe.tfs.Report.test_step("", f"Checking TestVariableReadable value. Expected: {expectedValue}")
    if(XILServer.MAPort.TestVariableReadable.copy() == expectedValue):
      vector.canoe.tfs.Report.test_step_pass("", "Test passed!")
      return
    
    vector.canoe.tfs.Report.test_step("", f"Actual: {XILServer.MAPort.TestVariableReadable.copy()}")
    vector.canoe.tfs.Report.test_step_fail("", "Test failed!")
  