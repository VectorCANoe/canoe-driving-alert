//===============================================================================
// Seed & Key DLL with extended interface and options argument
// This is an example implementation for the sample configuration "UDSsim".
// Customize it to your needs!
// Copyright (c) Vector Informatik GmbH. All rights reserved.
//===============================================================================

#define WIN32_LEAN_AND_MEAN
#ifndef STRICT
#define STRICT // enable STRICT type checking
#endif
#include <windows.h>
#include "GenerateKeyExOpt.h"


extern "C" BOOL WINAPI DllMain(
  HINSTANCE const /*instance*/, // handle to DLL module
  DWORD const /*reason*/,       // reason for calling function
  LPVOID const /*reserved*/)    // reserved
{
  return TRUE;  // Successful DLL_PROCESS_ATTACH.
}


KEYGENALGO_API VKeyGenResultExOpt GenerateKeyExOpt(
  const unsigned char* ipSeedArray,  // Array for the seed [in]
  unsigned int iSeedArraySize,       // Length of the array for the seed [in]
  const unsigned int iSecurityLevel, // Security level [in]
  const char* ipVariant,             // Name of the active variant [in]
  const char* ipOptions,             // Optional parameter which might be used for OEM specific information [in]
  unsigned char* iopKeyArray,        // Array for the key [in, out]
  unsigned int iMaxKeyArraySize,     // Maximum length of the array for the key [in]
  unsigned int& oActualKeyArraySize) // Length of the key [out]
{
  // Check the input arguments
  if (iSecurityLevel == 0 || iSecurityLevel > 17)
  {
    return VKeyGenResultExOpt::KGREO_SecurityLevelInvalid;
  }

  if (iMaxKeyArraySize < iSeedArraySize || iSeedArraySize < 2)
  {
    return VKeyGenResultExOpt::KGREO_BufferToSmall;
  }

  if (!ipVariant || ipVariant[0] == '\0')
  {
    return VKeyGenResultExOpt::KGREO_VariantInvalid;
  }

  if (!ipSeedArray || !iopKeyArray || !ipOptions || strlen(ipOptions) < iSeedArraySize)
  {
    return VKeyGenResultExOpt::KGREO_UnspecifiedError;
  }

  // Copy the input bytes to the output bytes
  memcpy(iopKeyArray, ipSeedArray, iSeedArraySize);

  // As an example each byte in the options array will be added to each byte of the seed array securityLevel times.
  for (auto l = 0u; l < iSecurityLevel; ++l)
  {
    for (auto i = 0u; i < iSeedArraySize; ++i)
    {
      iopKeyArray[i] += ipOptions[i];
    }
  }

  oActualKeyArraySize = iSeedArraySize;

  return VKeyGenResultExOpt::KGREO_Ok;
}