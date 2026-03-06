// Timer.cpp : Example of a CANalyzer/CANoe C Library
//
// This sample file demonstrates the usage of distribution objects
// without configured busses with CANalyzer/CANoe C Library.
//

#include "CCL/CCL.h"
#include <stddef.h>

extern void OnMeasurementPreStart();
extern void OnMeasurementStart();
extern void OnTimer1(int64_t time, int32_t timerID);
extern void WriteDoValues();
extern void ConsumerCallingHandler(cclTime time, cclCallContextID ccID);
extern void ProviderCallingHandler(cclTime time, cclCallContextID ccID);
extern void ConsumerCalledHandler(cclTime time, cclCallContextID ccID);
extern void ProviderCalledHandler(cclTime time, cclCallContextID ccID);
extern void ProviderReturningHandler(cclTime time, cclCallContextID ccID);
extern void ConsumerReturnedHandler(cclTime time, cclCallContextID ccID);
extern void FunctionResultHandler(cclTime time, cclCallContextID ccID);

int32_t gTimerID1;
int32_t inParamValue = 1988;
int32_t outParamValue = 2024;
int32_t returnValueReference = 2024 - 1988;

cclValueID do1Foo;  //Provider or Server
cclValueID do2Foo;  //Consumer or Client
cclCallContextID do2FooCallContextID;

cclValueID do1Field1;

void cclOnDllLoad()
{
   cclSetInterfaceType(CCL_APPLICATION_MODEL);
   cclSetMeasurementPreStartHandler(&OnMeasurementPreStart);
   cclSetMeasurementStartHandler(&OnMeasurementStart);
}


void OnMeasurementPreStart()
{
   gTimerID1 = cclTimerCreate(&OnTimer1);

   do1Foo = cclFunctionGetID(CCL_DISTRIBUTED_OBJECTS, "DOSpace::do1.Foo");
   do1Field1 = cclValueGetID(CCL_DISTRIBUTED_OBJECTS, "DOSpace::do1.Field1", NULL, CCL_PHYS);
   do2Foo = cclFunctionGetID(CCL_DISTRIBUTED_OBJECTS, "DOSpace::do2.Foo");
}


void OnMeasurementStart()
{
   cclWrite("Handle Timer");
   cclTimerSet(gTimerID1, cclTimeMilliseconds(1000));

   cclWrite("Handle Distributed Objects");
   WriteDoValues();

}

void OnTimer1(int64_t time, int32_t timerID)
{
   cclWrite("C Library Example: OnTimer1");
   cclTimerCancel(gTimerID1);

   // Registering DO handler
   if (cclFunctionSetHandler(do1Foo, CCL_CALL_STATE_CALLING, ProviderCallingHandler) != 0)
   {
      cclWrite("Not sucessful ProviderCallingHandler");
   }
   if (cclFunctionSetHandler(do1Foo, CCL_CALL_STATE_CALLED, ProviderCalledHandler) != 0)
   {
      cclWrite("Not sucessful ProviderCalledHandler");
   }
   if (cclFunctionSetHandler(do1Foo, CCL_CALL_STATE_RETURNING, ProviderReturningHandler) != 0)
   {
      cclWrite("Not sucessful ProviderReturningHandler");
   }


   if (cclFunctionSetHandler(do2Foo, CCL_CALL_STATE_CALLING, ConsumerCallingHandler) != 0)
   {
      cclWrite("Not sucessful ConsumerCallingHandler");
   }
   if (cclFunctionSetHandler(do2Foo, CCL_CALL_STATE_CALLED, ConsumerCalledHandler) != 0)
   {
      cclWrite("Not sucessful ConsumerCalledHandler");
   }
   if (cclFunctionSetHandler(do2Foo, CCL_CALL_STATE_RETURNED, ConsumerReturnedHandler) != 0)
   {
      cclWrite("Not sucessful ConsumerReturnedHandler");
   }

   // Set the inParam before the call
   cclValueSetInteger(cclCallContextValueGetID(do2FooCallContextID, CCL_MEMBER_IN_PARAM ".inParam", CCL_IMPL), inParamValue);

   // Client calls 
   //in vCDL we have defined foo as: provided method int32 Foo(in int32 inParam, out int32 outParam);
   do2FooCallContextID = cclCreateCallContext(do2Foo);
   cclCallAsync(do2FooCallContextID, FunctionResultHandler);
}

void WriteDoValues()
{
   int32_t rc;

   rc = cclValueSetInteger(do1Field1, 5);
   if (rc == 0) {
      cclWrite("Write DOTest::DistObj1.Field1 value");
   }
   else {
      cclWrite("Failed to write DOTest::DistObj1.Field1");
   }

   int64_t field1_value = 0;
   rc = cclValueGetInteger(do1Field1, &field1_value);

   if (field1_value == 5)
   {
      cclWrite("Write/Read of do1.Field1 was successful");
   }
   else
   {
      cclWrite("Write/Read of do1.Field1 was NOT successful");
   }
}


void ConsumerCallingHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>ConsumerCallingHandler<<<<<<<<<");
}

void ProviderCallingHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>ProviderCallingHandler<<<<<<<<<");
   //First we modify the in parameter of our defined function
   cclValueID valueID = cclCallContextValueGetID(ccID, CCL_MEMBER_IN_PARAM ".inParam", CCL_IMPL);

   //Double check if the value got set
   int64_t intValue = 0;
   cclValueGetInteger(valueID, &intValue);
   if (intValue == inParamValue)
   {
      cclWrite("In parameter of Foo got set correctly");
   }


}

void ConsumerCalledHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>ConsumerCalledHandler<<<<<<<<<");
}

void ProviderCalledHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>ProviderCalledHandler<<<<<<<<<");

   //Now we modify the out param
   cclValueID valueID = cclCallContextValueGetID(ccID, CCL_MEMBER_OUT_PARAM ".outParam", CCL_IMPL);
   cclValueSetInteger(valueID, outParamValue);

   int64_t intValue = 0;
   cclValueGetInteger(valueID, &intValue);
   if (intValue == outParamValue)
   {
      cclWrite("Out parameter of Foo got set correctly");
   }
}

void ConsumerReturningHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>ConsumerReturningHandler<<<<<<<<<");
}

void ProviderReturningHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>ProviderReturningHandler<<<<<<<<<");

   int64_t inParam, outParam;
   cclValueGetInteger(cclCallContextValueGetID(ccID, CCL_MEMBER_IN_PARAM ".inParam", CCL_IMPL), &inParam);
   cclValueGetInteger(cclCallContextValueGetID(ccID, CCL_MEMBER_OUT_PARAM ".outParam", CCL_IMPL), &outParam);

   if (inParam == inParamValue && outParam == outParamValue)
   {
      cclWrite("In and out parameters are still set correctly");
   }

   //Modify function result
   cclValueID valueID = cclCallContextValueGetID(ccID, CCL_MEMBER_RESULT, CCL_IMPL);
   cclValueSetInteger(valueID, (outParam - inParam));

   //Double check if the result got set
   int64_t intValue = 0;
   //cclValueGetInteger(valueID, &intValue);
   if (intValue == (outParamValue - inParamValue))
   {
      cclWrite("Foo result is correctly set to 36");
   }

}

void ConsumerReturnedHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>ConsumerReturnedHandler<<<<<<<<<");
}

void ProviderReturnedHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>ProviderReturnedHandler<<<<<<<<<");
}

void FunctionResultHandler(cclTime time, cclCallContextID ccID)
{
   cclWrite(">>>>>>>>>FunctionResultHandler<<<<<<<<<");

   int64_t inParam, outParam;
   cclValueGetInteger(cclCallContextValueGetID(ccID, CCL_MEMBER_IN_PARAM ".inParam", CCL_IMPL), &inParam);
   cclValueGetInteger(cclCallContextValueGetID(ccID, CCL_MEMBER_OUT_PARAM ".outParam", CCL_IMPL), &outParam);

   if (inParam == inParamValue && outParam == outParamValue)
   {
      cclWrite("In and out parameters are still set correctly");
   }


   int64_t intValue = 0;
   cclValueGetInteger(cclCallContextValueGetID(ccID, CCL_MEMBER_RESULT, CCL_IMPL), &intValue);
   if (intValue == (outParamValue - inParamValue))
   {
      cclWrite("Foo result is correctly set in function result handler");
   }

}