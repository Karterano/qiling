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

from .EfiHiiImageProtocol import EFI_IMAGE_OUTPUT
from .EfiGraphicsOutputProtocol import EFI_GRAPHICS_OUTPUT_BLT_PIXEL

EFI_FONT_HANDLE = PTR(VOID)

EFI_HII_OUT_FLAGS = UINT32

class EFI_HII_ROW_INFO(STRUCT):
    _fields_ = [
        ('StartIndex',      UINTN),
        ('EndIndex',        UINTN),
        ('LineHeight',      UINTN),
        ('LineWidth',       UINTN),
        ('BaselineOffset',  UINTN),
    ]

EFI_FONT_INFO_MASK = UINT32

class EFI_FONT_INFO(STRUCT):
    _fields_ = [
        ('FontStyle',   EFI_HII_FONT_STYLE),
        ('FontSize',    UINT16),
        ('FontName',    CHAR16 * 1)  # Array[1]
    ]

class EFI_FONT_DISPLAY_INFO(STRUCT):
    _fields_ = [
        ('ForegroundColor', EFI_GRAPHICS_OUTPUT_BLT_PIXEL),
        ('BackgroundColor', EFI_GRAPHICS_OUTPUT_BLT_PIXEL),
        ('FontInfoMask',    EFI_FONT_INFO_MASK),
        ('FontInfo',        EFI_FONT_INFO)
    ]


# @see: MdePkg\Include\Protocol\HiiFont.h
class EFI_HII_FONT_PROTOCOL(STRUCT):
    EFI_HII_FONT_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('StringToImage',   FUNCPTR(EFI_STATUS, PTR(EFI_HII_FONT_PROTOCOL), EFI_HII_OUT_FLAGS, EFI_STRING, PTR(EFI_FONT_DISPLAY_INFO), PTR(PTR(EFI_IMAGE_OUTPUT)), UINTN, UINTN, PTR(PTR(EFI_HII_ROW_INFO)), PTR(UINTN), PTR(UINTN))),
        ('StringIdToImage', FUNCPTR(EFI_STATUS, PTR(EFI_HII_FONT_PROTOCOL), EFI_HII_OUT_FLAGS, EFI_HII_HANDLE, EFI_STRING_ID, PTR(CHAR8), PTR(EFI_FONT_DISPLAY_INFO), PTR(PTR(EFI_IMAGE_OUTPUT)), UINTN, UINTN, PTR(PTR(EFI_HII_ROW_INFO)), PTR(UINTN), PTR(UINTN))),
        ('GetGlyph',        FUNCPTR(EFI_STATUS, PTR(EFI_HII_FONT_PROTOCOL), CHAR16, PTR(EFI_FONT_DISPLAY_INFO), PTR(PTR(EFI_IMAGE_OUTPUT)), PTR(UINTN))),
        ('GetFontInfo',     FUNCPTR(EFI_STATUS, PTR(EFI_HII_FONT_PROTOCOL), PTR(EFI_FONT_HANDLE), PTR(EFI_FONT_DISPLAY_INFO), PTR(PTR(EFI_FONT_DISPLAY_INFO)), EFI_STRING))
    ]

    @dxeapi(params = {
        "This"              : POINTER,              # IN CONST  PTR(EFI_HII_FONT_PROTOCOL)
        "Flags"             : EFI_HII_OUT_FLAGS,    # IN        EFI_HII_OUT_FLAGS
        "String"            : WSTRING,              # IN CONST  EFI_STRING
        "StringInfo"        : POINTER,              # IN CONST  PTR(EFI_FONT_DISPLAY_INFO)
        "Blt"               : POINTER,              # IN OUT    PTR(PTR(EFI_IMAGE_OUTPUT))
        "BltX"              : UINTN,                # IN        UINTN
        "BltY"              : UINTN,                # IN        UINTN
        "RowInfoArray"      : POINTER,              # OUT       PTR(PTR(EFI_HII_ROW_INFO))  OPTIONAL
        "RowInfoArraySize"  : POINTER,              # OUT       PTR(UINTN)                  OPTIONAL
        "ColumnInfoArray"   : POINTER               # OUT       PTR(UINTN)                  OPTIONAL
    })
    def hook_StringToImage(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"              : POINTER,              # IN CONST  PTR(EFI_HII_FONT_PROTOCOL)
        "Flags"             : EFI_HII_OUT_FLAGS,    # IN        EFI_HII_OUT_FLAGS
        "PackageList"       : POINTER,              # IN        EFI_HII_HANDLE
        "StringId"          : EFI_STRING_ID,        # IN        EFI_STRING_ID
        "Language"          : POINTER,              # IN CONST  PTR(CHAR8)
        "StringInfo"        : POINTER,              # IN CONST  PTR(EFI_FONT_DISPLAY_INFO)  OPTIONAL
        "Blt"               : POINTER,              # IN OUT    PTR(PTR(EFI_IMAGE_OUTPUT))
        "BltX"              : UINTN,                # IN        UINTN
        "BltY"              : UINTN,                # IN        UINTN
        "RowInfoArray"      : POINTER,              # OUT       PTR(PTR(EFI_HII_ROW_INFO))  OPTIONAL
        "RowInfoArraySize"  : POINTER,              # OUT       PTR(UINTN)                  OPTIONAL
        "ColumnInfoArray"   : POINTER               # OUT       PTR(UINTN)                  OPTIONAL
    })
    def hook_StringIdToImage(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"              : POINTER,              # IN CONST  PTR(EFI_HII_FONT_PROTOCOL)
        "Char"              : CHAR16,               # IN CONST  CHAR16
        "StringInfo"        : POINTER,              # IN CONST  PTR(EFI_FONT_DISPLAY_INFO)
        "Blt"               : POINTER,              # OUT       PTR(PTR(EFI_IMAGE_OUTPUT))
        "Baseline"          : POINTER               # OUT       PTR(UINTN)                  OPTIONAL
    })
    def hook_GetGlyph(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"              : POINTER,          # IN CONST      PTR(EFI_HII_FONT_PROTOCOL)
        "FontHandle"        : POINTER,          # IN OUT        PTR(EFI_FONT_HANDLE)
        "StringInfoIn"      : POINTER,          # IN CONST      PTR(EFI_FONT_DISPLAY_INFO)  OPTIONAL
        "StringInfoOut"     : POINTER,          # OUT           PTR(PTR(EFI_FONT_DISPLAY_INFO))
        "String"            : WSTRING           # IN CONST      EFI_STRING                  OPTIONAL
    })
    def hook_GetFontInfo(ql: Qiling, address: int, params):
        pass

descriptor = {
    "guid" : "e9ca4775-8657-47fc-97e7-7ed65a084324",
    "struct" : EFI_HII_FONT_PROTOCOL,
    "fields" : (
        ("StringToImage", EFI_HII_FONT_PROTOCOL.hook_StringToImage),
        ("StringIdToImage", EFI_HII_FONT_PROTOCOL.hook_StringIdToImage),
        ("GetGlyph", EFI_HII_FONT_PROTOCOL.hook_GetGlyph),
        ("GetFontInfo", EFI_HII_FONT_PROTOCOL.hook_GetFontInfo)
    )
}
