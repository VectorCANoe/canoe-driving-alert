/*----------------------------------------------------------------------------------------------------------------------
Module: CANoeFDX
------------------------------------------------------------------------------------------------------------------------
Datagram builder class for CANoe FDX protocol
------------------------------------------------------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/

#include "FDXDatagram.h"

#include <assert.h>
#include <cstring>

using namespace CANoeFDX;


FDXDatagram::FDXDatagram()
  : mSize(0)
{
  std::memset(mBuffer, 0, cCapacity);
}


void FDXDatagram::InitWithHeader()
{
  std::memset(mBuffer, 0, cCapacity);
  CANoeFDX::DatagramHeader* header = reinterpret_cast<CANoeFDX::DatagramHeader*>(mBuffer);
  header->fdxSignature = CANoeFDX::kFdxSignature;
  header->fdxMajorVersion = CANoeFDX::kFdxMajorVersion;
  header->fdxMinorVersion = CANoeFDX::kFdxMinorVersion;
  header->numberOfCommands = 0;
  header->seqNrOrDgramLen = CANoeFDX::kSequenceNumberUnused;
  header->fdxProtocolFlags = kByteOrderLittleEndian;
  header->reserved = 0;
  mSize = sizeof(CANoeFDX::DatagramHeader);
}


void FDXDatagram::SetSequenceNumber(uint16_t sequenceNumber)
{
  CANoeFDX::DatagramHeader* header = reinterpret_cast<CANoeFDX::DatagramHeader*>(mBuffer);
  header->seqNrOrDgramLen = sequenceNumber;
}


void  FDXDatagram::SetDatagramLength()
{
  CANoeFDX::DatagramHeader* header = reinterpret_cast<CANoeFDX::DatagramHeader*>(mBuffer);
  header->seqNrOrDgramLen = static_cast<uint16_t>(mSize);
}


void FDXDatagram::AddDataRequest(uint16_t groupID)
{
  auto header = AddCommand(CANoeFDX::kCommandCode_DataRequest, sizeof(CANoeFDX::DataRequestCommand));
  CANoeFDX::DataRequestCommand* command = static_cast<CANoeFDX::DataRequestCommand*>(header);
  command->groupID = groupID;
}


void* FDXDatagram::AddDataExchange(uint16_t groupID, uint16_t dataSize)
{
  auto header = AddCommand(CANoeFDX::kCommandCode_DataExchange, CANoeFDX::kDataExchangeBaseSize + dataSize);
  CANoeFDX::DataExchangeCommand* command = static_cast<CANoeFDX::DataExchangeCommand*>(header);
  command->groupID = groupID;
  command->dataSize = dataSize;
  return command->dataBytes;
}


void FDXDatagram::AddFreeRunningRequest(uint16_t groupID, uint16_t flags, uint32_t cycleTime, uint32_t firstDuration)
{
  auto header = AddCommand(CANoeFDX::kCommandCode_FreeRunningRequest, sizeof(CANoeFDX::FreeRunningRequestCommand));
  CANoeFDX::FreeRunningRequestCommand* command = static_cast<CANoeFDX::FreeRunningRequestCommand*>(header);
  command->groupID = groupID;
  command->flags = flags;
  command->cycleTime = cycleTime;
  command->firstDuration = firstDuration;
}


void FDXDatagram::AddFreeRunningCancel(uint16_t groupID)
{
  auto header = AddCommand(CANoeFDX::kCommandCode_FreeRunningCancel, sizeof(CANoeFDX::FreeRunningCancelCommand));
  CANoeFDX::FreeRunningCancelCommand* command = static_cast<CANoeFDX::FreeRunningCancelCommand*>(header);
  command->groupID = groupID;
}


void FDXDatagram::AddStart()
{
  AddCommand(CANoeFDX::kCommandCode_Start, sizeof(CANoeFDX::CommandHeader));
}


void FDXDatagram::AddStop()
{
  AddCommand(CANoeFDX::kCommandCode_Stop, sizeof(CANoeFDX::CommandHeader));
}


CANoeFDX::CommandHeader* FDXDatagram::AddCommand(uint16_t commandCode, uint16_t commandSize)
{
  CANoeFDX::DatagramHeader* header = reinterpret_cast<CANoeFDX::DatagramHeader*>(mBuffer);
  CANoeFDX::CommandHeader* command = reinterpret_cast<CANoeFDX::CommandHeader*>(mBuffer + mSize);
  assert(mSize + commandSize <= cCapacity);
  mSize += commandSize;
  header->numberOfCommands++;
  command->commandSize = commandSize;
  command->commandCode = commandCode;
  return command;
}


uint16_t IncrementSequenceNumber(uint16_t seqNr)
{
  if (seqNr == CANoeFDX::kSequenceNumberUnused)
  {
    return CANoeFDX::kSequenceNumberUnused;
  }
  else if (seqNr & CANoeFDX::kSequenceNumberSessionEndFlag)
  {
    return CANoeFDX::kSequenceNumberUnused;
  }
  else if (seqNr == 0x7FFF)
  {
    return 1;
  }
  else
  {
    return seqNr + 1;
  }
}
