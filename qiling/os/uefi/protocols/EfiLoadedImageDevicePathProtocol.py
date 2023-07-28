#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from ..ProcessorBind import *
from ..UefiBaseType import *
from ..UefiSpec import EFI_DEVICE_PATH_PROTOCOL
from ..UefiMultiPhase import EFI_MEMORY_TYPE

# @see: MdePkg\Include\Protocol\LoadedImage.h

class EFI_LOADED_IMAGE_DEVICE_PATH_PROTOCOL(EFI_DEVICE_PATH_PROTOCOL):
    pass

def make_descriptor(fields):
    return {
        "guid" : "bc62157e-3e33-4fec-9920-2d3b36d750df",
        "struct" : EFI_LOADED_IMAGE_DEVICE_PATH_PROTOCOL,
        "fields" : (
            ('Type',        0),
            ('SubType',    0),
            ('Length',        (UINT8 * 2)(0))
        )
    }
