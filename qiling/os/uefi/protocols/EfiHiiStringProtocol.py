#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from ctypes import sizeof
from qiling import Qiling
from qiling.os.const import *
from qiling.os.uefi.utils import read_int64, write_int64
from qiling.os.uefi.const import *
from qiling.os.uefi.context import HiiContext
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
        hii_context: HiiContext = ql.loader.context.hii_context
        
        package_list_handle = params['PackageList']
        if package_list_handle not in hii_context.package_lists:
            return EFI_NOT_FOUND
        
        supported_languages = hii_context.supported_languages[package_list_handle]
        supported_languages_s = ''.join(s for s in supported_languages)
        supported_languages_b = bytes(supported_languages_s, 'latin1') + b'\x00'

        buffer = params["Languages"]
        ql.log.debug(f"Languages: {hex(buffer)}")

        if params['LanguagesSize'] == 0:
            return EFI_INVALID_PARAMETER
        
        buffer_size = read_int64(ql, params['LanguagesSize'])
        ql.log.debug(f"LanguagesSize: {hex(buffer_size)}")
        
        if buffer_size != 0 and buffer == 0:
            return EFI_INVALID_PARAMETER
        
        # This also captures buffer_size == 0 and buffer == NULL to query the neccessary size
        if len(supported_languages_b) > buffer_size:
            write_int64(ql, params['LanguagesSize'], len(supported_languages_b))
            return EFI_BUFFER_TOO_SMALL

        ql.log.debug(f"Writing {len(supported_languages_b)} bytes to {hex(buffer)}")

        ql.mem.write(buffer, supported_languages_b)
        write_int64(ql, params['LanguagesSize'], len(supported_languages_b))
        return EFI_SUCCESS


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
        ("NewString", EFI_HII_STRING_PROTOCOL.hook_NewString),
        ("GetString", EFI_HII_STRING_PROTOCOL.hook_GetString),
        ("SetString", EFI_HII_STRING_PROTOCOL.hook_SetString),
        ("GetLanguages", EFI_HII_STRING_PROTOCOL.hook_GetLanguages),
        ("GetSecondaryLanguages", EFI_HII_STRING_PROTOCOL.hook_GetSecondaryLanguages)
    )
}
