#!/usr/bin/env python3
#
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from ..ProcessorBind import *
from ..UefiBaseType import *

# @see: MdePkg\Include\Protocol\DevicePath.h
# TODO Qiling is right, this object is massively more complex than the UEFI spec makes it seem
#  This thing is only the shared header, there will be much more data depending on the type and subtype


class EFI_DEVICE_PATH_PROTOCOL(STRUCT):
    _fields_ = [
        ('Type',    UINT8),
        ('SubType',    UINT8),
        ('Length',    UINT8 * 2)
    ]


def make_descriptor(fields):
    return {
        "guid": "050eb8C6-c12e-4b86-892b-40985e8b3137",
        "struct": EFI_DEVICE_PATH_PROTOCOL,
        "fields": (
            ('Type',        0),
            ('SubType',    0),
            ('Length',        (UINT8 * 2)(0))
        )
    }
