/*--------------------------------------------------------------------------------
Module: BlfDump
Interfaces:
----------------------------------------------------------------------------------
Functions to dump Blf CAN related log objects
----------------------------------------------------------------------------------
Copyright(c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------*/

#include "CANDumpFunctions.h"
#include "SystemDumpFunctions.h"

namespace BlfDump {
  std::string ConvertWeekdayToString(const uint16_t dayOfWeekIndex)
  {
    const static std::string weekDays[7] = { "sun", "mon", "tue", "wed", "thu", "fri", "sat" };
    if (dayOfWeekIndex >= 0 && dayOfWeekIndex < 7)
    {
      return weekDays[dayOfWeekIndex];
    }
    return "";
  }

  std::string ConvertMonthToString(const uint16_t monthIndex)
  {
    const static std::string months[12] = { "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" };
    if (monthIndex >= 1 && monthIndex < 13)
    {
      return months[monthIndex - 1];
    }
    return "";
  }

  int DumpLogHeader(void * hBlfFile)
  {
    VBLFileStatisticsEx logStatistics;
    logStatistics.mStatisticsSize = sizeof(VBLFileStatisticsEx);
    BLGetFileStatisticsEx(hBlfFile, &logStatistics);
    SYSTEMTIME logStartTimestamp = logStatistics.mMeasurementStartTime;

    printf("date %s %s %2d %02d:%02d:%02d.%03d %4d \n",
      ConvertWeekdayToString(logStartTimestamp.wDayOfWeek).c_str(),
      ConvertMonthToString(logStartTimestamp.wMonth).c_str(),
      logStartTimestamp.wDay,
      logStartTimestamp.wHour,
      logStartTimestamp.wMinute,
      logStartTimestamp.wSecond,
      logStartTimestamp.wMilliseconds,
      logStartTimestamp.wYear
    );
    printf("base hex timestamps absolute\n");
    printf("internal events logged\n");
    printf("Canoe version of measurement %2d.%d.%d\n", logStatistics.mApplicationMajor, logStatistics.mApplicationMinor, logStatistics.mApplicationBuild);
    return 0;
  }

  void DumpLoglineHeader(const uint64_t timestamp, const int32_t channel, const std::string& protocol)
  {
    const uint64_t accuracyFactor = 1000;
    const uint64_t timeAccuracy = timestamp / accuracyFactor;
    const uint64_t timeSeconds = timeAccuracy / 1000000;
    const uint64_t timeFraction = timeAccuracy % 1000000;

    const std::string channelString = channel > 0 ? std::to_string(channel) : "";
    printf("%6" PRIu64 ".%06" PRIu64 " %s %-2s", timeSeconds, timeFraction, protocol.c_str(), channelString.c_str());
  }

  void DumpBlfObjects(void* hBlfFile)
  {
    bool bSuccess = true;
    VBLObjectHeaderBase objectHeaderBase;

    while (bSuccess && BLPeekObject(hBlfFile, &objectHeaderBase))
    {
      switch (objectHeaderBase.mObjectType)
      {
      case BL_OBJ_TYPE_CAN_MESSAGE:
      case BL_OBJ_TYPE_CAN_MESSAGE2:
        bSuccess = DumpCANMessage(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_SYS_VARIABLE:
        bSuccess = DumpSysVar(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_CAN_STATISTIC:
        bSuccess = DumpCANStatistic(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_CAN_ERROR:
        bSuccess = DumpCanError(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_CAN_ERROR_EXT:
        bSuccess = DumpCANErrorExt(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_CAN_DRIVER_ERROR:
        bSuccess = DumpCANDriverError(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_CAN_SETTING_CHANGED:
        bSuccess = DumpCANSettingsChanged(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_CAN_FD_MESSAGE_64:
        bSuccess = DumpCANFDMessage64(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_CAN_FD_ERROR_64:
        bSuccess = DumpCANFDError64(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_OVERRUN_ERROR:
        bSuccess = DumpOverrunError(hBlfFile, objectHeaderBase);
        break;
      case BL_OBJ_TYPE_TEST_STRUCTURE:
        bSuccess = DumpTestStructure(hBlfFile, objectHeaderBase);
        break;

        // Cases of Objects that should not be dumped and skipped
      case BL_OBJ_TYPE_APP_TEXT:
      case BL_OBJ_TYPE_reserved_5:
      case BL_OBJ_TYPE_DIAG_REQUEST_INTERPRETATION:
      case BL_OBJ_TYPE_ENV_DOUBLE:
      case BL_OBJ_TYPE_ENV_INTEGER:
      case BL_OBJ_TYPE_ENV_STRING:
      case BL_OBJ_TYPE_ENV_DATA:
        bSuccess = BLSkipObject(hBlfFile, &objectHeaderBase);
        continue;
        // Default case if an unrecognized object is encountered
      default:
        printf("BlfDump: Unhandled type: %d\n", objectHeaderBase.mObjectType);
        bSuccess = BLSkipObject(hBlfFile, &objectHeaderBase);
        break;
      }
    }
  }

  void DumpBlfFile(void * hBlfFile)
  {
    DumpLogHeader(hBlfFile);
    DumpBlfObjects(hBlfFile);
  }
} //namespace BlfDump

int main(int argc, char* argv[])
{
  using namespace BlfDump;
  if (argc != 2)
  {
    printf("Invalid parameters! Please specify a filename.\n");
    printf("Usage:\n %s <blf-file path>\n", argv[0]);
    return -1;
  }
  void * hBlfFile = BLCreateFile(argv[1], GENERIC_READ);

  if (hBlfFile == nullptr)
  {
    fprintf(stderr, "%s: Unable to open file: %s\n", argv[0], argv[1]);
    return -1;
  }
 
  DumpBlfFile(hBlfFile);
  return 0;
}