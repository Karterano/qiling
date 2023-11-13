#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from qiling import Qiling
from qiling.os.uefi import bs, rt
from qiling.os.uefi.utils import init_struct
from .ProcessorBind import *
from .UefiBaseType import *
from .UefiMultiPhase import *
from qiling.os.uefi.UefiSpec import EFI_SIMPLE_TEXT_INPUT_PROTOCOL, EFI_CONFIGURATION_TABLE
from qiling.os.uefi.protocols.EfiSimpleTextOutputProtocol import EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL

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


def initialize(ql: Qiling, gST: int, gBS: int, gRT: int, cfg: int, out: int):
    descriptor = {
        'struct' : EFI_SYSTEM_TABLE,
        'fields' : (
            ('Hdr',                     None),
            ('ConsoleInHandle',        1),
            ('ConsoleOutHandle',        1),
            ('ConOut',                  out),
            ('StandardErrorHandle',     1),
            ('StdErr',                  out),
            ('RuntimeServices',         gRT),
            ('BootServices',            gBS),
            ('NumberOfTableEntries',    0),
            ('ConfigurationTable',      cfg)
        )
    }

    ql.loader.gST = gST

    instance = init_struct(ql, gST, descriptor)
    instance.saveTo(ql, gST)

__all__ = [
    'initialize'
]