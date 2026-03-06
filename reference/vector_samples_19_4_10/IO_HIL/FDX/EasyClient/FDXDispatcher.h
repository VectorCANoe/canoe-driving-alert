/*----------------------------------------------------------------------------------------------------------------------
Module: CANoeFDX
------------------------------------------------------------------------------------------------------------------------
Datagram dispatcher class for CANoe FDX protocol
------------------------------------------------------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/
#pragma once

#include <stdint.h>
#include <stddef.h>

#include "CANoeFDX.h"
#include "FDXDatagram.h"



class IFDXDispatchCallbacks
{
public:
  virtual void OnFormatError() {};
  virtual void OnSequenceNumberError(CANoeFDX::DatagramHeader* header, uint16_t expectedSeqNr) {};

  virtual void OnStatus(CANoeFDX::DatagramHeader* header, CANoeFDX::StatusCommand* command) {};
  virtual void OnDataError(CANoeFDX::DatagramHeader* header, CANoeFDX::DataErrorCommand* command) {};
  virtual void OnDataExchange(CANoeFDX::DatagramHeader* header, CANoeFDX::DataExchangeCommand* command) {};
};



class FDXDispatcher
{
public:
  FDXDispatcher();

  void SetCallbacks(IFDXDispatchCallbacks* callbacks);

  bool CheckhDatagramHeader_TCP(FDXDatagram& datagram, size_t& datagramLength);
  bool CheckhDatagramHeader_UDP(FDXDatagram& datagram);
  void DispatchCommands(FDXDatagram& datagram);

private:
  IFDXDispatchCallbacks* mCallbacks;
  uint16_t mNextExpectedSeqNr;
};
