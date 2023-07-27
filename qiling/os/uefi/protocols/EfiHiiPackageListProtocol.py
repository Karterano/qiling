#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from ..ProcessorBind import *
from ..UefiBaseType import *

from qiling.os.uefi.UefiInternalFormRepresentation import EFI_HII_PACKAGE_LIST_HEADER

# @see: MdePkg\Include\Protocol\HiiPackageList.h
# This is only a pointer to a struct. 
# Upon loading a module with a HII resource, this should be installed on the module's handle,
# such that calling HandleProtocol() will directly return the pointer to the struct in the interface
# TODO the struct should of course already be initialized with the corresponding values from parsing the HII resource

# TODO this is a workaround since protocols that are not structs are not supported by qiling
#  this assumes that it is only access by using the address of the first element
class EFI_HII_PACKAGE_LIST_PROTOCOL(STRUCT):
    _fields_ = [
        ('WORKAROUND FOR EFI_HII_PACKAGE_LIST_HEADER NOT REALLY A STRUCT', PTR(EFI_HII_PACKAGE_LIST_HEADER))
    ]

def make_descriptor(ptr_hii_package_list_header: int):
    descriptor = {
        "guid" : "6a1ee763-d47a-43b4-aabe-ef1de2ab56fc",
        "struct" : EFI_HII_PACKAGE_LIST_PROTOCOL,
        "fields" : (
            ('WORKAROUND FOR EFI_HII_PACKAGE_LIST_HEADER NOT REALLY A STRUCT', ptr_hii_package_list_header),
        )
    }
    return descriptor