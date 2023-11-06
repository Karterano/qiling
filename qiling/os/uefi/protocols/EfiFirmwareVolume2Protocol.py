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
from ..PiMultiPhase import *
from .. import utils


EFI_FV_ATTRIBUTES = UINT64
EFI_FV_FILETYPE = UINT8
EFI_FV_FILE_ATTRIBUTES = UINT32
EFI_SECTION_TYPE = UINT8
EFI_FV_WRITE_POLICY = UINT32


class EFI_FV_WRITE_FILE_DATA(STRUCT):
    _fields_ = [
        ('NameGuid',           PTR(EFI_GUID)),
        ('Type',                EFI_FV_FILETYPE),
        ('FileAttributes',      EFI_FV_FILE_ATTRIBUTES),
        ('Buffer',             PTR(VOID)),
        ('BufferSize',          UINT32)
    ]

class EFI_FIRMWARE_VOLUME2_PROTOCOL(STRUCT):
    EFI_FIRMWARE_VOLUME2_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('GetVolumeAttributes', FUNCPTR(EFI_STATUS, PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL), PTR(EFI_FV_ATTRIBUTES))),
        ('SetVolumeAttributes', FUNCPTR(EFI_STATUS, PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL), PTR(EFI_FV_ATTRIBUTES))),
        ('ReadFile',            FUNCPTR(EFI_STATUS, PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL), PTR(EFI_GUID), PTR(PTR(VOID)), PTR(UINTN), PTR(EFI_FV_FILETYPE), PTR(EFI_FV_FILE_ATTRIBUTES), PTR(UINT32))),
        ('ReadSection',         FUNCPTR(EFI_STATUS, PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL), PTR(EFI_GUID), EFI_SECTION_TYPE , UINTN, PTR(PTR(VOID)), PTR(UINTN), PTR(UINT32))),
        ('WriteFile',           FUNCPTR(EFI_STATUS, PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL), UINT32, EFI_FV_WRITE_POLICY, PTR(EFI_FV_WRITE_FILE_DATA))),
        ('GetNextFile',         FUNCPTR(EFI_STATUS, PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL), PTR(VOID), PTR(EFI_FV_FILETYPE), PTR(EFI_GUID), PTR(EFI_FV_FILE_ATTRIBUTES), PTR(UINTN))),
        ('KeySize',             UINT32),
        ('ParentHandle',        EFI_HANDLE),
        ('GetInfo',             FUNCPTR(EFI_STATUS, PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL), PTR(EFI_GUID), PTR(UINTN), PTR(VOID))),
        ('SetInfo',             FUNCPTR(EFI_STATUS, PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL), PTR(EFI_GUID), UINTN, PTR(VOID))),
    ]

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL)
        "FvAttributes"  : POINTER   # OUT PTR(EFI_FV_ATTRIBUTES)
    })
    def hook_GetVolumeAttributes(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL)
        "FvAttributes"  : POINTER   # IN OUT PTR(EFI_FV_ATTRIBUTES)
    })
    def hook_SetVolumeAttributes(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                  : POINTER,  # IN CONST PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL)
        "NameGuid"              : POINTER,  # IN CONST PTR(EFI_GUID)
        "Buffer"                : POINTER,  # IN OUT PTR(PTR(VOID))
        "BufferSize"            : POINTER,  # IN OUT PTR(UINTN)
        "FoundType"             : POINTER,  # OUT PTR(EFI_FV_FILETYPE)
        "FileAttributes"        : POINTER,  # OUT PTR(EFI_FV_FILE_ATTRIBUTES)
        "AuthenticationStatus"  : POINTER   # OUT PTR(UINT32)
    })
    def hook_ReadFile(ql: Qiling, address: int, params):
        return EFI_NOT_FOUND

    @dxeapi(params = {
        "This"                  : POINTER,          # IN CONST PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL)
        "NameGuid"              : POINTER,          # IN CONST PTR(EFI_GUID)
        "SectionType"           : EFI_SECTION_TYPE, # IN EFI_SECTION_TYPE
        "SectionInstance"       : UINTN,            # IN UINTN
        "Buffer"                : POINTER,          # IN OUT PTR(PTR(VOID))
        "BufferSize"            : POINTER,          # IN OUT PTR(UINTN)
        "AuthenticationStatus"  : POINTER           # OUT PTR(UINT32)
    })
    def hook_ReadSection(ql: Qiling, address: int, params):
        return EFI_NOT_FOUND

    @dxeapi(params = {
        "This"                  : POINTER,              # IN CONST PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL)
        "NumberOfFiles"         : UINT32,               # IN UINT32
        "WritePolicy"           : EFI_FV_WRITE_POLICY,  # IN EFI_FV_WRITE_POLICY
        "FileData"              : POINTER               # IN PTR(EFI_FV_WRITE_FILE_DATA)
    })
    def hook_WriteFile(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                  : POINTER,          # IN CONST PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL)
        "Key"                   : POINTER,          # IN OUT PTR(VOID)
        "FileType"              : POINTER,          # IN OUT PTR(EFI_FV_FILETYPE)
        "NameGuid"              : POINTER,          # OUT PTR(EFI_GUID)
        "Attributes"            : POINTER,          # OUT PTR(EFI_FV_FILE_ATTRIBUTES)
        "Size"                  : POINTER           # OUT PTR(UINTN)
    })
    def hook_GetNextFile(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                  : POINTER,          # IN CONST PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL)
        "InformationType"       : POINTER,          # IN CONST PTR(EFI_GUID)
        "BufferSize"            : POINTER,          # IN OUT PTR(UINTN)
        "Buffer"                : POINTER           # OUT PTR(VOID)
    })
    def hook_GetInfo(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                  : POINTER,          # IN CONST PTR(EFI_FIRMWARE_VOLUME2_PROTOCOL)
        "InformationType"       : POINTER,          # IN CONST PTR(EFI_GUID)
        "BufferSize"            : UINTN,            # IN UINTN
        "Buffer"                : POINTER           # IN CONST PTR(VOID)
    })
    def hook_SetInfo(ql: Qiling, address: int, params):
        pass

descriptor = {
    "guid" : "220e73b6-6bdb-4413-8405-b974b108619a",
    "struct" : EFI_FIRMWARE_VOLUME2_PROTOCOL,
    "fields" : (
        ("GetVolumeAttributes", EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_GetVolumeAttributes),
        ("SetVolumeAttributes", EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_SetVolumeAttributes),
        ("ReadFile",            EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_ReadFile),
        ("ReadSection",         EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_ReadSection),
        ("WriteFile",           EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_WriteFile),
        ("GetNextFile",         EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_GetNextFile),
        ("GetInfo",             EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_GetInfo),
        ("SetInfo",             EFI_FIRMWARE_VOLUME2_PROTOCOL.hook_SetInfo),
    )
}
