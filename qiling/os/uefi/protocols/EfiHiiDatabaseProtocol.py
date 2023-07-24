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

EFI_HII_HANDLE = PTR(VOID)

class EFI_HII_PACKAGE_LIST_HEADER(STRUCT):
    _fields_ = [
        ('PackageListGuid',   EFI_GUID),
        ('PackagLength',    UINT32)
    ]

class EFI_HII_PACKAGE_HEADER(STRUCT):
    _fields_ = [
        ('Length', UINT32),
        ('Type', UINT32),
        ('Data', PTR(UINT8))  # Array
    ]

EFI_HII_DATABASE_NOTIFY_TYPE = UINTN

EFI_HII_DATABASE_NOTIFY = FUNCPTR(EFI_STATUS, UINT8, PTR(EFI_GUID), PTR(EFI_HII_PACKAGE_HEADER), EFI_HII_HANDLE, EFI_HII_DATABASE_NOTIFY_TYPE)

class EFI_KEY(ENUM):
    _members_ = [
        'EfiKeyLCtrl', 'EfiKeyA0', 'EfiKeyLAlt', 'EfiKeySpaceBar', 'EfiKeyA2',
        'EfiKeyA3', 'EfiKeyA4', 'EfiKeyRCtrl', 'EfiKeyLeftArrow',
        'EfiKeyDownArrow', 'EfiKeyRightArrow', 'EfiKeyZero', 'EfiKeyPeriod',
        'EfiKeyEnter', 'EfiKeyLShift', 'EfiKeyB0', 'EfiKeyB1', 'EfiKeyB2',
        'EfiKeyB3', 'EfiKeyB4', 'EfiKeyB5', 'EfiKeyB6', 'EfiKeyB7', 'EfiKeyB8',
        'EfiKeyB9', 'EfiKeyB10', 'EfiKeyRShift', 'EfiKeyUpArrow', 'EfiKeyOne',
        'EfiKeyTwo', 'EfiKeyThree', 'EfiKeyCapsLock', 'EfiKeyC1', 'EfiKeyC2',
        'EfiKeyC3', 'EfiKeyC4', 'EfiKeyC5', 'EfiKeyC6', 'EfiKeyC7', 'EfiKeyC8',
        'EfiKeyC9', 'EfiKeyC10', 'EfiKeyC11', 'EfiKeyC12', 'EfiKeyFour',
        'EfiKeyFive', 'EfiKeySix', 'EfiKeyPlus', 'EfiKeyTab', 'EfiKeyD1',
        'EfiKeyD2', 'EfiKeyD3', 'EfiKeyD4', 'EfiKeyD5', 'EfiKeyD6', 'EfiKeyD7',
        'EfiKeyD8', 'EfiKeyD9', 'EfiKeyD10', 'EfiKeyD11', 'EfiKeyD12', 'EfiKeyD13',
        'EfiKeyDel', 'EfiKeyEnd', 'EfiKeyPgDn', 'EfiKeySeven', 'EfiKeyEight',
        'EfiKeyNine', 'EfiKeyE0', 'EfiKeyE1', 'EfiKeyE2', 'EfiKeyE3', 'EfiKeyE4',
        'EfiKeyE5', 'EfiKeyE6', 'EfiKeyE7', 'EfiKeyE8', 'EfiKeyE9', 'EfiKeyE10',
        'EfiKeyE11', 'EfiKeyE12', 'EfiKeyBackSpace', 'EfiKeyIns', 'EfiKeyHome',
        'EfiKeyPgUp', 'EfiKeyNLck', 'EfiKeySlash', 'EfiKeyAsterisk',
        'EfiKeyMinus', 'EfiKeyEsc', 'EfiKeyF1', 'EfiKeyF2', 'EfiKeyF3', 'EfiKeyF4',
        'EfiKeyF5', 'EfiKeyF6', 'EfiKeyF7', 'EfiKeyF8', 'EfiKeyF9', 'EfiKeyF10',
        'EfiKeyF11', 'EfiKeyF12', 'EfiKeyPrint', 'EfiKeySLck', 'EfiKeyPause',
        'EfiKeyIntl0', 'EfiKeyIntl1', 'EfiKeyIntl2', 'EfiKeyIntl3',
        'EfiKeyIntl4', 'EfiKeyIntl5', 'EfiKeyIntl6', 'EfiKeyIntl7',
        'EfiKeyIntl8', 'EfiKeyIntl9'
    ]

class EFI_KEY_DESCRIPTOR(STRUCT):
    _fields_ = [
        ('Key', EFI_KEY),
        ('Unicode', CHAR16),
        ('ShiftedUnicode', CHAR16),
        ('AltGrUnicode', CHAR16),
        ('ShiftedAltGrUnicode', CHAR16),
        ('Modifier', UINT16),
        ('AffectedAttribute', UINT16),
    ]

class EFI_HII_KEYBOARD_LAYOUT(STRUCT):
    _fields_ = [
        ('LayoutLength', UINT16),
        ('Guid', EFI_GUID),
        ('LayoutDescriptorStringOffset', UINT32),
        ('DescriptorCount', UINT8),
        ('Descriptors', PTR(EFI_KEY_DESCRIPTOR))  # Array
    ]


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
    "This"          : POINTER,  # IN CONST PTR(EFI_HII_DATABASE_PROTOCOL)
    "PackageList"   : POINTER,  # IN CONST PTR(EFI_HII_PACKAGE_LIST_HEADER)
    "DriverHandle"  : POINTER,  # IN CONST EFI_HANDLE
    "Handle"        : POINTER,  # OUT PTR(EFI_HII_HANDLE)
})
def hook_NewPackageList(ql: Qiling, address: int, params):
    pass

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
    pass

descriptor = {
    "guid" : "ef9fc172-a1b2-4693-b327-6d32fc416042",
    "struct" : EFI_HII_DATABASE_PROTOCOL,
    "fields" : (
        ("NewPackageList", hook_NewPackageList),
        ("RemovePackageList", hook_RemovePackageList),
        ("UpdatePackageList", hook_UpdatePackageList),
        ("ListPackageLists", hook_ListPackageLists),
        ("ExportPackageLists", hook_ExportPackageLists),
        ("RegisterPackageNotify", hook_RegisterPackageNotify),
        ("UnregisterPackageNotify", hook_UnregisterPackageNotify),
        ("FindKeyboardLayouts", hook_FindKeyboardLayouts),
        ("GetKeyboardLayout", hook_GetKeyboardLayout),
        ("SetKeyboardLayout", hook_SetKeyboardLayout),
        ("GetPackageListHandle", hook_GetPackageListHandle)
    )
}
