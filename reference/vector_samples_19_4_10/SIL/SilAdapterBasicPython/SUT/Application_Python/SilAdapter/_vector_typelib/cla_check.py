#
# Copyright (c) Vector Informatik GmbH. All rights reserved.
#
# This code was generated automatically. Changes to this file may
# cause incorrect behavior and will be lost if the code is regenerated.

canoe_cla_installed = True

try:
    import vector.canoe
except ModuleNotFoundError:
    canoe_cla_installed = False

if canoe_cla_installed is True:
    raise RuntimeError("The SIL Adapter cannot be used within CANoe. Please use the SIL Adapter in a script outside of CANoe.")

try:
    import canoe_sil_adapter_runtime.cla
except ModuleNotFoundError:
    raise ModuleNotFoundError("The canoe-sil-adapter-runtime package is missing. Install it with <CANoe/CANoe4SW install folder>/Installer Additional Components/SilAdapter/Python Runtime/install_runtime.py.")

SAB_CLA = "SabCla"
CANOE_CLA = "CANoeCla"
REQUIRED_CLA_VERSION = "6.1.2"


def check_version():
    required_version = REQUIRED_CLA_VERSION.split('.')
    required_major = int(required_version[0])
    required_minor = int(required_version[1])
    required_patch = int(required_version[2])
    implementation_version = canoe_sil_adapter_runtime.cla.GetImplementationVersion()
    if(implementation_version.major != required_major or (required_minor, required_patch) > (implementation_version.minor, implementation_version.patch)):
        raise VersionException(str(implementation_version.major) + '.' + str(implementation_version.minor) + '.' + str(implementation_version.patch))


class VersionException(Exception):
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return 'The canoe-sil-adapter-runtime package version is incompatible: {0} suited {1}. Please update the canoe-sil-adapter-runtime package and regenerate the SIL Adapter.'.format(self.message, REQUIRED_CLA_VERSION)
