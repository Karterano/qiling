#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from ..ProcessorBind import *
from ..UefiBaseType import *
from ..UefiSpec import EFI_IMAGE_UNLOAD
from ..st import EFI_SYSTEM_TABLE
from ..UefiMultiPhase import EFI_MEMORY_TYPE
from .EfiLDevicePathProtocol import EFI_DEVICE_PATH_PROTOCOL

# @see: MdePkg\Include\Protocol\LoadedImage.h
class EFI_LOADED_IMAGE_PROTOCOL(STRUCT):
    _pack_ = 8

    _fields_ = [
        ('Revision',        UINT32),
        ('ParentHandle',    EFI_HANDLE),
        ('SystemTable',        PTR(EFI_SYSTEM_TABLE)),
        ('DeviceHandle',    EFI_HANDLE),
        ('FilePath',        PTR(EFI_DEVICE_PATH_PROTOCOL)),
        ('Reserved',         PTR(VOID)),
        ('LoadOptionsSize',    UINT32),
        ('LoadOptions',        PTR(VOID)),
        ('ImageBase',        PTR(VOID)),
        ('ImageSize',        UINT64),
        ('ImageCodeType',    EFI_MEMORY_TYPE),
        ('ImageDataType',    EFI_MEMORY_TYPE),
        ('Unload',            EFI_IMAGE_UNLOAD)
    ]

def make_descriptor(fields):
    descriptor = {
        "guid" : "5b1b31a1-9562-11d2-8e3f-00a0c969723b",
        "struct" : EFI_LOADED_IMAGE_PROTOCOL,
        "fields" : (
            ('Revision',        0x1000),
            ('ParentHandle',    0),
            ('SystemTable',        fields['gST']),
            ('DeviceHandle',    fields['device_handle']),
            ('FilePath',        fields['file_path']),        # This is a handle to a complex path object, skip it for now.
            ('LoadOptionsSize',    0),
            ('LoadOptions',        0),
            ('ImageBase',        fields['image_base']),
            ('ImageSize',        fields['image_size']),
            ('ImageCodeType',    EFI_MEMORY_TYPE.EfiLoaderCode),
            ('ImageDataType',    EFI_MEMORY_TYPE.EfiLoaderData),
            ('Unload',            0)
        )
    }

    return descriptor

# __all__ = [
#     'EFI_LOADED_IMAGE_PROTOCOL',
#     'make_descriptor'
# ]