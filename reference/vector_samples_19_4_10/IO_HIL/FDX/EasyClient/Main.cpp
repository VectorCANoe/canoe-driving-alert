/*----------------------------------------------------------------------------------------------------------------------
Module: EasyClient
------------------------------------------------------------------------------------------------------------------------
Example of the CANoeFDX interface.
------------------------------------------------------------------------------------------------------------------------
Copyright (c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/

#include "CANoeFDX.h"
#include "FDXDatagram.h"
#include "FDXDispatcher.h"
#include "FDXSocket.h"
#include "EasyLogic.h"

#include <iostream>
#include <memory>
#include <cstring>
#include <boost/asio.hpp>
#include <boost/asio/ip/address.hpp>


enum TransportLayer { eUDP, eTCP };


class Application
{
public:
  Application(const boost::asio::ip::udp::endpoint& localEndpoint, const boost::asio::ip::udp::endpoint& canoeEndpoint);
  Application(const boost::asio::ip::tcp::endpoint& localEndpoint, const boost::asio::ip::tcp::endpoint& canoeEndpoint);

  void Run();

private:
  void RegisterBreakHandler();
  void StartTimer();

  boost::asio::io_context        mContext;
  boost::asio::signal_set        mSignals;
  boost::asio::steady_timer      mTimer;

  TransportLayer                 mTransportLayer;
  std::unique_ptr<FDXSocket>     mFDXSocket;
  FDXDispatcher                  mFDXDispatcher;
  EasyLogic                      mApplicationLogic;
};


Application::Application(const boost::asio::ip::udp::endpoint& localEndpoint, const boost::asio::ip::udp::endpoint& canoeEndpoint)
  : mContext()
  , mSignals(mContext, SIGINT)
  , mTimer(mContext)
  , mTransportLayer(eUDP)
  , mFDXSocket(std::make_unique<FDXSocketUDP>(mContext, localEndpoint, canoeEndpoint))
  , mFDXDispatcher()
  , mApplicationLogic(mFDXSocket.get())

{
  mFDXSocket->SetDispatcher(&mFDXDispatcher);
  mFDXDispatcher.SetCallbacks(&mApplicationLogic);
}


Application::Application(const boost::asio::ip::tcp::endpoint& localEndpoint, const boost::asio::ip::tcp::endpoint& canoeEndpoint)
  : mContext()
  , mSignals(mContext, SIGINT)
  , mTimer(mContext)
  , mTransportLayer(eTCP)
  , mFDXSocket(std::make_unique<FDXSocketTCP>(mContext, localEndpoint, canoeEndpoint))
  , mFDXDispatcher()
  , mApplicationLogic(mFDXSocket.get())
{
  mFDXSocket->SetDispatcher(&mFDXDispatcher);
  mFDXDispatcher.SetCallbacks(&mApplicationLogic);
}


void Application::Run()
{
  if (mContext.stopped())
  {
    return;
  }
  RegisterBreakHandler();
  StartTimer();
  mContext.run();
}


void Application::RegisterBreakHandler()
{
  // Control-C Handler that is stopping the event loop of io_context
  auto handler = [this](const boost::system::error_code& /*error*/, int /*signal_number*/)
  {
    std::cout << "CONTROL-C Handler stopping event loop!" << std::endl;

    // In case of UDP as transport layer, send a last datagram to stop sequence counting
    bool needLastDatagram = mFDXSocket->FinishSequenceCounting();
    if (needLastDatagram)
    {
      FDXDatagram datagram;
      datagram.InitWithHeader();
      mFDXSocket->SendFdxDatagram(datagram);
    }

    mContext.stop();
  };


  mSignals.async_wait(handler);
}


void Application::StartTimer()
{
  mTimer.expires_after(std::chrono::milliseconds(EasyLogic::cCycleInterval));

  mTimer.async_wait(
    [this](const boost::system::error_code& ec)
  {
    if (!ec)
    {
      mApplicationLogic.OnTimer();
    }
    StartTimer();
  });
}


// ---------------------------------------------------------------------------------------------------------------------
// Program main function
// ---------------------------------------------------------------------------------------------------------------------


int main(int argc, char* argv[])
{
  // The first program argument specifies the IP address of the host, where the RuntimeKernel of CANoe is running.
  // If no program argument is given, the argument defaults to the IPv6 address '::1', which is the address of the 
  // loopback network interface ('localhost').
  boost::asio::ip::address canoeAddress;
  {
    const char* addr = (argc >= 2) ? argv[1] : "::1";

    boost::system::error_code addressErrorCode;
    canoeAddress = boost::asio::ip::make_address(addr, addressErrorCode);
    if (addressErrorCode)
    {
      std::cerr << "Invalid IP address specified." << std::endl;
      return 1;
    }
  }

  // The second program argument specifies the transport layer, that is used for the FDX communication. It is either 
  // 'upd' or 'tcp'. This argument is optional, the defaults is 'udp'.
  TransportLayer transportLayer;
  {
    const char* layer = (argc >= 3) ? argv[2] : "udp";
    if (std::strcmp(layer, "udp") == 0)
    {
      transportLayer = eUDP;
    }
    else if (std::strcmp(layer, "tcp") == 0)
    {
      transportLayer = eTCP;
    }
    else
    {
      std::cerr << "Invalid transport layer specified. Transport layer must be 'udp' or 'tcp'." << std::endl;
      return 2;
    }
  }

  // The port number, that is used by CANoe for binding the FDX communication port.
  uint16_t canoePort = 2801;

  // The port number, that is used by this FDX client for binding the FDX communication port.
  uint16_t localPort = 2802;


  std::cout << "EasyClient, an example of a CANoe FDX client program." << std::endl;
  if (transportLayer == eUDP && canoeAddress.is_v4())
  {
    std::cout << "Transport Layer: UDP IPv4" << std::endl;
  }
  else if (transportLayer == eUDP && canoeAddress.is_v6())
  {
    std::cout << "Transport Layer: UDP IPv6" << std::endl;
  }
  else if (transportLayer == eTCP && canoeAddress.is_v4())
  {
    std::cout << "Transport Layer: TCP IPv4" << std::endl;
  }
  else if (transportLayer == eTCP && canoeAddress.is_v6())
  {
    std::cout << "Transport Layer: TCP IPv6" << std::endl;
  }
  std::cout << "CANoe Endpoint: " << canoeAddress.to_string() << " , " << std::dec << canoePort << std::endl;


  std::unique_ptr<Application> app;
  if (transportLayer == eUDP)
  {
    boost::asio::ip::udp::endpoint canoeEndpoint{ canoeAddress, canoePort };
    boost::asio::ip::udp::endpoint localEndpoint{ canoeEndpoint.protocol(), localPort };
    app = std::make_unique<Application>(localEndpoint, canoeEndpoint);
  }
  else if (transportLayer == eTCP)
  {
    boost::asio::ip::tcp::endpoint canoeEndpoint{ canoeAddress, canoePort };
    boost::asio::ip::tcp::endpoint localEndpoint{ canoeEndpoint.protocol(), localPort };
    app = std::make_unique<Application>(localEndpoint, canoeEndpoint);
  }

  app->Run();

  return 0;
}
