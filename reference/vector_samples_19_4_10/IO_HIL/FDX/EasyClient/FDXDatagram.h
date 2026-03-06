/*----------------------------------------------------------------------------------------------------------------------
Module: CANoeFDX
------------------------------------------------------------------------------------------------------------------------
Datagram builder class for CANoe FDX protocol
------------------------------------------------------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/
#pragma once

#include <stdint.h>
#include <stddef.h>

#include "CANoeFDX.h"


class FDXDatagram
{
public:
  FDXDatagram();

  // Clear the datagram buffer and then place the FDX datagram header.
  void  InitWithHeader();

  // For UDP as transport layer: Set the header field seqNrOrDgramLen to the give sequence number
  void  SetSequenceNumber(uint16_t sequenceNumber);

  // For TCP as transport layer: Set the header field seqNrOrDgramLen to the current datagram size, which is given
  // by the member variable mSize.
  void  SetDatagramLength();

  // Add a data request command to this datagram.
  void  AddDataRequest(uint16_t groupID);

  // Add a data exchange command to this datagram and return a pointer to the field 'dataBytes' of the command.
  void* AddDataExchange(uint16_t groupID, uint16_t dataSize);

  // Add a free running request command to this datagram.
  void  AddFreeRunningRequest(uint16_t groupID, uint16_t flags, uint32_t cycleTime, uint32_t firstDuration);

  // Add a free running cancel command to this datagram.
  void  AddFreeRunningCancel(uint16_t groupID);

  // Add a start command to this datagram.
  void  AddStart();

  // Add a stop command to this datagram.
  void  AddStop();

  inline void* Buffer() { return mBuffer; };
  inline uint32_t Size() { return mSize; }
  inline void Size(uint32_t s) { mSize = s; }
  inline uint32_t Capacity() { return cCapacity; }

  inline void* RemainingBuffer() { return mBuffer + mSize; }
  inline uint32_t RemainingSize() { return cCapacity - mSize; }

private:
  CANoeFDX::CommandHeader* AddCommand(uint16_t commandCode, uint16_t commandSize);

  static const uint32_t cCapacity = 65536;
  uint8_t mBuffer[cCapacity];
  uint32_t mSize;
};



uint16_t IncrementSequenceNumber(uint16_t seqNr);
