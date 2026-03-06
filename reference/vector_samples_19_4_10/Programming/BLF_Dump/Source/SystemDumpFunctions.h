/*--------------------------------------------------------------------------------
Module: BlfDump
Interfaces:
----------------------------------------------------------------------------------
Functions to dump System related log objects
----------------------------------------------------------------------------------
Copyright(c) Vector Informatik GmbH. All rights reserved.
----------------------------------------------------------------------------------*/

#pragma once
#include "binlog.h"
#include <math.h>
#include <string>
#include <sstream>
#include <iomanip>
#include <inttypes.h>


namespace BlfDump {
  // Dump Functions
  bool DumpSysVar(void * hBlfFile, const VBLObjectHeaderBase& sysVarObjectHeaderBase);
  bool DumpOverrunError(void * hBlfFile, const VBLObjectHeaderBase& objectHeaderBase);
  bool DumpTestStructure(void * hBlfFile, const VBLObjectHeaderBase& objectHeaderBase);

} //namespace BlfDump