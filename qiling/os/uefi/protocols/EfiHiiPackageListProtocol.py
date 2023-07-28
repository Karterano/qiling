#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

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
#
# We instead model this with a struct with a single member, as the size and address of the struct will be the same 
#  in memory anyway, the pseudo-name '->' is just for logging when initializing and will not be remembered anyway.
#  will be the same in memory later as the original typedef. (Otherwise we would have to change protocol handlers to 
#  install single pointers differently.)


class EFI_HII_PACKAGE_LIST_PROTOCOL(STRUCT):
    _fields_ = [
        ('->', PTR(EFI_HII_PACKAGE_LIST_HEADER))
    ]

def make_descriptor(hii_package_list_header_ptr: int):
    return {
        "guid" : "6a1ee763-d47a-43b4-aabe-ef1de2ab56fc",
        "struct": EFI_HII_PACKAGE_LIST_PROTOCOL,
        "fields": (
            ('->', hii_package_list_header_ptr),
        )
    }
