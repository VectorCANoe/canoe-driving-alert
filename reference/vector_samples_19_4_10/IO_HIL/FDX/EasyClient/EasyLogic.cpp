/*-----------------------------------------------------------------------------
Module: EasyClient
------------------------------------------------------------------------------------------------------------------------
Example of the CANoeFDX interface.
------------------------------------------------------------------------------------------------------------------------
Copyright(c) Vector Informatik GmbH.All rights reserved.
--------------------------------------------------------------------------------------------------------------------- */

#include "EasyLogic.h"

#include <iostream>



struct EasyDataRead
{
  static const uint16_t cGroupID = 1;
  static const uint16_t cSize = 8;

  int16_t  SigEngineSpeed;          // offset 0
  uint8_t  SigOnOff;                // offset 2
  uint8_t  SigFlashLight;           // offset 3
  uint8_t  SigHeadLight;            // offset 4
  uint8_t  VarHazardLightsSwitch;   // offset 5
  uint8_t  VarHeadLightSwitch;      // offset 6
  uint8_t  Reserved1;               // offset 7
};

// Check the memory layout of struct EasyDataRead
static_assert(EasyDataRead::cSize == sizeof(EasyDataRead), "Invalid size of struct EasyDataRead");
static_assert(0 == offsetof(EasyDataRead, SigEngineSpeed), "Invalid offset of EasyDataRead::SigEngineSpeed");
static_assert(2 == offsetof(EasyDataRead, SigOnOff), "Invalid offset of EasyDataRead::SigOnOff");
static_assert(3 == offsetof(EasyDataRead, SigFlashLight), "Invalid offset of EasyDataRead::SigFlashLight");
static_assert(4 == offsetof(EasyDataRead, SigHeadLight), "Invalid offset of EasyDataRead::SigHeadLight");
static_assert(5 == offsetof(EasyDataRead, VarHazardLightsSwitch), "Invalid offset of EasyDataRead::VarHazardLightsSwitch");
static_assert(6 == offsetof(EasyDataRead, VarHeadLightSwitch), "Invalid offset of EasyDataRead::VarHeadLightSwitch");



struct EasyDataWrite
{
  static const uint16_t cGroupID = 2;
  static const uint16_t cSize = 8;

  int16_t  VarEngineSpeedEntry;    // offset 0
  uint8_t  VarEngineStateSwitch;   // offset 2
  uint8_t  SigFlashLigth;          // offset 3
  uint8_t  SigHeadLight;           // offset 4
  uint8_t  Reserved1;              // offset 5
  uint8_t  Reserved2;              // offset 6
  uint8_t  Reserved3;              // offset 7
};

// Check the memory layout of struct EasyDataWrite
static_assert(EasyDataWrite::cSize == sizeof(EasyDataWrite), "Invalid size of struct EasyDataWrite");
static_assert(0 == offsetof(EasyDataWrite, VarEngineSpeedEntry), "Invalid offset of EasyDataWrite::VarEngineSpeedEntry");
static_assert(2 == offsetof(EasyDataWrite, VarEngineStateSwitch), "Invalid offset of EasyDataWrite::VarEngineStateSwitch");
static_assert(3 == offsetof(EasyDataWrite, SigFlashLigth), "Invalid offset of EasyDataWrite::SigFlashLight");
static_assert(4 == offsetof(EasyDataWrite, SigHeadLight), "Invalid offset of EasyDataWrite::SigHeadLight");



struct EasyFrameAccess
{
  static const uint16_t cGroupID = 3;
  static const uint16_t cSize = 16;

  uint32_t EngineState_byteArraySize;
  struct EngineStateFrame
  {
    static const uint16_t cSize = 2;

    uint16_t OnOff : 1;
    int16_t  EngineSpeed : 15;
  } engineState;

  // automatic padding to 4 byte boundary
  uint32_t LightState_byteArraySize;
  struct LightStateFrame
  {
    static const uint16_t cSize = 1;

    uint8_t  HeadLight : 1;
    uint8_t  _no_data_1 : 1;
    uint8_t  FlashLight : 1;
    uint8_t  _no_data_2 : 5;
  } lightState;
};

// Check the memory layout of struct EasyFrameAccess
static_assert(EasyFrameAccess::cSize == sizeof(EasyFrameAccess), "Invalid size of struct EasyFrameAccess");
static_assert(EasyFrameAccess::EngineStateFrame::cSize == sizeof(EasyFrameAccess::EngineStateFrame), "Invalid size of struct EngineStateFrame");
static_assert(EasyFrameAccess::LightStateFrame::cSize == sizeof(EasyFrameAccess::LightStateFrame), "Invalid size of struct LightStateFrame");
static_assert(0 == offsetof(EasyFrameAccess, EngineState_byteArraySize), "Invalid offset of EasyFrameAccess::EngineState_byteArraySize");
static_assert(4 == offsetof(EasyFrameAccess, engineState), "Invalid offset of EasyFrameAccess::engineState");
static_assert(8 == offsetof(EasyFrameAccess, LightState_byteArraySize), "Invalid offset of EasyFrameAccess::LightState_byteArraySize");
static_assert(12 == offsetof(EasyFrameAccess, lightState), "Invalid offset of EasyFrameAccess::lightState");



void EasyLogic::OnFormatError()
{
  printf("Format Error\n");
}

void EasyLogic::OnSequenceNumberError(CANoeFDX::DatagramHeader* header, uint16_t expectedSeqNr)
{
  printf("Sequence Number Error\n");
}

void EasyLogic::OnStatus(CANoeFDX::DatagramHeader* header, CANoeFDX::StatusCommand* command)
{
  if (command->measurementState == CANoeFDX::kMeasurementState_NotRunning)
  {
    printf("CANoe measurement is not running\n");
  }
  mCANoeMeasurementState = command->measurementState;
}

void EasyLogic::OnDataError(CANoeFDX::DatagramHeader* header, CANoeFDX::DataErrorCommand* command)
{
  if (command->dataErrorCode != CANoeFDX::kDataErrorCode_MeasurementNotRunning)
  {
    printf("Data error for group ID %d, error code %d\n", command->groupID, command->dataErrorCode);
  }
}

void EasyLogic::OnDataExchange(CANoeFDX::DatagramHeader* header, CANoeFDX::DataExchangeCommand* command)
{
  if (command->groupID == EasyDataRead::cGroupID)
  {
    EasyDataRead* readData = reinterpret_cast<EasyDataRead*>(command->dataBytes);
    std::cout << "Variables Read:" << std::endl;
    std::cout << "EngineSpeed = " << readData->SigEngineSpeed << " "
      << "HeadLight = " << ((readData->SigHeadLight) ? "on" : "off") << " "
      << "FlashLight = " << ((readData->SigFlashLight) ? "on" : "off") << std::endl;

    if (mHazardLightsSwitch == 0 && readData->VarHazardLightsSwitch == 1)
    {
      // activate hazard lights
      mHazardLightsSwitch = 1;
      mHazardLightsState = 1;
      gHazardLightsTime = cHazardLightsFrequency;
    }
    else if (mHazardLightsSwitch == 1 && readData->VarHazardLightsSwitch == 0)
    {
      // deactivate hazard lights
      mHazardLightsSwitch = 0;
      mHazardLightsState = 0;
      gHazardLightsTime = 0;
    }

    mHeadLightsState = readData->VarHeadLightSwitch;
  }
  else if (command->groupID == EasyFrameAccess::cGroupID)
  {
    EasyFrameAccess* readData = reinterpret_cast<EasyFrameAccess*>(command->dataBytes);
    std::cout << "Frames Read:" << "EngineOnOff = " << (readData->engineState.OnOff ? "on" : "off") << std::endl;
    std::cout << "EngineSpeed = " << readData->engineState.EngineSpeed << " "
      << "HeadLight = " << (readData->lightState.HeadLight ? "on" : "off") << " "
      << "FlashLight = " << (readData->lightState.FlashLight ? "on" : "off") << std::endl;
  }
}

void EasyLogic::OnTimer()
{
  // change engine speed
  if (mCANoeMeasurementState == CANoeFDX::kMeasurementState_Running)
  {
    if (mCurrentEngSpeed >= 3000)
    {
      mDeltaEngineSpeed = -50;
    }
    else if (mCurrentEngSpeed <= 0)
    {
      mDeltaEngineSpeed = +50;
    }
    mCurrentEngSpeed += mDeltaEngineSpeed;
  }
  else
  {
    mCurrentEngSpeed = 0;
    mDeltaEngineSpeed = +50;
  }


  // toggle hazard lights
  if (mHazardLightsSwitch == 1)
  {
    gHazardLightsTime -= cCycleInterval;
    if (gHazardLightsTime <= 0)
    {
      mHazardLightsState = 1 - mHazardLightsState;  // toggle state
      gHazardLightsTime = cHazardLightsFrequency;
    }
  }


  mCounter++;
  if (mCounter % 2 == 0)
  {
    // build datagram using individual signal and variable access
    mFDXDatagram.InitWithHeader();
    mFDXDatagram.AddDataRequest(EasyDataRead::cGroupID);
    void* dataBytes;
    dataBytes = mFDXDatagram.AddDataExchange(EasyDataWrite::cGroupID, EasyDataWrite::cSize);
    EasyDataWrite* writeData = reinterpret_cast<EasyDataWrite*>(dataBytes);
    writeData->VarEngineSpeedEntry = mCurrentEngSpeed;
    writeData->VarEngineStateSwitch = (mCANoeMeasurementState == CANoeFDX::kMeasurementState_Running) ? 1 : 0;
    writeData->SigFlashLigth = mHazardLightsState;
    writeData->SigHeadLight = mHeadLightsState;
  }
  else
  {
    // build datagram using full frame access (byte array)
    mFDXDatagram.InitWithHeader();
    mFDXDatagram.AddDataRequest(EasyDataRead::cGroupID);
    mFDXDatagram.AddDataRequest(EasyFrameAccess::cGroupID);
    void* dataBytes;
    dataBytes = mFDXDatagram.AddDataExchange(EasyFrameAccess::cGroupID, EasyFrameAccess::cSize);
    EasyFrameAccess* writeData = reinterpret_cast<EasyFrameAccess*>(dataBytes);

    writeData->EngineState_byteArraySize = EasyFrameAccess::EngineStateFrame::cSize;
    writeData->engineState.OnOff = 1;
    writeData->engineState.EngineSpeed = mCurrentEngSpeed;

    writeData->LightState_byteArraySize = EasyFrameAccess::LightStateFrame::cSize;
    writeData->lightState.HeadLight = mHeadLightsState;
    writeData->lightState.FlashLight = mHazardLightsState;
  }

  mFDXSocket->SendFdxDatagram(mFDXDatagram);
}

