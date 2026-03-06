/*----------------------------------------------------------------------------------------------------------------------
Module: CANoeFDX
------------------------------------------------------------------------------------------------------------------------
Socket wrapper for CANoe FDX protocol based on the boost::asio library.
------------------------------------------------------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/

#include "FDXSocket.h"

#include <iostream>

// ---------------------------------------------------------------------------------------------------------------------
// FDXSocket
// ---------------------------------------------------------------------------------------------------------------------

FDXSocket::~FDXSocket()
{}

// ---------------------------------------------------------------------------------------------------------------------
// FDXSocketUDP
// ---------------------------------------------------------------------------------------------------------------------


FDXSocketUDP::FDXSocketUDP(boost::asio::io_context& context,
  const boost::asio::ip::udp::endpoint& localEndpoint,
  const boost::asio::ip::udp::endpoint& canoeEndpoint)
  : mFDXDispatcher(nullptr)
  , mLocalEndpoint(localEndpoint)
  , mCANoeEndpoint(canoeEndpoint)
  , mSocket(context)
  , mReceiveFromEndpoint()
  , mReceiveDatagram()
  , mNextTransmitSequenceNumber(CANoeFDX::kSequenceNumberSessionStart)
{
  // Open socket
  boost::system::error_code opendErrorCode;
  mSocket.open(localEndpoint.protocol(), opendErrorCode);
  if (opendErrorCode)
  {
    std::cerr << "Opening UDP socket failed." << std::endl;
    context.stop();
    return;
  }

  // Binding the UDP socket to the local endpoint.
  boost::system::error_code bindErrorCode;
  mSocket.bind(localEndpoint, bindErrorCode);
  if (bindErrorCode)
  {
    std::cerr << "Binding UDP socket failed." << std::endl;
    context.stop();
    return;
  }

  StartReceive();
}


FDXSocketUDP::~FDXSocketUDP()
{
}

void FDXSocketUDP::SetDispatcher(FDXDispatcher* dispatcher)
{
  mFDXDispatcher = dispatcher;
}


void FDXSocketUDP::StartReceive()
{
  auto handler = [this](const boost::system::error_code& errorCode, std::size_t bytesReceived)
  {
    if (errorCode)
    {
      if (errorCode == boost::system::errc::connection_refused)
      {
        // This error message is typically received after sending a UDP datagram and there is no application on the 
        // target machine available, that has opened the addressed UDP port.
        // Check that CANoe is running, the FDX feature is enabled and the correct port number is used.
        std::cerr << "Target machine refuses a UDP datagram." << std::endl;
      }
      else
      {
        std::cerr << "Receive from UDP socket failed."
          << " (" << std::dec << errorCode.value() << " '" << errorCode.message() << "')" << std::endl;
      }
    }
    else
    {
      mReceiveDatagram.Size(static_cast<uint32_t>(bytesReceived));
      if (mFDXDispatcher->CheckhDatagramHeader_UDP(mReceiveDatagram))
      {
        mFDXDispatcher->DispatchCommands(mReceiveDatagram);
      }
    }
    StartReceive();
  };

  mSocket.async_receive_from(
    boost::asio::buffer(mReceiveDatagram.Buffer(), mReceiveDatagram.Capacity()),
    mReceiveFromEndpoint,
    handler);
}


void FDXSocketUDP::SendFdxDatagram(FDXDatagram& datagram)
{
  boost::asio::socket_base::message_flags flags = 0;
  boost::system::error_code errorCode;
  datagram.SetSequenceNumber(mNextTransmitSequenceNumber);
  mSocket.send_to(boost::asio::buffer(datagram.Buffer(), datagram.Size()), mCANoeEndpoint, flags, errorCode);
  if (errorCode)
  {
    std::cerr << "Send over UDP socket failed." << std::endl;
  }
  else
  {
    mNextTransmitSequenceNumber = IncrementSequenceNumber(mNextTransmitSequenceNumber);
  }
}


bool FDXSocketUDP::FinishSequenceCounting()
{
  if (mNextTransmitSequenceNumber == CANoeFDX::kSequenceNumberUnused)
  {
    // The feature sequence counting is already disabled
    return false;
  }
  else if (mNextTransmitSequenceNumber == CANoeFDX::kSequenceNumberSessionStart)
  {
    // The feature sequence counting is enabled, but the first datagram of the sequence was not transmitted yet.
    mNextTransmitSequenceNumber = CANoeFDX::kSequenceNumberUnused;
    return false;
  }
  else
  {
    // Set the session end flag in the next FDX datagram.
    mNextTransmitSequenceNumber = mNextTransmitSequenceNumber | CANoeFDX::kSequenceNumberSessionEndFlag;
    return true;
  }
};


// ---------------------------------------------------------------------------------------------------------------------
// FDXSocketTCP
// ---------------------------------------------------------------------------------------------------------------------


FDXSocketTCP::FDXSocketTCP(boost::asio::io_context& context,
  const boost::asio::ip::tcp::endpoint& localEndpoint,
  const boost::asio::ip::tcp::endpoint& canoeEndpoint)
  : mFDXDispatcher(nullptr)
  , mLocalEndpoint(localEndpoint)
  , mCANoeEndpoint(canoeEndpoint)
  , mSocket(context)
  , mReceiveDatagram()
  , mReceiveState(eReceiveIdle)
{
  // Open socket
  boost::system::error_code opendErrorCode;
  // mSocket.open(boost::asio::ip::tcp::v4(), opendErrorCode);
  mSocket.open(mLocalEndpoint.protocol(), opendErrorCode);
  if (opendErrorCode)
  {
    std::cerr << "Opening TCP socket failed." << std::endl;
    context.stop();
    return;
  }

  // Binding the TCP socket to the local endpoint.
  boost::system::error_code bindErrorCode;
  mSocket.bind(mLocalEndpoint, bindErrorCode);
  if (bindErrorCode)
  {
    std::cerr << "Binding TCP socket failed." << std::endl;
    context.stop();
    return;
  }

  // Connect the TCP socket to CANoe.
  boost::system::error_code connectErrorCode;
  mSocket.connect(mCANoeEndpoint, connectErrorCode);
  if (connectErrorCode)
  {
    std::cerr << "Connecting TCP socket failed." << std::endl;
    context.stop();
    return;
  }

  mReceiveState = eReceiveHeader;
  mReceiveBytesRequired = sizeof(CANoeFDX::DatagramHeader);
  StartReceive();
}


FDXSocketTCP::~FDXSocketTCP()
{
}


void FDXSocketTCP::SetDispatcher(FDXDispatcher* dispatcher)
{
  mFDXDispatcher = dispatcher;
}


void FDXSocketTCP::StartReceive()
{
  size_t remainingSize = mReceiveBytesRequired - mReceiveDatagram.Size();

  auto handler = [this](const boost::system::error_code& errorCode, std::size_t bytesReceived)
  {
    OnReceived(errorCode, bytesReceived);
  };

  mSocket.async_receive(boost::asio::buffer(mReceiveDatagram.RemainingBuffer(), remainingSize), handler);
}


void FDXSocketTCP::OnReceived(const boost::system::error_code& errorCode, std::size_t bytesReceived)
{
  if (errorCode)
  {
    std::cerr << "Receive from TCP socket failed." << std::endl;
  }
  else
  {
    uint32_t totalBytesReceived = mReceiveDatagram.Size() + static_cast<uint32_t>(bytesReceived);
    mReceiveDatagram.Size(totalBytesReceived);

    if (mReceiveBytesRequired != totalBytesReceived)
    {
      StartReceive(); // continue receiving until all bytes are available
    }
    else if (mReceiveState == eReceiveHeader)
    {
      size_t datagramLength = 0;
      bool headerIsValid = false;
      headerIsValid = mFDXDispatcher->CheckhDatagramHeader_TCP(mReceiveDatagram, datagramLength);

      if (headerIsValid)
      {
        // Continue receiving with the fdx commands.
        mReceiveBytesRequired = datagramLength;
        mReceiveState = eReceiveCommands;
        StartReceive();
      }
      else
      {
        mReceiveState = eReceiveError;
      }
    }
    else if (mReceiveState == eReceiveCommands)
    {
      mFDXDispatcher->DispatchCommands(mReceiveDatagram);

      // Clear the receive datagram buffer
      mReceiveDatagram.Size(0);

      // Start Receiving the next datagram
      mReceiveState = eReceiveHeader;
      mReceiveBytesRequired = sizeof(CANoeFDX::DatagramHeader);
      StartReceive();
    }
  }
}


void FDXSocketTCP::SendFdxDatagram(FDXDatagram& datagram)
{
  boost::asio::socket_base::message_flags flags = 0;
  boost::system::error_code ec;

  datagram.SetDatagramLength();

  mSocket.send(boost::asio::buffer(datagram.Buffer(), datagram.Size()), flags, ec);
  if (ec)
  {
    std::cerr << "Send over TCP socket failed." << std::endl;
  }
}


bool FDXSocketTCP::FinishSequenceCounting()
{
  // Sequence counting is used only in case of UDP as transport layer. There is nothing to do in case of TCP.
  return false;
};