#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from ctypes import POINTER
from ..ProcessorBind import *
from ..UefiBaseType import *

from qiling.os.uefi.UefiInternalFormRepresentation import EFI_HII_PACKAGE_LIST_HEADER

# @see: MdePkg\Include\Protocol\HiiPackageList.h
# Upon loading a module with a HII resource, this should be installed on the module's handle,
# such that calling HandleProtocol() will directly return the pointer to the struct in the interface
#
# In EDK2:
#
# typedef EFI_HII_PACKAGE_LIST_HEADER *EFI_HII_PACKAGE_LIST_PROTOCOL;


class EFI_HII_PACKAGE_LIST_PROTOCOL(POINTER(EFI_HII_PACKAGE_LIST_HEADER)):
    pass

def make_descriptor(hii_package_list_header_ptr: int):
    return {
        "guid" : "6a1ee763-d47a-43b4-aabe-ef1de2ab56fc",
        "pointer_name": EFI_HII_PACKAGE_LIST_PROTOCOL,
        "address": hii_package_list_header_ptr
    }
