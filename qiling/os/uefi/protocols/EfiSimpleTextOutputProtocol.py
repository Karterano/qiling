#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from qiling import Qiling
from qiling.os.const import *
# from qiling.os.uefi.const import *
from ..fncc import *
# from ..ProcessorBind import *
# from ..UefiBaseType import *

from qiling.os.uefi.UefiInternalFormRepresentation import *


class EFI_SIMPLE_TEXT_OUTPUT_MODE(STRUCT):
    _fields_ = [
        ('MaxMode',         INT32),
        ('Mode',            INT32),
        ('Attribute',       INT32),
        ('CursorColumn',    INT32),
        ('CursorRow',       INT32),
        ('CursorVisible',   BOOLEAN)
    ]


# @see: MdePkg\Include\Protocol\SimpleTextOut.h
class EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL(STRUCT):
    EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('Reset',               FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL), BOOLEAN)),
        ('OutputString',        FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL), PTR(CHAR16))),
        ('TestString',          FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL), PTR(CHAR16))),
        ('QueryMode',           FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL), UINTN, PTR(UINTN), PTR(UINTN))),
        ('SetMode',             FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL), UINTN)),
        ('SetAttribute',        FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL), UINTN)),
        ('ClearScreen',         FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL))),
        ('SetCursorPosition',   FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL), UINTN, UINTN)),
        ('EnableCursor',        FUNCPTR(EFI_STATUS, PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL), BOOLEAN)),
        ('Mode',                PTR(EFI_SIMPLE_TEXT_OUTPUT_MODE))
    ]

    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
        "ExtendedVerification"      : BOOLEAN   # IN        BOOLEAN
    })
    def hook_Reset(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
        "String"                    : POINTER   # IN        PTR(CHAR16)
    })
    def hook_OutputString(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
        "String"                    : POINTER   # IN        PTR(CHAR16)
    })
    def hook_TestString(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
        "ModeNumber"                : UINTN,    # IN        UINTN
        "Columns"                   : POINTER,  # OUT       PTR(UINTN)
        "Rows"                      : POINTER   # OUT       PTR(UINTN)
    })
    def hook_QueryMode(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
        "ModeNumber"                : UINTN     # IN        UINTN
    })
    def hook_SetMode(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
        "Attribute"                : UINTN      # IN        UINTN
    })
    def hook_SetAttribute(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
    })
    def hook_ClearScreen(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
        "Column"                    : UINTN,    # IN        UINTN
        "Row"                       : UINTN,    # IN        UINTN
    })
    def hook_SetCursorPosition(ql: Qiling, address: int, params):
        pass


    @dxeapi(params = {
        "This"                      : POINTER,  # IN        PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)
        "Visible"                   : BOOLEAN   # IN        BOOLEAN
    })
    def hook_EnableCursor(ql: Qiling, address: int, params):
        pass

descriptor = {
    "guid" : "387477c2-69c7-11d2-8e39-00a0c969723b",
    "struct" : EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL,
    "fields" : (
        ("Reset",               EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_Reset),
        ("OutputString",        EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_OutputString),
        ("TestString",          EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_TestString),
        ("QueryMode",           EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_QueryMode),
        ("SetMode",             EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_SetMode),
        ("SetAttribute",        EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_SetAttribute),
        ("ClearScreen",         EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_ClearScreen),
        ("SetCursorPosition",   EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_SetCursorPosition),
        ("EnableCursor",        EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL.hook_EnableCursor),
        # TODO this should probably be initialized properly
        ("Mode", 0)
    )
}
