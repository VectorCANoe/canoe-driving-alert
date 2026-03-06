/*----------------------------------------------------------------------------------------------------------------------
Module: CANoeFDX
------------------------------------------------------------------------------------------------------------------------
Datagram dispatcher class for CANoe FDX protocol
------------------------------------------------------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/

#include "FDXDispatcher.h"



FDXDispatcher::FDXDispatcher()
  : mNextExpectedSeqNr(CANoeFDX::kSequenceNumberSessionStart)
{}


void FDXDispatcher::SetCallbacks(IFDXDispatchCallbacks* callbacks)
{
  mCallbacks = callbacks;
}


bool FDXDispatcher::CheckhDatagramHeader_TCP(FDXDatagram& datagram, size_t& datagramLength)
{
  CANoeFDX::DatagramHeader* header = reinterpret_cast<CANoeFDX::DatagramHeader*>(datagram.Buffer());

  if (datagram.Size() < sizeof(CANoeFDX::DatagramHeader))
  {
    mCallbacks->OnFormatError();
    return false;  // datagram is smaller as a header
  }

  if (header->fdxSignature != CANoeFDX::kFdxSignature)
  {
    mCallbacks->OnFormatError();
    return false;  // different value for magic cookie 
  }

  // fdx protocol version requirement: 2.1 or compatible

  if (!((header->fdxMajorVersion == CANoeFDX::kFdxMajorVersion2) &&
    (header->fdxMinorVersion >= CANoeFDX::kFDXMinorVersion1)))
  {
    mCallbacks->OnFormatError();
    return false; // version error
  }

  if ((header->fdxProtocolFlags & CANoeFDX::kByteOrderMask) == CANoeFDX::kByteOrderBigEndian)
  {
    mCallbacks->OnFormatError();
    return false;  // This client only supports little endian.
  }

  if (header->seqNrOrDgramLen < sizeof(CANoeFDX::DatagramHeader))
  {
    mCallbacks->OnFormatError();
    return false;  // A datagram length less then the size of the fdx protocol header is an error.
  }

  datagramLength = header->seqNrOrDgramLen;
  return true;
}


bool FDXDispatcher::CheckhDatagramHeader_UDP(FDXDatagram& datagram)
{
  CANoeFDX::DatagramHeader* header = reinterpret_cast<CANoeFDX::DatagramHeader*>(datagram.Buffer());

  if (datagram.Size() < sizeof(CANoeFDX::DatagramHeader))
  {
    mCallbacks->OnFormatError();
    return false;  // datagram is smaller as a header
  }

  if (header->fdxSignature != CANoeFDX::kFdxSignature)
  {
    mCallbacks->OnFormatError();
    return false;  // different value for magic cookie 
  }

  if (header->fdxMajorVersion != CANoeFDX::kFdxMajorVersion) // major version does not fit
  {
    mCallbacks->OnFormatError();
    return false; // version error
  }

  if ((header->fdxProtocolFlags & CANoeFDX::kByteOrderMask) == CANoeFDX::kByteOrderBigEndian)
  {
    mCallbacks->OnFormatError();
    return false;  // This client only supports little endian 
  }

  // Check Sequence Number
  if (header->seqNrOrDgramLen == CANoeFDX::kSequenceNumberUnused)
  {
    // sequence numbering unused => check nothing
  }
  else
  {
    if ((header->seqNrOrDgramLen & 0x7FFF) != mNextExpectedSeqNr)
    {
      mCallbacks->OnSequenceNumberError(header, mNextExpectedSeqNr);
    }
    if (header->seqNrOrDgramLen & CANoeFDX::kSequenceNumberSessionEndFlag)
    {
      mNextExpectedSeqNr = CANoeFDX::kSequenceNumberSessionStart;
    }
    else
    {
      mNextExpectedSeqNr = IncrementSequenceNumber(header->seqNrOrDgramLen);
    }
  }

  return true;
}


void FDXDispatcher::DispatchCommands(FDXDatagram& datagram)
{
  CANoeFDX::DatagramHeader* header = reinterpret_cast<CANoeFDX::DatagramHeader*>(datagram.Buffer());

  // Check The memory structure of the following commands.
  // Do this check for the whole datagram before any request is processed.
  {
    uint32_t offset = sizeof(CANoeFDX::DatagramHeader);
    uint32_t remainingBytes = datagram.Size() - offset;

    for (uint32_t i = 0; i < header->numberOfCommands; i++)
    {
      if (remainingBytes < sizeof(CANoeFDX::CommandHeader))
      {
        mCallbacks->OnFormatError();
        return;  // too small for command header
      }

      CANoeFDX::CommandHeader* command = reinterpret_cast<CANoeFDX::CommandHeader*>((char*)datagram.Buffer() + offset);
      if (remainingBytes < command->commandSize)
      {
        mCallbacks->OnFormatError();
        return;  // datagram is to small for this command
      }

      offset += command->commandSize;
      remainingBytes -= command->commandSize;
    }

    if (remainingBytes != 0)
    {
      mCallbacks->OnFormatError();
      return;  // there are some unused data bytes at the end of the datagram
    }
  }


  // Check the internal structure of the commands.
  {
    uint32_t offset = sizeof(CANoeFDX::DatagramHeader);
    for (uint32_t i = 0; i < header->numberOfCommands; i++)
    {
      CANoeFDX::CommandHeader* command = reinterpret_cast<CANoeFDX::CommandHeader*>((char*)datagram.Buffer() + offset);
      switch (command->commandCode)
      {
      case CANoeFDX::kCommandCode_DataExchange:
        if (command->commandSize < CANoeFDX::kDataExchangeBaseSize)
        {
          mCallbacks->OnFormatError();
          return;  // invalid size for DataExchange command, command is to small
        }
        if (command->commandSize < CANoeFDX::kDataExchangeBaseSize + static_cast<CANoeFDX::DataExchangeCommand*>(command)->dataSize)
        {
          mCallbacks->OnFormatError();
          return;  // invalid size for DataExchange command, payload does not fit into command
        }
        break;

      case CANoeFDX::kCommandCode_Status:
        if (command->commandSize < sizeof(CANoeFDX::StatusCommand))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      case CANoeFDX::kCommandCode_DataError:
        if (command->commandSize < sizeof(CANoeFDX::DataErrorCommand))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      case CANoeFDX::kCommandCode_DataRequest:
        if (command->commandSize < sizeof(CANoeFDX::DataRequestCommand))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      case CANoeFDX::kCommandCode_Key:
        if (command->commandSize < sizeof(CANoeFDX::KeyCommand))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      case CANoeFDX::kCommandCode_Start:
        if (command->commandSize < sizeof(CANoeFDX::CommandHeader))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      case CANoeFDX::kCommandCode_Stop:
        if (command->commandSize < sizeof(CANoeFDX::CommandHeader))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      case CANoeFDX::kCommandCode_HardwareChanged:
        if (command->commandSize < sizeof(CANoeFDX::CommandHeader))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      case CANoeFDX::kCommandCode_FreeRunningRequest:
        if (command->commandSize < sizeof(CANoeFDX::FreeRunningRequestCommand))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      case CANoeFDX::kCommandCode_FreeRunningCancel:
        if (command->commandSize < sizeof(CANoeFDX::FreeRunningCancelCommand))
        {
          mCallbacks->OnFormatError();
          return;
        }
        break;

      default:
        // ignore any unknown command
        break;
      }
      offset += command->commandSize;
    }
  }

  // Dispatch the commands.
  {
    uint32_t offset = sizeof(CANoeFDX::DatagramHeader);
    for (uint32_t i = 0; i < header->numberOfCommands; i++)
    {
      CANoeFDX::CommandHeader* command = reinterpret_cast<CANoeFDX::CommandHeader*>((char*)datagram.Buffer() + offset);
      switch (command->commandCode)
      {
      case CANoeFDX::kCommandCode_DataExchange:
        mCallbacks->OnDataExchange(header, static_cast<CANoeFDX::DataExchangeCommand*>(command));
        break;
      case CANoeFDX::kCommandCode_Status:
        mCallbacks->OnStatus(header, static_cast<CANoeFDX::StatusCommand*>(command));
        break;
      case CANoeFDX::kCommandCode_DataError:
        mCallbacks->OnDataError(header, static_cast<CANoeFDX::DataErrorCommand*>(command));
        break;
      default:
        // ignore any other command
        break;
      }
      offset += command->commandSize;
    }
  }
}
