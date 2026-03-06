/*----------------------------------------------------------------------------------------------------------------------
Module: EasyClient
------------------------------------------------------------------------------------------------------------------------
Example of the CANoeFDX interface.
------------------------------------------------------------------------------------------------------------------------
Copyright(c) Vector Informatik GmbH.All rights reserved.
----------------------------------------------------------------------------------------------------------------------*/
#pragma once

#include <stdint.h>

#include "CANoeFDX.h"
#include "FDXDispatcher.h"
#include "FDXSocket.h"



class EasyLogic : public IFDXDispatchCallbacks
{
public:
  EasyLogic(FDXSocket* fdxSocket)
    : mFDXSocket(fdxSocket)
    , mFDXDatagram()
  {}

  virtual void OnFormatError() override;
  virtual void OnSequenceNumberError(CANoeFDX::DatagramHeader* header, uint16_t expectedSeqNr) override;
  virtual void OnStatus(CANoeFDX::DatagramHeader* header, CANoeFDX::StatusCommand* command) override;
  virtual void OnDataError(CANoeFDX::DatagramHeader* header, CANoeFDX::DataErrorCommand* command) override;
  virtual void OnDataExchange(CANoeFDX::DatagramHeader* header, CANoeFDX::DataExchangeCommand* command) override;

  void OnTimer();
  static constexpr int32_t cCycleInterval = 100;   // period for timer [ms]

private:
  FDXSocket* mFDXSocket;
  FDXDatagram mFDXDatagram;

  int32_t mCurrentEngSpeed = 0;
  int32_t mDeltaEngineSpeed = +50;
  int32_t mCounter = 0;

  int32_t mHazardLightsSwitch = false;         // state of the hazard lights switch (on|off)
  int32_t mHazardLightsState = false;          // current state of hazard lights (on|off)
  int32_t gHazardLightsTime = 0;               // time in milliseconds to the next change of mHazardLightsState if
  // the hazard lights switch is turned on.
  const int32_t cHazardLightsFrequency = 500;  // [ms]

  int32_t mHeadLightsState = false;
  uint8_t mCANoeMeasurementState = CANoeFDX::kMeasurementState_NotRunning;
};
