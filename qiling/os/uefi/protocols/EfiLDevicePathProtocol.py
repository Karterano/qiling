#!/usr/bin/env python3
#
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from ..ProcessorBind import *
from ..UefiBaseType import *

# @see: MdePkg\Include\Protocol\DevicePath.h
# TODO Qiling is right, this object is massively more complex than the UEFI spec makes it seem
#  This thing is only the shared header, there will be much more data depending on the type and subtype


EFI_DEVICE_PATH_PROTOCOL_GUID = "09576e91-6d3f-11d2-8e39-00a0c969723b"

class EFI_DEVICE_PATH_PROTOCOL(STRUCT):
    _fields_ = [
        ('Type',    UINT8),
        ('SubType',    UINT8),
        ('Length',    UINT8 * 2)
    ]


descriptor = {
        "guid": EFI_DEVICE_PATH_PROTOCOL_GUID,
        "struct": EFI_DEVICE_PATH_PROTOCOL,
        "fields": (
            ('Type',        0),
            ('SubType',    0),
            ('Length',        (UINT8 * 2)(0))
        )
    }
