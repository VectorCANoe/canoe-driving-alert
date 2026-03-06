// Ethernet.cpp : Example of a CANoe C Library
//
// This sample file demonstrates the usage of the Ethernet bus in a
// CANalyzer/CANoe C Library. This only works in channel-based Ethernet setups.
//

#include "CCL/CCL.h"

#include <string.h> // memcpy

extern void OnMeasurementPreStart();
extern void OnMeasurementStart();
extern void OnEthernetPacketReceived(struct cclEthernetPacket *packet);
extern void OnTimer(int64_t time, int32_t timerID);


int32_t gTimerID;
int32_t gChannel;

void cclOnDllLoad()
{
  cclSetMeasurementPreStartHandler(&OnMeasurementPreStart);
  cclSetMeasurementStartHandler(&OnMeasurementStart);
}

void OnMeasurementPreStart()
{
  int rc;

  gTimerID = cclTimerCreate(&OnTimer);
  rc = cclEthernetGetChannelNumber("Ethernet1", &gChannel);
  rc = cclEthernetSetPacketHandler(gChannel, &OnEthernetPacketReceived);
  if (rc != CCL_SUCCESS)
  {
    cclPrintf("Error setting message handler: %i", rc);
    if (rc == CCL_NOTSUPPORTED)
    {
      cclPrintf("C Library is only supported on channel-based Ethernet configurations!");
    }
  }
}

void OnMeasurementStart()
{
  int rc = cclTimerSet(gTimerID, cclTimeMilliseconds(500));
}

void OnTimer(int64_t time, int32_t timerID)
{
  int rc;
  uint8_t receiverMac[6] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06 };
  uint8_t senderMac[6]   = { 0x02, 0x84, 0xCF, 0x3B, 0xBE, 0x01 };
  uint8_t packetData[60] = { 0 };

  memcpy(&packetData[0], receiverMac, 6);
  memcpy(&packetData[6], senderMac, 6);

  rc = cclEthernetOutputPacket(gChannel, sizeof packetData, packetData);
}

void OnEthernetPacketReceived(struct cclEthernetPacket *packet)
{
  cclPrintf("C Library Example: OnEthernetPacketReceived at time %lli type: %i %i", packet->time, packet->packetData[12], packet->packetData[13]);
}
