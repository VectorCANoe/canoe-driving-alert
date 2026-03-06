/*----------------------------------------------------------------------------------------------------------------------
Module: CANoeFDX
Interfaces: -
------------------------------------------------------------------------------------------------------------------------
Fast Data eXchange (FDX)
Protocol definition for connecting a HIL system over UDP or TCP to CANoe
------------------------------------------------------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/
#pragma once

#include <stdint.h>

namespace CANoeFDX
{
  // ===================================================================================================================
  // Version of CANoe FDX Protocol
  // ===================================================================================================================

  const uint8_t kFdxMajorVersion1 = 1;
  const uint8_t kFdxMajorVersion2 = 2;

  const uint8_t kFDXMinorVersion0 = 0;
  const uint8_t kFDXMinorVersion1 = 1;
  const uint8_t kFDXMinorVersion2 = 2;

  // current version of the protocol
  const uint8_t kFdxMajorVersion = kFdxMajorVersion2;
  const uint8_t kFdxMinorVersion = kFDXMinorVersion1;

  // ===================================================================================================================
  // DatagramHeader
  // Each datagram transmitted by the UDP protocol start with a header. The datagram header contains a signature
  // (magic cookie) and the version of the CANoe FDX protocol. The header is followed by one ore more command
  // structures. The field numberOfCommands specifies, how many command structures are following. The datagram header is
  // equipped with a sequence number, that enable CANoe and his counterpart to detect lost datagrams.
  // ===================================================================================================================

  const uint64_t kFdxSignature = 0x584446656F4E4143;

  const uint16_t kSequenceNumberUnused = 0x8000;
  const uint16_t kSequenceNumberSessionStart = 0x0000;
  const uint16_t kSequenceNumberSessionEndFlag = 0x8000;

  // FDX protocol flags
  const uint8_t kByteOrderMask = 0x01;
  const uint8_t kByteOrderLittleEndian = 0x00;
  const uint8_t kByteOrderBigEndian = 0x01;

  struct DatagramHeader
  {
    uint64_t fdxSignature;     // FDX signature, that is used as a magic cookie.This field must contain the value
                               // kFDXSignature otherwise the datagram is ignored.
    uint8_t fdxMajorVersion;   // major version of CANoe FDX protocol
    uint8_t fdxMinorVersion;   // minor version of CANoe FDX protocol
    uint16_t numberOfCommands; // number of commands, that are contained in the datagram
    uint16_t seqNrOrDgramLen;  // datagram sequence number (seqNr) of FDX session when using UDP as transport layer
                               // or datagram length (dramLen) when using TCP as transport layer
    uint8_t fdxProtocolFlags;  // Additional protocol flags. Currently only the least significant bit is used and
                               // indicates the byte order
    uint8_t reserved;          // One unused byte for a better alignment, may be used in a future version of the
                               // protocol. This field should be initialized to zero.
  };

  // ===================================================================================================================
  // CommandHeader
  // Each command structure starts with a command header. The header contains  the size of the complete command
  // structure and the command code.
  // ===================================================================================================================

  // The command code for the field  CommandHeader::commandCode
  const uint16_t kCommandCode_Start = 0x0001;
  const uint16_t kCommandCode_Stop = 0x0002;
  const uint16_t kCommandCode_Key = 0x0003;
  const uint16_t kCommandCode_Status = 0x004;
  const uint16_t kCommandCode_DataExchange = 0x0005;
  const uint16_t kCommandCode_DataRequest = 0x0006;
  const uint16_t kCommandCode_DataError = 0x0007;
  const uint16_t kCommandCode_FreeRunningRequest = 0x0008;
  const uint16_t kCommandCode_FreeRunningCancel = 0x0009;
  const uint16_t kCommandCode_StatusRequest = 0x000A;
  const uint16_t kCommandCode_SequenceNumberError = 0x000B;
  const uint16_t kCommandCode_FunctionCall = 0x000C;
  const uint16_t kCommandCode_FunctionCallError = 0x000D;

  const uint16_t kCommandCode_HardwareChanged = 0x0010;
  const uint16_t kCommandCode_IncrementTime = 0x0011;

  const uint16_t kCommandCode_Custom = 0x8000;
  const uint16_t kCommandCode_RT2RT_COM = 0x8001;

  struct CommandHeader
  {
    uint16_t commandSize; // size of this command in bytes
    uint16_t commandCode; // the kind of command
  };

  // ===================================================================================================================
  // KeyCommand
  // command code: kCommandCode_Key
  // Transmit a key stroke to the runtime kernel. This can invoke a 'on key' handler in CAPL.
  // ===================================================================================================================

  struct KeyCommand : CommandHeader
  {
    uint32_t canoeKeyCode; // key code as used CAPL programs of CANoe
                           // use code 0 for KEYUP events
  };

  // ===================================================================================================================
  // StatusCommand
  // command code: kCommandCode_Status
  // ===================================================================================================================

  const uint8_t kMeasurementState_NotRunning = 1;
  const uint8_t kMeasurementState_PreStart = 2;
  const uint8_t kMeasurementState_Running = 3;
  const uint8_t kMeasurementState_Stop = 4;

  struct StatusCommand : CommandHeader
  {
    uint8_t measurementState; // state of measurement (NotRunning, PreStart,Running, Stop)
    uint8_t reserved1;        // 3 unused bytes for better alignment
    uint8_t reserved2;
    uint8_t reserved3;
    int64_t timestamp; // current time of measurement in nanoseconds
  };

  // ===================================================================================================================
  // DataExchangeCommand
  // command code: kCommandCode_DataExchange (also used by kCommandCode_RT2RT_COM)
  // ===================================================================================================================

  // size of a DataExchangeCommand without data bytes
  const uint16_t kDataExchangeBaseSize = sizeof(CommandHeader) + 4;

  struct DataExchangeCommand : CommandHeader
  {
    uint16_t groupID;      // ID of the data group
    uint16_t dataSize;     // size of the following array
    uint8_t  dataBytes[1]; // the data bytes
  };

  // ===================================================================================================================
  // DataRequestCommand
  // command code: kCommandCode_DataRequest
  // ===================================================================================================================

  struct DataRequestCommand : CommandHeader
  {
    uint16_t groupID; // ID of the requested data group
  };

  // ===================================================================================================================
  // DataErrorCommand
  // command code: kCommandCode_DataError
  // ===================================================================================================================

  const uint16_t kDataErrorCode_NoError = 0;
  const uint16_t kDataErrorCode_MeasurementNotRunning = 1;
  const uint16_t kDataErrorCode_GroupIdInvalid = 2;
  const uint16_t kDataErrorCode_DataSizeTooLarge = 3;

  struct DataErrorCommand : CommandHeader
  {
    uint16_t groupID;       // ID of the data group, that was requested
    uint16_t dataErrorCode; // The reason, why CANoe cannot process the  data request command
  };

  // ===================================================================================================================
  // FreeRunningRequestCommand
  // command code: kCommandCode_FreeRunningRequest
  // ===================================================================================================================

  const uint16_t kFreeRunningFlag_TransmitAtPreStart = 1;
  const uint16_t kFreeRunningFlag_TransmitAtStop = 2;
  const uint16_t kFreeRunningFlag_TransmitCyclic = 4;
  const uint16_t kFreeRunningFlag_TransmitAtTrigger = 8;

  struct FreeRunningRequestCommand : CommandHeader
  {
    uint16_t groupID;       // ID of the data group, that is requested
    uint16_t flags;         // see constants kFreeRunningFlag_XXX
    uint32_t cycleTime;     // Time period in nanoseconds for the free running mode
    uint32_t firstDuration; // Time interval in nanoseconds for the first transmit cycle
  };

  // ===================================================================================================================
  // FreeRunningCancelCommand
  // command code: kCommandCode_FreeRunningCancel
  // ===================================================================================================================

  struct FreeRunningCancelCommand : CommandHeader
  {
    uint16_t groupID; // ID of the data group, for which the free running mode is canceled
  };

  // ===================================================================================================================
  // SequenceNumberErrorCommand
  // command code: kCommandCode_SequenceNumberError
  // ===================================================================================================================

  struct SequenceNumberErrorCommand : CommandHeader
  {
    uint16_t receivedSeqNr;
    uint16_t expectedSeqNr;
  };

  // ===================================================================================================================
  // HardwareChangedCommand
  // command code: kCommandCode_HardwareChanged
  // ===================================================================================================================

  struct HardwareChangedCommand : CommandHeader
  {
    uint32_t reserved;
  };

  // ===================================================================================================================
  // IncrementTimeCommand
  // command code: kCommandCode_IncrementTime
  // ===================================================================================================================

  struct IncrementTimeCommand : CommandHeader
  {
    uint32_t reserved1; // 4 unused bytes for better alignment
    uint64_t timestep;  // time in nanoseconds for the simulation step
  };

  // ===================================================================================================================
  // CustomCommand
  // command code: kCommandCode_Custom
  // ===================================================================================================================

  struct CustomCommand : CommandHeader
  {
    uint32_t commandID; // custom command ID
    uint32_t dataSize;  // size of custom command data
  };

  // ===================================================================================================================
  // FunctionCallCommand
  // command code: kCommandCode_FunctionCall
  // ===================================================================================================================

  // size of a FunctionCallCommand without data bytes
  const uint16_t kFunctionCallBaseSize = sizeof(CommandHeader) + 6;

  struct FunctionCallCommand : CommandHeader
  {
    uint16_t functionID;  // ID of the called function
    uint16_t requestID;   // customer specified numeric ID for associating calls with responses
    uint16_t dataSize;    // size of the following array
    uint8_t dataBytes[1]; // the data bytes
  };

  // ===================================================================================================================
  // FunctionCallErrorCommand
  // command code: kCommandCode_FunctionCallError
  // ===================================================================================================================

  const uint16_t kFunctionCallErrorCode_NoError = 0;
  const uint16_t kFunctionCallErrorCode_MeasurementNotRunning = 1;
  const uint16_t kFunctionCallErrorCode_FunctionIdInvalid = 2;
  const uint16_t kFunctionCallErrorCode_DataSizeTooLarge = 3;
  const uint16_t kFunctionCallErrorCode_ParameterFormat = 4;
  const uint16_t kFunctionCallErrorCode_Timeout = 5;
  const uint16_t kFunctionCallErrorCode_MeasurementStopped = 6;

  struct FunctionCallErrorCommand : CommandHeader
  {
    uint16_t functionID; // ID of the called function
    uint16_t requestID;  // customer specified numeric ID for associating calls with responses
    uint16_t errorCode;  // the reason why CANoe cannot process the function call
  };
} // namespace CANoeFDX
