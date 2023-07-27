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

from qiling.os.uefi.protocols.EfiHiiFontProtocol import EFI_FONT_INFO

from qiling.os.uefi.UefiInternalFormRepresentation import EFI_HII_HANDLE, EFI_STRING, EFI_STRING_ID


# @see: MdePkg\Include\Protocol\HiiString.h
class EFI_HII_STRING_PROTOCOL(STRUCT):
    EFI_HII_STRING_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('NewString',               FUNCPTR(EFI_STATUS, PTR(EFI_HII_STRING_PROTOCOL), EFI_HII_HANDLE, PTR(EFI_STRING_ID), PTR(CHAR8), PTR(CHAR16), EFI_STRING, PTR(EFI_FONT_INFO))),
        ('GetString',               FUNCPTR(EFI_STATUS, PTR(EFI_HII_STRING_PROTOCOL), PTR(CHAR8), EFI_HII_HANDLE, EFI_STRING_ID, EFI_STRING, PTR(UINTN), PTR(PTR(EFI_FONT_INFO)))),
        ('SetString',               FUNCPTR(EFI_STATUS, PTR(EFI_HII_STRING_PROTOCOL), EFI_HII_HANDLE, EFI_STRING_ID, PTR(CHAR8), EFI_STRING, PTR(EFI_FONT_INFO))),
        ('GetLanguages',            FUNCPTR(EFI_STATUS, PTR(EFI_HII_STRING_PROTOCOL), EFI_HII_HANDLE, PTR(CHAR8), PTR(UINTN))),
        ('GetSecondaryLanguages',   FUNCPTR(EFI_STATUS, PTR(EFI_HII_STRING_PROTOCOL), EFI_HII_HANDLE, PTR(CHAR8), PTR(CHAR8), PTR(UINTN)))
    ]

@dxeapi(params = {
    "This"          : POINTER,  # IN CONST PTR(CONST EFI_HII_STRING_PROTOCOL)
    "PackageList"   : POINTER,  # IN EFI_HII_HANDLE
    "StringId"      : POINTER,  # OUT PTR(EFI_STRING_ID)
    "Language"      : POINTER,  # IN CONST PTR(CHAR8)
    "LanguageName"  : POINTER,  # IN CONST PTR(CHAR16)
    "String"        : WSTRING,  # IN CONST EFI_STRING
    "StringFontInfo": POINTER   # IN CONST PTR(EFI_FONT_INFO)
})
def hook_NewString(ql: Qiling, address: int, params):
    pass

@dxeapi(params = {
    "This"          : POINTER,          # IN CONST PTR(CONST EFI_HII_STRING_PROTOCOL)
    "Language"      : POINTER,          # IN CONST PTR(CHAR8)
    "PackageList"   : POINTER,          # IN EFI_HII_HANDLE
    "StringId"      : EFI_STRING_ID,    # IN EFI_STRING_ID
    "String"        : WSTRING,          # OUT EFI_STRING
    "StringSize"    : POINTER,          # IN OUT PTR(UINTN)
    "StringFontInfo": POINTER,          # OUT EFI_FONT_INFO PTR(PTR(EFI_FONT_INFO))
})
def hook_GetString(ql: Qiling, address: int, params):
    pass

@dxeapi(params = {
    "This"              : POINTER,          # IN CONST PTR(CONST EFI_HII_STRING_PROTOCOL)
    "PackageList"       : POINTER,          # IN EFI_HII_HANDLE
    "StringId"          : EFI_STRING_ID,    # IN EFI_STRING_ID
    "Language"          : POINTER,          # IN CONST PTR(CHAR8)
    "String"            : WSTRING,          # IN CONST EFI_STRING
    "StringFontInfo"    : POINTER           # IN CONST PTR(EFI_FONT_INFO)
})
def hook_SetString(ql: Qiling, address: int, params):
    pass

@dxeapi(params = {
    "This"              : POINTER,      # IN CONST PTR(CONST EFI_HII_STRING_PROTOCOL)
    "PackageList"       : POINTER,      # IN EFI_HII_HANDLE
    "Languages"         : POINTER,      # IN OUT PTR(CHAR8)
    "LanguagesSize"     : POINTER,     # IN OUT PTR(UINTN)
})
def hook_GetLanguages(ql: Qiling, address: int, params):
    pass

@dxeapi(params = {
    "This"                      : POINTER,  # IN CONST PTR(CONST EFI_HII_STRING_PROTOCOL)
    "PackageList"               : POINTER,  # IN EFI_HII_HANDLE
    "PrimaryLanguage"           : POINTER,  # IN CONST PTR(CHAR8)
    "SecondaryLanguages"        : POINTER,  # IN OUT PTR(CHAR8)
    "SecondaryLanguagesSize"    : POINTER   # IN OUT PTR(UINTN)
})
def hook_GetSecondaryLanguages(ql: Qiling, address: int, params):
    pass

descriptor = {
    "guid" : "0fd96974-23aa-4cdc-b9cb-98d17750322a",
    "struct" : EFI_HII_STRING_PROTOCOL,
    "fields" : (
        ("NewString", hook_NewString),
        ("GetString", hook_GetString),
        ("SetString", hook_SetString),
        ("GetLanguages", hook_GetLanguages),
        ("GetSecondaryLanguages", hook_GetSecondaryLanguages)
    )
}
