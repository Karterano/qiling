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


EFI_STATUS_CODE_TYPE = UINT32
EFI_STATUS_CODE_VALUE = UINT32


class EFI_STATUS_CODE_DATA(STRUCT):
    _fields_ = [
        ('HeaderSize',  UINT16),
        ('Size',        UINT16),
        ('Type',        EFI_GUID)
    ]

# @see: MdePkg\Include\Protocol\MmAccess.h
class _EFI_STATUS_CODE_PROTOCOL(STRUCT):
    _EFI_STATUS_CODE_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('ReportStatusCode',    FUNCPTR(EFI_STATUS, EFI_STATUS_CODE_TYPE ,EFI_STATUS_CODE_VALUE, UINT32, PTR(EFI_GUID), PTR(EFI_STATUS_CODE_DATA)))
    ]

@dxeapi(params = {
    "Type"      : EFI_STATUS_CODE_TYPE,     # IN EFI_STATUS_CODE_TYPE
    "Value"     : EFI_STATUS_CODE_VALUE,    # IN EFI_STATUS_CODE_VALUE
    "Instance"  : UINT32,                   # IN UINT32
    "CallerId"  : POINTER,                  # IN PTR(EFI_GUID) OPTIONAL
    "Data"      : POINTER                   # IN PTR(EFI_STATUS_CODE_DATA) OPTIONAL
})
def hook_ReportStatusCode(ql: Qiling, address: int, params):
    pass

descriptor = {
    "guid" : "d2b2b828-0826-48a7-b3df-983c006024f0",
    "struct" : _EFI_STATUS_CODE_PROTOCOL,
    "fields" : (
        ("ReportStatusCode", hook_ReportStatusCode),
    )
}
