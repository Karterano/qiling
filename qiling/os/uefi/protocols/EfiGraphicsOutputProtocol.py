#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from qiling import Qiling
from qiling.os.const import *
from qiling.os.uefi.const import *
from ..fncc import *
# from ..ProcessorBind import *
# from ..UefiBaseType import *

from qiling.os.uefi.UefiInternalFormRepresentation import *


class EFI_PIXEL_BITMASK(STRUCT):
    _fields_ = [
        ('RedMask',         UINT32),
        ('GreenMask',       UINT32),
        ('BlueMask',        UINT32),
        ('ReservedMask',    UINT32),
    ]

class EFI_GRAPHICS_PIXEL_FORMAT(ENUM):
    _members_ = [
        'PixelRedGreenBlueReserved8BitPerColor',
        'PixelBlueGreenRedReserved8BitPerColor',
        'PixelBitMask',
        'PixelBltOnly',
        'PixelFormatMax'
    ]

class EFI_GRAPHICS_OUTPUT_MODE_INFORMATION(STRUCT):
    _fields_ = [
        ('Version',                 UINT32),
        ('HorizontalResolution',    UINT32),
        ('VerticalResolution',      UINT32),
        ('PixelFormat',             EFI_GRAPHICS_PIXEL_FORMAT),
        ('PixelInformation',        EFI_PIXEL_BITMASK),
        ('PixelsPerScanLine',       UINT32)
    ]

class EFI_GRAPHICS_OUTPUT_BLT_PIXEL(STRUCT):
    _fields_ = [
        ('Blue',        UINT8),
        ('Green',       UINT8),
        ('Red',         UINT8),
        ('Reserved',    UINT8)
    ]

class EFI_GRAPHICS_OUTPUT_BLT_OPERATION(ENUM):
    _members_ = [
        'EfiBltVideoFill',
        'EfiBltVideoToBltBuffer',
        'EfiBltBufferToVideo',
        'EfiBltVideoToVideo'
    ]

class EFI_GRAPHICS_OUTPUT_PROTOCOL_MODE(STRUCT):
    _fields_ = [
        ('MaxMode',         UINT32),
        ('Mode',            UINT32),
        ('Info',            EFI_GRAPHICS_OUTPUT_MODE_INFORMATION),
        ('SizeOfInfo',      UINTN),
        ('FrameBufferBase', EFI_PHYSICAL_ADDRESS),
        ('FrameBufferSize', UINTN)
    ]

# @see: MdePkg\Include\Protocol\GraphicsOutput.h
class EFI_GRAPHICS_OUTPUT_PROTOCOL(STRUCT):
    EFI_GRAPHICS_OUTPUT_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('QueryMode',       FUNCPTR(EFI_STATUS, PTR(EFI_GRAPHICS_OUTPUT_PROTOCOL), UINT32, PTR(UINTN), PTR(PTR(EFI_GRAPHICS_OUTPUT_MODE_INFORMATION)))),
        ('SetMode',         FUNCPTR(EFI_STATUS, PTR(EFI_GRAPHICS_OUTPUT_PROTOCOL), UINT32)),
        ('Blt',             FUNCPTR(EFI_STATUS, PTR(EFI_GRAPHICS_OUTPUT_PROTOCOL), PTR(EFI_GRAPHICS_OUTPUT_BLT_PIXEL), EFI_GRAPHICS_OUTPUT_BLT_OPERATION, UINTN, UINTN, UINTN, UINTN, UINTN, UINTN, UINTN)),
        ('Mode',            PTR(EFI_GRAPHICS_OUTPUT_PROTOCOL_MODE))
    ]

    @dxeapi(params = {
        "This"          : POINTER,  # IN        PTR(CONST EFI_HII_STRING_PROTOCOL)
        "ModeNumber"    : UINT32,   # IN        UINT32
        "SizeOfInfo"    : POINTER,  # OUT       PTR(UINTN)
        "Info"          : POINTER   # OUT       PTR(PTR(EFI_GRAPHICS_OUTPUT_MODE_INFORMATION))
    })
    def hook_QueryMode(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN        PTR(CONST EFI_HII_STRING_PROTOCOL)
        "ModeNumber"    : UINT32    # IN        UINT32
    })
    def hook_SetMode(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN        PTR(CONST EFI_HII_STRING_PROTOCOL)
        "BltBuffer"     : POINTER,  # IN        PTR(EFI_GRAPHICS_OUTPUT_BLT_PIXEL)  OPTIONAL
        "BltOperation"  : ENUM,     # IN        EFI_GRAPHICS_OUTPUT_BLT_OPERATION
        "SourceX"       : UINTN,    # IN        UINTN
        "SourceY"       : UINTN,    # IN        UINTN
        "DestinationX"  : UINTN,    # IN        UINTN
        "DestinationY"  : UINTN,    # IN        UINTN
        "Width"         : UINTN,    # IN        UINTN
        "Height"        : UINTN,    # IN        UINTN
        "Delta"         : UINTN,    # IN        UINTN                               OPTIONAL
    })
    def hook_Blt(ql: Qiling, address: int, params):
        pass

descriptor = {
    "guid" : "9042a9de-23dc-4a38-96fb-7aded080516a",
    "struct" : EFI_GRAPHICS_OUTPUT_PROTOCOL,
    "fields" : (
        ("QueryMode", EFI_GRAPHICS_OUTPUT_PROTOCOL.hook_QueryMode),
        ("SetMode", EFI_GRAPHICS_OUTPUT_PROTOCOL.hook_SetMode),
        ("Blt", EFI_GRAPHICS_OUTPUT_PROTOCOL.hook_Blt),
        # TODO this should probably be initialized properly
        ("Mode", 0)
    )
}
