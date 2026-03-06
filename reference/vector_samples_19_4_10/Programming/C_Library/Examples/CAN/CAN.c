// CAN.c : Example of a CANalyzer/CANoe C Library
//
// This sample file demonstrates the usage of the CAN bus in a 
// CANalyzer/CANoe C Library.
//

#include "CCL/CCL.h"


extern void OnMeasurementPreStart();
extern void OnMeasurementStart();
extern void OnTimer(int64_t time, int32_t timerID);
extern void OnCanMessage0x101(struct cclCanMessage* message);
extern void OnCanMessage0x102x(struct cclCanMessage* message);


int32_t gTimerID;


void cclOnDllLoad()
{
  cclSetMeasurementPreStartHandler(&OnMeasurementPreStart);
  cclSetMeasurementStartHandler(&OnMeasurementStart);
}


void OnMeasurementPreStart()
{
  int32_t rc;
  gTimerID = cclTimerCreate(&OnTimer);
  rc = cclCanSetMessageHandler(1, cclCanMakeStandardIdentifier(0x101), &OnCanMessage0x101);
  rc = cclCanSetMessageHandler(1, cclCanMakeExtendedIdentifier(0x102), &OnCanMessage0x102x);
}


void OnMeasurementStart()
{
  int32_t rc;
  rc = cclTimerSet(gTimerID, cclTimeMilliseconds(500) );
}


void OnTimer(int64_t time, int32_t timerID)
{
  int32_t channel = 1;
  uint32_t id = cclCanMakeExtendedIdentifier(0x100);
  uint32_t flags = 0;
  uint8_t dataLength = 8;
  uint8_t data[8] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08 };
  int32_t rc;

  rc = cclCanOutputMessage(channel, id, flags, dataLength, data);
  rc = cclTimerSet(gTimerID, cclTimeMilliseconds(500) );
}


void OnCanMessage0x101(struct cclCanMessage* message)
{
  cclWrite("C-API Example: OnCanMessage0x101");
}


void OnCanMessage0x102x(struct cclCanMessage* message)
{
  int32_t isExtendedIdentifier;
  int32_t isStandardIdentifier;
  uint32_t idValue;

  cclWrite("C-API Example: OnCanMessage0x102x");
  isExtendedIdentifier = cclCanIsExtendedIdentifier(message->id);
  isStandardIdentifier = cclCanIsStandardIdentifier(message->id);
  idValue = cclCanValueOfIdentifier(message->id);
}