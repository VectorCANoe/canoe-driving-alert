/*--------------------------------------------------------------------------------
Module: BlfDump
Interfaces:
----------------------------------------------------------------------------------
Functions to dump Blf CAN related log objects
----------------------------------------------------------------------------------
Copyright(c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------*/

#include "CANDumpFunctions.h"

namespace BlfDump {
  // Forward Declare
  void DumpLoglineHeader(const uint64_t timestamp, const int32_t channel, const std::string& protocol);

  // Private Helper Functions
  std::string FormatCANData(const uint8_t data[], const uint8_t dlc);
  std::string FormatCANErrorCount(const uint8_t rxErrorCount, const uint8_t txErrorCount);
  std::string CANDirectionToString(const int32_t dir);

  bool DumpCANMessage(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase)
  {
    VBLCANMessage2 canMessage2;
    canMessage2.mHeader.mBase = canObjectHeaderBase;

    if (BLReadObjectSecure(hBlfFile, &canMessage2.mHeader.mBase, sizeof(canMessage2)))
    {
      DumpLoglineHeader(canMessage2.mHeader.mObjectTimeStamp, canMessage2.mChannel, "CAN");
      printf("%-4s %s %x %s Length = %d BitCount = %d ID = %u\n",
        CANDirectionToString(canMessage2.mFlags).c_str(),   //Message direction (Rx/Tx)
        CAN_MSG_RTR(canMessage2.mFlags) ? "r" : "d",        //Remote/Standard Frame indicator
        canMessage2.mDLC,                                   //DLC (in hexadecimal)
        CAN_MSG_RTR(canMessage2.mFlags) ? "" : FormatCANData(canMessage2.mData, canMessage2.mDLC).c_str(), //Message Data (only dumped if the frame is standard)
        canMessage2.mFrameLength,                           //Frame duration in ns
        canMessage2.mBitCount,                              //Bitcount
        (canMessage2.mID & 0x7FFFFFFFU)                     //Message ID (in hexadecimal)
      );      
      BLFreeObject(hBlfFile, &canMessage2.mHeader.mBase);
      return true;
    }
    return false;
  }

  bool DumpCANFDMessage64(void * hBlfFile, const VBLObjectHeaderBase& canfdObjectHeaderBase)
  {
    VBLCANFDMessage64 canfdMessage64;
    canfdMessage64.mHeader.mBase = canfdObjectHeaderBase;
    if (BLReadObjectSecure(hBlfFile, &canfdMessage64.mHeader.mBase, sizeof(canfdMessage64)))
    {
      DumpLoglineHeader(canfdMessage64.mHeader.mObjectTimeStamp, canfdMessage64.mChannel, "CANFD");
      printf("%-4s %-8x %d %d %x %2d %s %8d %3d %8x %8x %8x %8x %8x %8x\n",
        CANDirectionToString(canfdMessage64.mDir).c_str(),  //Message direction (Rx/Tx)
        (canfdMessage64.mID),                               //Message ID (in hexadecimal)
        CAN_FD_MSG_BRS(canfdMessage64.mFlags >> 12),        //BRS flag (1 or 0)
        CAN_FD_MSG_ESI(canfdMessage64.mFlags >> 12),        //ESI flag (1 or 0)
        canfdMessage64.mDLC,                                //DLC (in hexadecimal)
        canfdMessage64.mValidDataBytes,                     //Payload length (in decimal, value range 0-64)
        FormatCANData(canfdMessage64.mData, canfdMessage64.mValidDataBytes).c_str(), //CANfd Frame Data
        canfdMessage64.mFrameLength,                        //Frame duration in ns
        canfdMessage64.mBitCount,                           //Bitcount
        canfdMessage64.mFlags,                              //Flags
        canfdMessage64.mCRC,                                //CRC field
        canfdMessage64.mBtrCfgArb,                          //Arbitration phase bit rate (in hexadecimal)
        canfdMessage64.mBtrCfgData,                         //Data phase bit rate (in hexadecimal)
        BLExtFrameDataPtr(&canfdMessage64)->mBTRExtArb,     //Extended bit timing arbitration phase (in hexadecimal)
        BLExtFrameDataPtr(&canfdMessage64)->mBTRExtData     //Extended bit timing data phase (in hexadecimal)                        
      );          

      BLFreeObject(hBlfFile, &canfdMessage64.mHeader.mBase);
      return true;
    }
    return false;
  }

  bool DumpCanError(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase)
  {
    VBLCANErrorFrame canError;
    canError.mHeader.mBase = canObjectHeaderBase;

    if (BLReadObjectSecure(hBlfFile, &canError.mHeader.mBase, sizeof(canError)))
    {
      DumpLoglineHeader(canError.mHeader.mObjectTimeStamp, canError.mChannel, "CAN");
      printf("Error Frame\n");                              // Error Frame indicator
      BLFreeObject(hBlfFile, &canError.mHeader.mBase);
      return true;
    }
    return false;
  }

  bool DumpCANErrorExt(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase)
  {
    VBLCANErrorFrameExt canErrorExt;
    canErrorExt.mHeader.mBase = canObjectHeaderBase;

    if (BLReadObjectSecure(hBlfFile, &canErrorExt.mHeader.mBase, sizeof(canErrorExt)))
    {
      DumpLoglineHeader(canErrorExt.mHeader.mObjectTimeStamp, canErrorExt.mChannel, "CAN");
      printf("ErrorFrame Flags = 0x%x CodeExt = 0x%x Code = 0x%x ID = 0x%x DLC = %u Position = %u Length = %u %s\n",
        canErrorExt.mFlags,                                 //Flags
        canErrorExt.mFlagsExt,                              //Extended Flags
        canErrorExt.mECC,                                   //Error Control Code
        canErrorExt.mID,                                    //Frame ID
        canErrorExt.mDLC,                                   //DLC (in hexadecimal)
        canErrorExt.mPosition,                              //Error Position
        canErrorExt.mFrameLengthInNS,                       //Frame duration in ns
        canErrorExt.mDLC ? ("Data = " + FormatCANData(canErrorExt.mData, canErrorExt.mDLC)).c_str() : "" // Error Data (only dumped if DLC > 0)
      );
      BLFreeObject(hBlfFile, &canErrorExt.mHeader.mBase);
      return true;
    }
    return false;
  }

  bool DumpCANFDError64(void * hBlfFile, const VBLObjectHeaderBase& canfdObjectHeaderBase)
  {
    VBLCANFDErrorFrame64 canfdError64;
    canfdError64.mHeader.mBase = canfdObjectHeaderBase;

    if (BLReadObjectSecure(hBlfFile, &canfdError64.mHeader.mBase, sizeof(canfdError64)))
    {
      uint16_t errorCodeExt = canfdError64.mErrorCodeExt;

      DumpLoglineHeader(canfdError64.mHeader.mObjectTimeStamp, canfdError64.mChannel, "CANFD");
      printf("%-4s ErrorCode: 0x%x %2x %4x %8x %s %2d %8x %d %d %x %2d %s %8d %8x %8x %8x %8x %8x %8x\n",
        CANDirectionToString((errorCodeExt & 32) ? 0 : 1).c_str(), //Message direction (Rx/Tx)
        canfdError64.mErrorCodeExt,                         //Error Code
        canfdError64.mFlags,                                //Flags
        canfdError64.mECC,                                  //Error Code      
        canfdError64.mErrorCodeExt,                         //Extended Error Code
        (canfdError64.mExtFlags & 8) ? "Data" : "Arb.",     //Error phase
        canfdError64.mErrorPosition,                        //Error position
        (canfdError64.mID),                                 //Frame ID
        CAN_FD_MSG_BRS(canfdError64.mExtFlags),             //BRS flag (1 or 0)
        CAN_FD_MSG_ESI(canfdError64.mExtFlags),             //ESI flag (1 or 0)
        canfdError64.mDLC,                                  //DLC (in hexadecimal)
        canfdError64.mValidDataBytes,                       //Payload length (in decimal, value range 0-64)
        FormatCANData(canfdError64.mData, canfdError64.mValidDataBytes).c_str(),   //CANfd Frame Data
        canfdError64.mFrameLength,                          //Frame duration in ns
        canfdError64.mExtFlags,                             //Flags
        canfdError64.mCRC,                                  //CRC field        
        canfdError64.mBtrCfgArb,                            //Arbitration phase bit rate (in hexadecimal)
        canfdError64.mBtrCfgData,                           //Data phase bit rate (in hexadecimal)
        BLExtFrameDataPtr(&canfdError64)->mBTRExtArb,       //Extended bit timing arbitration phase (in hexadecimal)
        BLExtFrameDataPtr(&canfdError64)->mBTRExtData       //Extended bit timing data phase (in hexadecimal)                
      );

      BLFreeObject(hBlfFile, &canfdError64.mHeader.mBase);
      return true;
    }
    return false;
  }

  bool DumpCANStatistic(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase)
  {
    VBLCANDriverStatistic canDriverStat;
    canDriverStat.mHeader.mBase = canObjectHeaderBase;
    if (BLReadObjectSecure(hBlfFile, &canDriverStat.mHeader.mBase, sizeof(canDriverStat)))
    {
      DumpLoglineHeader(canDriverStat.mHeader.mObjectTimeStamp, canDriverStat.mChannel, "CAN");
      short busLoad = canDriverStat.mBusLoad;
      if (busLoad == (-32768)) busLoad = 0;
	    printf("Statistic: D %u R %u XD %u XR %u E %u O %u B %u.%02d%%\n",
        canDriverStat.mStandardDataFrames,                  //Amount of standard data frames
        canDriverStat.mStandardRemoteFrames,                //Amount of standard remote frames
        canDriverStat.mExtendedDataFrames,                  //Amount of extended data frames
        canDriverStat.mExtendedRemoteFrames,                //Amount of extended remote frames
        canDriverStat.mErrorFrames,                         //Amount of error frames
        canDriverStat.mOverloadFrames,                      //Amount of overload frames
        busLoad / 100,                                      //Bus load (pre-decimal places)
        busLoad % 100                                       //Bus load (decimal places)
      );
      BLFreeObject(hBlfFile, &canDriverStat.mHeader.mBase);
      return true;
    }
    return false;
  }


  bool DumpCANSettingsChanged(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase)
  {
    VBLCANSettingsChanged canSettingsChanged;
    canSettingsChanged.mHeader.mBase = canObjectHeaderBase;
    if (BLReadObjectSecure(hBlfFile, &canSettingsChanged.mHeader.mBase, sizeof(canSettingsChanged)))
    {
      DumpLoglineHeader(canSettingsChanged.mHeader.mObjectTimeStamp, canSettingsChanged.mChannel, "CAN");
      if (!canSettingsChanged.mChangedType)
      {
        printf("CAN reseted");                              //CAN Reset indicator
      }
      else
      {
        printf("BitTimingChanged ArbSettings : %x DataSettings %x",
          canSettingsChanged.mBitTimings.mBTRExtArb,        //Extended bit timing arbitration phase (in hexadecimal)        
          canSettingsChanged.mBitTimings.mBTRExtData        //Extended bit timing data phase (in hexadecimal)  
        );
      }
      printf("\n");
      
      BLFreeObject(hBlfFile, &canSettingsChanged.mHeader.mBase);
      return true;
    }
    return false;
  }

  bool DumpCANDriverError(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase)
  {
    VBLCANDriverError canDriverError;
    canDriverError.mHeader.mBase = canObjectHeaderBase;
    if (BLReadObjectSecure(hBlfFile, &canDriverError.mHeader.mBase, sizeof(canDriverError)))
    {
      DumpLoglineHeader(canDriverError.mHeader.mObjectTimeStamp, canDriverError.mChannel, "CAN");
      printf("ErrorCode: 0x%x ErrorCount: %s\n",
        canDriverError.mErrorCode,                                                        //Error Code
        FormatCANErrorCount(canDriverError.mRXErrors, canDriverError.mTXErrors).c_str()   //Error Counts
      );
      BLFreeObject(hBlfFile, &canDriverError.mHeader.mBase);
      return true;
    }
    return false;
  }

  std::string FormatCANData(const uint8_t data[], const uint8_t dlc)
  {
    std::stringstream formattedData;
    for (int i = 0; i < dlc; i++)
    {
      formattedData << std::hex << std::setw(2) << std::setfill('0') << (int)data[i];
      formattedData << " ";
    }
    return formattedData.str();
  }

  std::string FormatCANErrorCount(const uint8_t rxErrorCount, const uint8_t txErrorCount)
  {
    if (rxErrorCount != 0 || txErrorCount != 0)
    {
      return std::string("TxErr: " + std::to_string(txErrorCount) + " RxErr: " + std::to_string(rxErrorCount));
    }
    return "";
  }

  std::string CANDirectionToString(const int32_t canFlags)
  {
    if (CAN_MSG_DIR(canFlags))
    {
      return "Tx  ";
    }
    else
    {
      return "Rx  ";
    }
  }
} //namespace BlfDump