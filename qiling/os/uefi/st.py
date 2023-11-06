#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from qiling import Qiling
from qiling.os.uefi import bs, rt
from .ProcessorBind import *
from .UefiBaseType import *
from .UefiMultiPhase import *
from qiling.os.uefi.UefiSpec import EFI_SIMPLE_TEXT_INPUT_PROTOCOL, EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL, EFI_CONFIGURATION_TABLE

class EFI_SYSTEM_TABLE(STRUCT):
    _pack_ = 8

    _fields_ = [
        ('Hdr',                        EFI_TABLE_HEADER),
        ('FirmwareVendor',            PTR(CHAR16)),
        ('FirmwareRevision',        UINT32),
        ('ConsoleInHandle',            EFI_HANDLE),
        ('ConIn',                    PTR(EFI_SIMPLE_TEXT_INPUT_PROTOCOL)),
        ('ConsoleOutHandle',        EFI_HANDLE),
        ('ConOut',                    PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)),
        ('StandardErrorHandle',        EFI_HANDLE),
        ('StdErr',                    PTR(EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL)),
        ('RuntimeServices',            PTR(rt.EFI_RUNTIME_SERVICES)),
        ('BootServices',            PTR(bs.EFI_BOOT_SERVICES)),
        ('NumberOfTableEntries',    UINTN),
        ('ConfigurationTable',        PTR(EFI_CONFIGURATION_TABLE))
    ]


def initialize(ql: Qiling, gST: int, gBS: int, gRT: int, cfg: int):
    ql.loader.gST = gST

    instance = EFI_SYSTEM_TABLE()
    instance.RuntimeServices = gRT
    instance.BootServices = gBS
    instance.NumberOfTableEntries = 0
    instance.ConfigurationTable = cfg

    instance.saveTo(ql, gST)

__all__ = [
    'initialize'
]