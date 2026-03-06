using Vector.CANoe.TFS;
using Vector.CANoe.Threading;

[TestClass]
public class MyTestClass
{
  
  [Export]
  [TestCase]
  public static void SimpleTestCaseNet()
  {
    var value = 5.5;
    var expectedValue = value + 1.0;
    
    Report.TestStep($"Setting TestVariableWriteable to {value}");
    XILServer.MAPort.TestVariableWriteable.Value = value;

    Execution.Wait(200);
    
    Report.TestStep($"Checking TestVariableReadable value. Expected: {expectedValue}");
    if(XILServer.MAPort.TestVariableReadable.Value == expectedValue)
    {
      Report.TestStepPass("Test passed!");
      return;
    }

    Report.TestStep($"Actual: {XILServer.MAPort.TestVariableReadable.Value}");
    Report.TestStepFail("Test failed!");
  }
}