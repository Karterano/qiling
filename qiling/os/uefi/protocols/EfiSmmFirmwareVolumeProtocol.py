#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from qiling import Qiling
from qiling.os.const import *
from qiling.os.uefi.const import *
from ..fncc import *
from ..ProcessorBind import *
from ..UefiBaseType import *
from ..PiMultiPhase import *
from .EfiFirmwareVolume2Protocol import EFI_FIRMWARE_VOLUME2_PROTOCOL

class EFI_SMM_FIRMWARE_VOLUME_PROTOCOL(EFI_FIRMWARE_VOLUME2_PROTOCOL):
    pass

descriptor = {
    "guid" : "19e9da84-072b-4274-b32e-0c0802e717a5",
    "struct" : EFI_SMM_FIRMWARE_VOLUME_PROTOCOL,
    "fields" : (
        ("GetVolumeAttributes", EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_GetVolumeAttributes),
        ("SetVolumeAttributes", EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_SetVolumeAttributes),
        ("ReadFile",            EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_ReadFile),
        ("ReadSection",         EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_ReadSection),
        ("WriteFile",           EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_WriteFile),
        ("GetNextFile",         EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_GetNextFile),
        ("GetInfo",             EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_GetInfo),
        ("SetInfo",             EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_SetInfo),
    )
}
