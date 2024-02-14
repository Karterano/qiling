#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from qiling import Qiling
from qiling.os.uefi import bs, rt, ds, st
from qiling.os.uefi.context import UefiContext
from qiling.os.uefi.utils import init_struct, install_configuration_table
from qiling.os.uefi.protocols import EfiSimpleTextOutputProtocol
# from .ProcessorBind import *
# from .UefiBaseType import *
# from .UefiMultiPhase import *

OUT_HANDLE = 1
MM_HANDLE = 2
FV_HANDLE = 3
HII_HANDLE = 4


# static mem layout:
#
#        +-- EFI_SYSTEM_TABLE ---------+
#        |                             |
#        | ...                         |
#        | RuntimeServices*     -> (1) |
#        | BootServices*        -> (2) |
#        | NumberOfTableEntries        |
#        | ConfigurationTable*  -> (4) |
#        +-----------------------------+
#    (1) +-- EFI_RUNTIME_SERVICES -----+
#        |                             |
#        | ...                         |
#        +-----------------------------+
#    (2) +-- EFI_BOOT_SERVICES --------+
#        |                             |
#        | ...                         |
#        +-----------------------------+
#    (3) +-- EFI_DXE_SERVICES ---------+
#        |                             |
#        | ...                         |
#        +-----------------------------+
#    (4) +-- EFI_CONFIGURATION_TABLE --+        of HOB_LIST
#        | VendorGuid                  |
#        | VendorTable*         -> (5) |
#        +-----------------------------+
#        +-- EFI_CONFIGURATION_TABLE --+        of DXE_SERVICE_TABLE
#        | VendorGuid                  |
#        | VendorTable*         -> (3) |
#        +-----------------------------+
#
#        ... the remainder of the chunk may be used for additional EFI_CONFIGURATION_TABLE entries

# dynamically allocated (context.conf_table_data_ptr):
#
#    (5) +-- VOID* --------------------+
#        | ...                         |
#        +-----------------------------+


def initialize(ql: Qiling, context: UefiContext, base: int, text_out_protocol: int = 0):
    gST = base
    gBS = gST + st.EFI_SYSTEM_TABLE.sizeof()        # boot services
    gRT = gBS + bs.EFI_BOOT_SERVICES.sizeof()        # runtime services
    gDS = gRT + rt.EFI_RUNTIME_SERVICES.sizeof()    # dxe services
    cfg = gDS + ds.EFI_DXE_SERVICES.sizeof()    # configuration tables array
    out = text_out_protocol

    ql.log.info(f'Global tables:')
    ql.log.info(f' | gST   {gST:#010x}')
    ql.log.info(f' | gBS   {gBS:#010x}')
    ql.log.info(f' | gRT   {gRT:#010x}')
    ql.log.info(f' | gDS   {gDS:#010x}')
    ql.log.info(f'')

    ql.os.monotonic_count = 0
    instance = init_struct(ql, gBS, bs.descriptor)
    instance.saveTo(ql, gBS)

    instance = init_struct(ql, gRT, rt.descriptor)
    instance.saveTo(ql, gRT)

    instance = init_struct(ql, gDS, ds.descriptor)
    instance.saveTo(ql, gDS)

    ql.loader.gST = gST
    instance = init_struct(ql, gST, st.make_descriptor({'gBS': gBS, 'gRT': gRT, 'cfg': cfg, 'out': out}))
    instance.saveTo(ql, gST)

    install_configuration_table(context, "HOB_LIST", None)
    install_configuration_table(context, "DXE_SERVICE_TABLE", gDS)
