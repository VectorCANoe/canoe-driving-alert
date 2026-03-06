/*--------------------------------------------------------------------------------
Module: BlfDump
Interfaces:
----------------------------------------------------------------------------------
Functions to dump Blf CAN related log objects
----------------------------------------------------------------------------------
Copyright(c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------*/

#pragma once
#include "binlog.h"
#include <string>
#include <sstream>
#include <iomanip>
#include <inttypes.h>

namespace BlfDump {
  // CAN Dump Functions
  bool DumpCANMessage(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase);
  bool DumpCANStatistic(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase);
  bool DumpCANDriverError(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase);
  bool DumpCANSettingsChanged(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase);
  bool DumpCanError(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase);
  bool DumpCANErrorExt(void * hBlfFile, const VBLObjectHeaderBase& canObjectHeaderBase);

  // CAN FD Dump Functions
  bool DumpCANFDMessage64(void * hBlfFile, const VBLObjectHeaderBase& canfdObjectHeaderBase);
  bool DumpCANFDError64(void * hBlfFile, const VBLObjectHeaderBase& canfdObjectHeaderBase);

} //namespace BlfDump