#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from uuid import UUID
from qiling import Qiling
from qiling.os.const import *
from qiling.os.uefi.const import *
from qiling.os.uefi.context import HiiContext
from qiling.os.uefi.protocols.EfiLDevicePathProtocol import EFI_DEVICE_PATH_PROTOCOL_GUID
from ..fncc import *
from ..ProcessorBind import *
from ..UefiBaseType import *

from qiling.os.uefi.UefiInternalFormRepresentation import *


EFI_HII_DATABASE_NOTIFY_TYPE = UINTN

EFI_HII_DATABASE_NOTIFY = FUNCPTR(EFI_STATUS, UINT8, PTR(EFI_GUID), PTR(EFI_HII_PACKAGE_HEADER), EFI_HII_HANDLE, EFI_HII_DATABASE_NOTIFY_TYPE)


# @see: MdePkg\Include\Protocol\HiiDatabase.h
class EFI_HII_DATABASE_PROTOCOL(STRUCT):
    EFI_HII_DATABASE_PROTOCOL = STRUCT
    _pack_ = 8

    _fields_ = [
        ('NewPackageList',          FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), PTR(EFI_HII_PACKAGE_LIST_HEADER), EFI_HANDLE, PTR(EFI_HII_HANDLE))),
        ('RemovePackageList',       FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), EFI_HII_HANDLE)),
        ('UpdatePackageList',       FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), EFI_HII_HANDLE, PTR(EFI_HII_PACKAGE_LIST_HEADER))),
        ('ListPackageLists',        FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), UINT8, PTR(EFI_GUID), PTR(UINTN), PTR(EFI_HII_HANDLE))),
        ('ExportPackageLists',      FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), EFI_HII_HANDLE, PTR(UINTN), PTR(EFI_HII_PACKAGE_LIST_HEADER))),
        ('RegisterPackageNotify',   FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), UINT8, PTR(EFI_GUID), EFI_HII_DATABASE_NOTIFY, EFI_HII_DATABASE_NOTIFY_TYPE, PTR(EFI_HANDLE))),
        ('UnregisterPackageNotify', FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), EFI_HANDLE)),
        ('FindKeyboardLayouts',     FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), PTR(UINT16), PTR(EFI_GUID))),
        ('GetKeyboardLayout',       FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), PTR(EFI_GUID), PTR(UINT16), PTR(EFI_HII_KEYBOARD_LAYOUT))),
        ('SetKeyboardLayout',       FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), PTR(EFI_GUID))),
        ('GetPackageListHandle',    FUNCPTR(EFI_STATUS, PTR(EFI_HII_DATABASE_PROTOCOL), EFI_HII_HANDLE, PTR(EFI_HANDLE))),
    ]

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST  PTR(EFI_HII_DATABASE_PROTOCOL)
        "PackageList"   : POINTER,  # IN CONST  PTR(EFI_HII_PACKAGE_LIST_HEADER)
        "DriverHandle"  : POINTER,  # IN        EFI_HANDLE                       OPTIONAL
        "Handle"        : POINTER,  # OUT       PTR(EFI_HII_HANDLE)
    })
    def hook_NewPackageList(ql: Qiling, address: int, params):
        package_list_ptr = params['PackageList']
        handle_ptr = params['Handle']

        if package_list_ptr == 0 or handle_ptr == 0:
            return EFI_INVALID_PARAMETER
        
        ql.log.debug(f"Looking for EFI_HII_PACKAGE_LIST_HEADER at {hex(package_list_ptr)}")

        package_list_header = EFI_HII_PACKAGE_LIST_HEADER.loadFrom(ql, package_list_ptr)
        package_list_guid = UUID(bytes_le=bytes(package_list_header.PackageListGuid))
        ql.log.debug(f"PackageListGuid: {package_list_guid}")
        ql.log.debug(f"PackageLength: {hex(package_list_header.PackagLength)}")

        hii_context: HiiContext = ql.loader.context.hii_context
        handle = hii_context.add_package_list(package_list_ptr, package_list_header)

        ql.mem.write_ptr(handle_ptr, handle)

        driver_handle = params['DriverHandle']
        ql.log.debug(f"DriverHandle: {hex(driver_handle)}")

        if driver_handle != 0:
            # Associate driver_handle with new handle
            hii_context.package_list_handle_to_device_handle[handle] = driver_handle

            # If driver_handle has EFI_DEVICE_PATH_PROTOCOL installed, 
            #   then also add a EFI_PACKAGE_TYPE_DEVICE_PATH package to the new package list
            context = ql.loader.dxe_context

            if driver_handle in context.protocols:
                supported = context.protocols[driver_handle]

                if EFI_DEVICE_PATH_PROTOCOL_GUID in supported:
                    device_path = supported[EFI_DEVICE_PATH_PROTOCOL_GUID]
                    hii_context.add_device_path_package(handle, device_path)

        return EFI_SUCCESS

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "Handle"        : POINTER,  # IN EFI_HII_HANDLE
    })
    def hook_RemovePackageList(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "Handle"        : POINTER,  # IN EFI_HII_HANDLE
        "PackageList"   : POINTER,  # IN CONST PTR(EFI_HII_PACKAGE_LIST_HEADER)
    })
    def hook_UpdatePackageList(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"              : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "PackageType"       : UINT8,    # IN UINT8
        "PackageGuid"       : POINTER,  # IN CONST PTR(EFI_GUID)
        "HandleBufferLength": POINTER,  # IN OUT PTR(UINTN)
        "Handle"            : POINTER,  # OUT PTR(EFI_HII_HANDLE)
    })
    def hook_ListPackageLists(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "Handle"        : POINTER,  # IN EFI_HII_HANDLE
        "BufferSize"    : POINTER,  # IN OUT PTR(UINTN)
        "Buffer"        : POINTER,  # OUT PTR(EFI_HII_PACKAGE_LIST_HEADER)
    })
    def hook_ExportPackageLists(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"          : POINTER,                          # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "PackageType"       : UINT8,                        # IN UINT8
        "PackageGuid"       : POINTER,                      # IN CONST PTR(EFI_GUID)
        "PackageNotifyFn"   : EFI_HII_DATABASE_NOTIFY,      # IN CONST EFI_HII_DATABASE_NOTIFY
        "NotifyType"        : EFI_HII_DATABASE_NOTIFY_TYPE, # IN EFI_HII_DATABASE_NOTIFY_TYPE
        "NotifyHandle"      : POINTER                       # OUT PTR(EFI_HANDLE)
    })
    def hook_RegisterPackageNotify(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"              : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "NotificationHandle": POINTER   # IN EFI_HANDLE
    })
    def hook_UnregisterPackageNotify(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                  : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "KeyGuidBufferLength"   : POINTER,  # IN OUT PTR(UINT16)
        "PackageGuid"           : POINTER,  # IN CONST PTR(EFI_GUID)
        "KeyGuidBuffer"         : POINTER   #  OUT PTR(EFI_GUID)
    })
    def hook_FindKeyboardLayouts(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                  : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "KeyGuid"               : POINTER,  # IN PTR(EFI_GUID)
        "KeyboardLayoutLength"  : POINTER,  # IN OUT PTR(UINT16)
        "KeyboardLayout"        : POINTER,  # OUT PTR(EFI_HII_KEYBOARD_LAYOUT)
    })
    def hook_GetKeyboardLayout(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"                  : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "KeyGuid"               : POINTER,  # IN PTR(EFI_GUID)
    })
    def hook_SetKeyboardLayout(ql: Qiling, address: int, params):
        pass

    @dxeapi(params = {
        "This"              : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
        "PackageListHandle" : POINTER,  # IN EFI_HII_HANDLE
        "DriverHandle"      : POINTER,  # OUT PTR(EFI_HANDLE)
    })
    def hook_GetPackageListHandle(ql: Qiling, address: int, params):
        driver_handle_ptr = params['DriverHandle']
        if driver_handle_ptr == 0:
            return EFI_INVALID_PARAMETER

        # PackageListHandles start at 0x10
        package_list_handle = params['PackageListHandle']
        if package_list_handle < 0x10:
            return EFI_INVALID_PARAMETER
        
        hii_context: HiiContext = ql.loader.context.hii_context
        if package_list_handle not in hii_context.package_list_handle_to_device_handle:
            return EFI_NOT_FOUND
        
        drive_handle = hii_context.package_list_handle_to_device_handle[package_list_handle]
        ql.mem.write_ptr(driver_handle_ptr, drive_handle)
        return EFI_SUCCESS


descriptor = {
    "guid" : "ef9fc172-a1b2-4693-b327-6d32fc416042",
    "struct" : EFI_HII_DATABASE_PROTOCOL,
    "fields" : (
        ("NewPackageList", EFI_HII_DATABASE_PROTOCOL.hook_NewPackageList),
        ("RemovePackageList", EFI_HII_DATABASE_PROTOCOL.hook_RemovePackageList),
        ("UpdatePackageList", EFI_HII_DATABASE_PROTOCOL.hook_UpdatePackageList),
        ("ListPackageLists", EFI_HII_DATABASE_PROTOCOL.hook_ListPackageLists),
        ("ExportPackageLists", EFI_HII_DATABASE_PROTOCOL.hook_ExportPackageLists),
        ("RegisterPackageNotify", EFI_HII_DATABASE_PROTOCOL.hook_RegisterPackageNotify),
        ("UnregisterPackageNotify", EFI_HII_DATABASE_PROTOCOL.hook_UnregisterPackageNotify),
        ("FindKeyboardLayouts", EFI_HII_DATABASE_PROTOCOL.hook_FindKeyboardLayouts),
        ("GetKeyboardLayout", EFI_HII_DATABASE_PROTOCOL.hook_GetKeyboardLayout),
        ("SetKeyboardLayout", EFI_HII_DATABASE_PROTOCOL.hook_SetKeyboardLayout),
        ("GetPackageListHandle", EFI_HII_DATABASE_PROTOCOL.hook_GetPackageListHandle)
    )
}
