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

from qiling.os.uefi.UefiInternalFormRepresentation import *

from .EfiGraphicsOutputProtocol import EFI_GRAPHICS_OUTPUT_BLT_PIXEL, EFI_GRAPHICS_OUTPUT_PROTOCOL

class EFI_IMAGE_INPUT(STRUCT):
    _fields_ = [
        ('Flags',   UINT32),
        ('Width',   UINT16),
        ('Height',  UINT16),
        ('Bitmap',  PTR(EFI_GRAPHICS_OUTPUT_BLT_PIXEL))
    ]

EFI_HII_DRAW_FLAGS = UINT32

# FIXME not sure if this is the right way to define a c type union
class Image(UNION):
    _fields_ = [
        ('Bitmap',  PTR(EFI_GRAPHICS_OUTPUT_BLT_PIXEL)),
        ('Screen',  PTR(EFI_GRAPHICS_OUTPUT_PROTOCOL))
    ]

class EFI_IMAGE_OUTPUT(STRUCT):
    _fields_ = [
        ('Width',   UINT16),
        ('Height',  UINT16),
        ('Image',  Image)
    ]



# @see: MdePkg\Include\Protocol\HiiImage.h
class EFI_HII_IMAGE_PROTOCOL(STRUCT):
    EFI_HII_IMAGE_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('NewImage',    FUNCPTR(EFI_STATUS, PTR(EFI_HII_IMAGE_PROTOCOL), EFI_HII_HANDLE, PTR(EFI_IMAGE_ID), PTR(EFI_IMAGE_INPUT))),
        ('GetImage',    FUNCPTR(EFI_STATUS, PTR(EFI_HII_IMAGE_PROTOCOL), EFI_HII_HANDLE, EFI_IMAGE_ID, PTR(EFI_IMAGE_INPUT))),
        ('SetImage',    FUNCPTR(EFI_STATUS, PTR(EFI_HII_IMAGE_PROTOCOL), EFI_HII_HANDLE, EFI_IMAGE_ID, PTR(EFI_IMAGE_INPUT))),
        ('DrawImage',   FUNCPTR(EFI_STATUS, PTR(EFI_HII_IMAGE_PROTOCOL), EFI_HII_DRAW_FLAGS, PTR(EFI_IMAGE_INPUT), PTR(PTR(EFI_IMAGE_OUTPUT)), UINTN, UINTN)),
        ('DrawImageId', FUNCPTR(EFI_STATUS, PTR(EFI_HII_IMAGE_PROTOCOL), EFI_HII_DRAW_FLAGS, EFI_HII_HANDLE, EFI_IMAGE_ID, PTR(PTR(EFI_IMAGE_OUTPUT)), UINTN, UINTN))
    ]

@dxeapi(params = {
    "This"              : POINTER,              # IN CONST  PTR(EFI_HII_IMAGE_PROTOCOL)
    "PackageList"       : POINTER,              # IN        EFI_HII_HANDLE
    "ImageId"           : POINTER,              # OUT       PTR(EFI_IMAGE_ID)
    "Image"             : POINTER               # IN CONST  PTR(EFI_IMAGE_INPUT)
})
def hook_NewImage(ql: Qiling, address: int, params):
    pass

@dxeapi(params = {
    "This"              : POINTER,              # IN CONST  PTR(EFI_HII_IMAGE_PROTOCOL)
    "PackageList"       : POINTER,              # IN        EFI_HII_HANDLE
    "ImageId"           : POINTER,              # IN        EFI_IMAGE_ID
    "Image"             : POINTER               # OUT       PTR(EFI_IMAGE_INPUT)
})
def hook_GetImage(ql: Qiling, address: int, params):
    pass

@dxeapi(params = {
    "This"              : POINTER,              # IN CONST  PTR(EFI_HII_IMAGE_PROTOCOL)
    "PackageList"       : POINTER,              # IN        EFI_HII_HANDLE
    "ImageId"           : POINTER,              # IN        EFI_IMAGE_ID
    "Image"             : POINTER               # IN CONST  PTR(EFI_IMAGE_INPUT)
})
def hook_SetImage(ql: Qiling, address: int, params):
    pass

@dxeapi(params = {
    "This"              : POINTER,              # IN CONST  PTR(EFI_HII_IMAGE_PROTOCOL)
    "Flags"             : EFI_HII_DRAW_FLAGS,   # IN        EFI_HII_DRAW_FLAGS
    "Image"             : POINTER,              # IN CONST  PTR(EFI_IMAGE_INPUT)
    "Blt"               : POINTER,              # IN OUT    PTR(PTR(EFI_IMAGE_OUTPUT))
    "BltX"              : UINTN,                # IN        UINTN
    "BltY"              : UINTN                 # IN        UINTN
})
def hook_DrawImage(ql: Qiling, address: int, params):
    pass

@dxeapi(params = {
    "This"              : POINTER,              # IN CONST  PTR(EFI_HII_IMAGE_PROTOCOL)
    "Flags"             : EFI_HII_DRAW_FLAGS,   # IN        EFI_HII_DRAW_FLAGS
    "PackageList"       : POINTER,              # IN        EFI_HII_HANDLE
    "ImageId"           : POINTER,              # IN        EFI_IMAGE_ID
    "Blt"               : POINTER,              # IN OUT    PTR(PTR(EFI_IMAGE_OUTPUT))
    "BltX"              : UINTN,                # IN        UINTN
    "BltY"              : UINTN                 # IN        UINTN
})
def hook_DrawImageId(ql: Qiling, address: int, params):
    pass

descriptor = {
    "guid" : "31a6406a-6bdf-4e46-b2a2-ebaa89c40920",
    "struct" : EFI_HII_IMAGE_PROTOCOL,
    "fields" : (
        ("NewImage", hook_NewImage),
        ("GetImage", hook_GetImage),
        ("SetImage", hook_SetImage),
        ("DrawImage", hook_DrawImage),
        ("DrawImageId", hook_DrawImageId)
    )
}
