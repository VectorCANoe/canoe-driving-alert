//===============================================================================
// Seed & Key DLL without options argument
// This is an example implementation for the sample configuration "UDSsim".
// Customize it to your needs!
// Copyright (c) Vector Informatik GmbH. All rights reserved.
//===============================================================================

#define WIN32_LEAN_AND_MEAN
#ifndef STRICT
#define STRICT // enable STRICT type checking
#endif
#include <windows.h>
#include "GenerateKeyEx.h"


extern "C" BOOL WINAPI DllMain(
  HINSTANCE const /*instance*/, // handle to DLL module
  DWORD const /*reason*/,       // reason for calling function
  LPVOID const /*reserved*/)    // reserved
{
  return TRUE;  // Successful DLL_PROCESS_ATTACH.
}


KEYGENALGO_API VKeyGenResultEx GenerateKeyEx(
  const unsigned char* ipSeedArray,  // Array for the seed [in]
  unsigned int iSeedArraySize,       // Length of the array for the seed [in]
  const unsigned int iSecurityLevel, // Security level [in]
  const char* ipVariant,             // Name of the active variant [in]
  unsigned char* iopKeyArray,        // Array for the key [in, out]
  unsigned int iMaxKeyArraySize,     // Maximum length of the array for the key [in]
  unsigned int& oActualKeyArraySize) // Length of the key [out]
{
  // Check the input arguments
  if (iSecurityLevel == 0 || iSecurityLevel > 17)
  {
    return VKeyGenResultEx::KGRE_SecurityLevelInvalid;
  }

  if (iMaxKeyArraySize < iSeedArraySize || iSeedArraySize < 2)
  {
    return VKeyGenResultEx::KGRE_BufferToSmall;
  }

  if (!ipVariant || ipVariant[0] == '\0')
  {
    return VKeyGenResultEx::KGRE_VariantInvalid;
  }

  if (!ipSeedArray || !iopKeyArray)
  {
    return VKeyGenResultEx::KGRE_UnspecifiedError;
  }

  // As an example each byte in the seed array will XOR-ed stored in key.
  for (auto i = 0u; i < iSeedArraySize; i++)
  {
    iopKeyArray[i] = ~ipSeedArray[i];
  }

  oActualKeyArraySize = iSeedArraySize;

  return VKeyGenResultEx::KGRE_Ok;
}