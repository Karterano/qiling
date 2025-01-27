#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from qiling import Qiling
from qiling.os.const import *
from qiling.os.uefi.const import *
from .EfiLDevicePathProtocol import EFI_DEVICE_PATH_PROTOCOL
from ..fncc import *
from ..ProcessorBind import *
from ..UefiBaseType import *

from qiling.os.uefi.UefiInternalFormRepresentation import EFI_STRING

# @see: MdePkg\Include\Protocol\HiiConfigRouting.h
class EFI_HII_CONFIG_ROUTING_PROTOCOL(STRUCT):
    EFI_HII_CONFIG_ROUTING_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('ExtractConfig',          FUNCPTR(EFI_STATUS, PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL), EFI_STRING, PTR(EFI_STRING), PTR(EFI_STRING))),
        ('ExportConfig',          FUNCPTR(EFI_STATUS, PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL), PTR(EFI_STRING))),
        ('RouteConfig',          FUNCPTR(EFI_STATUS, PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL), EFI_STRING, PTR(EFI_STRING))),
        ('BlockToConfig',          FUNCPTR(EFI_STATUS, PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL), EFI_STRING, PTR(UINT8), UINTN, PTR(EFI_STRING), PTR(EFI_STRING))),
        ('ConfigToBlock',          FUNCPTR(EFI_STATUS, PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL), EFI_STRING, PTR(UINT8), PTR(UINTN), PTR(EFI_STRING))),
        ('GetAltConfig',          FUNCPTR(EFI_STATUS, PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL), PTR(EFI_GUID), EFI_STRING, PTR(EFI_DEVICE_PATH_PROTOCOL), EFI_STRING, PTR(EFI_STRING))),
    ]

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL)
        "Request"       : WSTRING,  # IN CONST EFI_STRING
        "Progress"      : POINTER,  # OUT PTR(EFI_STRING)
        "Results"      : POINTER,   # OUT PTR(EFI_STRING)
    })
    def hook_ExtractConfig(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL)
        "Results"       : POINTER,   # OUT PTR(EFI_STRING)
    })
    def hook_ExportConfig(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL)
        "Configuration" : WSTRING,  # IN CONST EFI_STRING
        "Progress"      : POINTER,  # OUT PTR(EFI_STRING)
    })
    def hook_RouteConfig(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL)
        "ConfigRequest" : WSTRING,  # IN CONST EFI_STRING
        "Block"         : POINTER,  # IN CONST PTR(UINT8)
        "BlockSize"     : UINTN,    # IN CONST UINTN
        "Config"        : POINTER,  # OUT PTR(EFI_STRING)
        "Progress"      : POINTER,  # OUT PTR(EFI_STRING)
    })
    def hook_BlockToConfig(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL)
        "ConfigResp"    : WSTRING,  # IN CONST EFI_STRING FIXME this is from EDK2 UEFI Spec has PTR(EFI_STRING) instead?!
        "Block"         : POINTER,  # IN OUT PTR(UINT8)
        "BlockSize"     : UINTN,    # IN OUT PTR(UINTN)
        "Progress"      : POINTER,  # OUT PTR(EFI_STRING)
    })
    def hook_ConfigToBlock(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_CONFIG_ROUTING_PROTOCOL)
        "ConfigResp"    : WSTRING,  # IN CONST EFI_STRING
        "Guid"          : POINTER,  # IN CONST PTR(EFI_GUID)
        "Name"          : WSTRING,  # IN CONST EFI_STRING
        "DevicePath"    : POINTER,  # IN CONST PTR(EFI_DEVICE_PATH_PROTOCOL)
        "AltCfgId"      : WSTRING,  # IN CONST EFI_STRING
        "AltCfgResp"    : POINTER,  # OUT PTR(EFI_STRING)
    })
    def hook_GetAltConfig(ql: Qiling, address: int, params):
        pass

descriptor = {
    "guid" : "587e72d7-cc50-4f79-8209-ca291fc1a10f",
    "struct" : EFI_HII_CONFIG_ROUTING_PROTOCOL,
    "fields" : (
        ("ExtractConfig", EFI_HII_CONFIG_ROUTING_PROTOCOL.hook_ExtractConfig),
        ("ExportConfig", EFI_HII_CONFIG_ROUTING_PROTOCOL.hook_ExportConfig),
        ("RouteConfig", EFI_HII_CONFIG_ROUTING_PROTOCOL.hook_RouteConfig),
        ("BlockToConfig", EFI_HII_CONFIG_ROUTING_PROTOCOL.hook_BlockToConfig),
        ("ConfigToBlock", EFI_HII_CONFIG_ROUTING_PROTOCOL.hook_ConfigToBlock),
        ("GetAltConfig", EFI_HII_CONFIG_ROUTING_PROTOCOL.hook_GetAltConfig),
    )
}
