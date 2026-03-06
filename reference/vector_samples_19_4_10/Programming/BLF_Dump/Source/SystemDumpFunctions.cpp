/*--------------------------------------------------------------------------------
Module: BlfDump
Interfaces:
----------------------------------------------------------------------------------
Functions to dump System related log objects
----------------------------------------------------------------------------------
Copyright(c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------*/

#include "SystemDumpFunctions.h"

namespace BlfDump {
  // Forward Declare
  void DumpLoglineHeader(const uint64_t timestamp, const int32_t channel, const std::string& protocol);

  //Private Helper Functions
  std::string FormatSysVarData(void* sysVarDataPtr, const uint32_t sysVarType);

  bool DumpSysVar(void * hBlfFile, const VBLObjectHeaderBase& sysVarObjectHeaderBase)
  {
    VBLSystemVariable sysVariable;
    sysVariable.mHeader.mBase = sysVarObjectHeaderBase;
    if (BLReadObjectSecure(hBlfFile, &sysVariable.mHeader.mBase, sizeof(sysVariable)))
    {
      DumpLoglineHeader(sysVariable.mHeader.mObjectTimeStamp, 0, "");
      printf("SV: %d %s = %s\n",
        sysVariable.mType,                                    //Sysvar Type
        sysVariable.mName,                                    //Sysvar full path
        FormatSysVarData(sysVariable.mData, sysVariable.mType).c_str());    //Sysvar data, basic version (no arrays, etc.)
      BLFreeObject(hBlfFile, &sysVariable.mHeader.mBase);
      return true;
    }
    return false;
  }

  bool DumpOverrunError(void * hBlfFile, const VBLObjectHeaderBase& objectHeaderBase)
  {
    VBLDriverOverrun driverOverrun;
    driverOverrun.mHeader.mBase = objectHeaderBase;

    if (BLReadObjectSecure(hBlfFile, &driverOverrun.mHeader.mBase, sizeof(driverOverrun)))
    {
      DumpLoglineHeader(driverOverrun.mHeader.mObjectTimeStamp, driverOverrun.mChannel, "");
      printf(": Reception overrun - messages are lost\n");  //Overrun Error Indicator
      return true;
    }
    BLFreeObject(hBlfFile, &driverOverrun.mHeader.mBase);
    return false;
  }

  bool DumpTestStructure(void * hBlfFile, const VBLObjectHeaderBase& objectHeaderBase)
  {
    VBLTestStructure testStructure;
    testStructure.mHeader.mBase = objectHeaderBase;
    if (BLReadObjectSecure(hBlfFile, &testStructure.mHeader.mBase, sizeof(testStructure)))
    {
      DumpLoglineHeader(testStructure.mHeader.mObjectTimeStamp, 0, "TFS:");
      printf("%ws\n", testStructure.mText);
      return true;
    }
    BLFreeObject(hBlfFile, &testStructure.mHeader.mBase);
    return false;
  }

  std::string FormatSysVarData(void* sysVarDataPtr, const uint32_t sysVarType)
  {
    double_t doubleData;
    uint32_t longData;
    uint64_t longlongData;
    std::string stringData;

    std::ostringstream formatStream;
    formatStream << std::hex;
    switch (sysVarType)
    {
    case BL_SYSVAR_TYPE_DOUBLE:
      doubleData = *((double_t*)sysVarDataPtr);
      formatStream << std::setprecision(4) << doubleData;
      break;
    case BL_SYSVAR_TYPE_LONG:
      longData = *((uint32_t*)sysVarDataPtr);
      formatStream << longData;
      break;
    case BL_SYSVAR_TYPE_STRING:
      stringData = (static_cast<char*>(sysVarDataPtr));
      if (stringData.empty())
      {
        formatStream << "\"\"";
        break;
      }
      formatStream << stringData;
      break;
    case BL_SYSVAR_TYPE_LONGLONG:
      longlongData = *((uint64_t*)sysVarDataPtr);
      formatStream << longlongData;
      break;
    default:
      formatStream << 0;
      break;
    }
    return formatStream.str();
  }
} // namespace BlfDump