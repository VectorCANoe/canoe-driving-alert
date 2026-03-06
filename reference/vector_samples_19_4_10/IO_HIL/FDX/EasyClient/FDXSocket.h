/*----------------------------------------------------------------------------------------------------------------------
Module: CANoeFDX
------------------------------------------------------------------------------------------------------------------------
Socket wrapper for CANoe FDX protocol based on the boost::asio library.
------------------------------------------------------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/
#pragma once

#include <stdint.h>
#include <stddef.h>
#include <boost/asio.hpp>

#include "CANoeFDX.h"
#include "FDXDispatcher.h"



// ---------------------------------------------------------------------------------------------------------------------
// FDXSocket
// 
// Common interface for both Socket wrappers (UDP and TCP).
// ---------------------------------------------------------------------------------------------------------------------


class FDXSocket
{
public:
  virtual ~FDXSocket();

  // Set the dispatcher functions, that are called after receiving a FDX datagram.
  virtual void SetDispatcher(FDXDispatcher* dispatcher) = 0;

  // Send an FDX datagram to CANoe.
  virtual void SendFdxDatagram(FDXDatagram& datagram) = 0;

  // In case of UDP as transport layer a sequence counting feature can be used to detect lost UDP datagrams.
  // After calling FinishSequenceCounting, the next datagram will end the current counting sequence.
  virtual bool FinishSequenceCounting() = 0;
};


// ---------------------------------------------------------------------------------------------------------------------
// FDXSocketUDP
// 
// Socket wrapper for UDP
// ---------------------------------------------------------------------------------------------------------------------


class FDXSocketUDP : public FDXSocket
{
public:
  FDXSocketUDP(
    boost::asio::io_context& context,
    const boost::asio::ip::udp::endpoint& localEndpoint,
    const boost::asio::ip::udp::endpoint& canoeEndpoint);

  virtual ~FDXSocketUDP();

  void SetDispatcher(FDXDispatcher* dispatcher) override;
  void SendFdxDatagram(FDXDatagram& datagram) override;
  bool FinishSequenceCounting() override;

private:

  void StartReceive();

  FDXDispatcher* mFDXDispatcher;

  boost::asio::ip::udp::endpoint mLocalEndpoint;
  boost::asio::ip::udp::endpoint mCANoeEndpoint;
  boost::asio::ip::udp::socket   mSocket;

  boost::asio::ip::udp::endpoint mReceiveFromEndpoint;
  FDXDatagram                    mReceiveDatagram;

  uint16_t                       mNextTransmitSequenceNumber;
};


// ---------------------------------------------------------------------------------------------------------------------
// FDXSocketTCP
//
// Socket wrapper for TCP
// ---------------------------------------------------------------------------------------------------------------------


class FDXSocketTCP : public FDXSocket
{
public:
  FDXSocketTCP(
    boost::asio::io_context& context,
    const boost::asio::ip::tcp::endpoint& localEndpoint,
    const boost::asio::ip::tcp::endpoint& canoeEndpoint);

  virtual ~FDXSocketTCP();

  void SetDispatcher(FDXDispatcher* dispatcher) override;
  void SendFdxDatagram(FDXDatagram& datagram) override;
  bool FinishSequenceCounting() override;

private:

  enum ReceiveState
  {
    eReceiveIdle,
    eReceiveError,
    eReceiveHeader,
    eReceiveCommands
  };

  void StartReceive();
  void OnReceived(const boost::system::error_code& errorCode, std::size_t bytesReceived);

  FDXDispatcher* mFDXDispatcher;

  boost::asio::ip::tcp::endpoint mLocalEndpoint;
  boost::asio::ip::tcp::endpoint mCANoeEndpoint;
  boost::asio::ip::tcp::socket   mSocket;

  FDXDatagram                    mReceiveDatagram;
  ReceiveState                   mReceiveState;
  size_t                         mReceiveBytesRequired;
};






