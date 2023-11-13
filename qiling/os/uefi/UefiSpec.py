
#!/usr/bin/env python3
#
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

# @see: MdePkg\Include\Uefi\UefiSpec.h

from .ProcessorBind import *
from .UefiBaseType import *
from .UefiMultiPhase import *
from .protocols.EfiLDevicePathProtocol import EFI_DEVICE_PATH_PROTOCOL

# definitions for EFI_TIME.Daylight
EFI_TIME_ADJUST_DAYLIGHT = (1 << 1)
EFI_TIME_IN_DAYLIGHT = (1 << 2)

# definition for EFI_TIME.TimeZone
EFI_UNSPECIFIED_TIMEZONE = 0x07ff


class EFI_ALLOCATE_TYPE(ENUM):
    _members_ = [
        'AllocateAnyPages',
        'AllocateMaxAddress',
        'AllocateAddress',
        'MaxAllocateType'
    ]


class EFI_TIMER_DELAY(ENUM):
    _members_ = [
        'TimerCancel',
        'TimerPeriodic',
        'TimerRelative'
    ]


class EFI_INTERFACE_TYPE(ENUM):
    _members_ = [
        'EFI_NATIVE_INTERFACE'
    ]


class EFI_LOCATE_SEARCH_TYPE(ENUM):
    _members_ = [
        'AllHandles',
        'ByRegisterNotify',
        'ByProtocol'
    ]


class EFI_TIME_CAPABILITIES(STRUCT):
    _pack_ = 8

    _fields_ = [
        ('Resolution',    UINT32),
        ('Accuracy',    UINT32),
        ('SetsToZero',    BOOLEAN),
    ]


class EFI_MEMORY_DESCRIPTOR(STRUCT):
    _pack_ = 8

    _fields_ = [
        ('Type',            UINT32),
        ('PhysicalStart',    EFI_PHYSICAL_ADDRESS),
        ('VirtualStart',    EFI_VIRTUAL_ADDRESS),
        ('NumberOfPages',    UINT64),
        ('Attribute',        UINT64)
    ]


class EFI_CAPSULE_HEADER(STRUCT):
    _fields_ = [
        ('CapsuleGuid',            EFI_GUID),
        ('HeaderSize',            UINT32),
        ('Flags',                UINT32),
        ('CapsuleImageSize',    UINT32)
    ]


EFI_GET_TIME = FUNCPTR(EFI_STATUS, PTR(EFI_TIME), PTR(EFI_TIME_CAPABILITIES))
EFI_SET_TIME = FUNCPTR(EFI_STATUS, PTR(EFI_TIME))
EFI_GET_WAKEUP_TIME = FUNCPTR(EFI_STATUS, PTR(
    BOOLEAN), PTR(BOOLEAN), PTR(EFI_TIME))
EFI_SET_WAKEUP_TIME = FUNCPTR(EFI_STATUS, BOOLEAN, PTR(EFI_TIME))
EFI_SET_VIRTUAL_ADDRESS_MAP = FUNCPTR(
    EFI_STATUS, UINTN, UINTN, UINT32, PTR(EFI_MEMORY_DESCRIPTOR))
EFI_CONVERT_POINTER = FUNCPTR(EFI_STATUS, UINTN, PTR(PTR(VOID)))
EFI_GET_VARIABLE = FUNCPTR(EFI_STATUS, PTR(CHAR16), PTR(
    EFI_GUID), PTR(UINT32), PTR(UINTN), PTR(VOID))
EFI_GET_NEXT_VARIABLE_NAME = FUNCPTR(
    EFI_STATUS, PTR(UINTN), PTR(CHAR16), PTR(EFI_GUID))
EFI_SET_VARIABLE = FUNCPTR(EFI_STATUS, PTR(
    CHAR16), PTR(EFI_GUID), UINT32, UINTN, PTR(VOID))
EFI_GET_NEXT_HIGH_MONO_COUNT = FUNCPTR(EFI_STATUS, PTR(UINT32))
EFI_RESET_SYSTEM = FUNCPTR(VOID, EFI_RESET_TYPE, EFI_STATUS, UINTN, PTR(VOID))
EFI_UPDATE_CAPSULE = FUNCPTR(EFI_STATUS, PTR(
    PTR(EFI_CAPSULE_HEADER)), UINTN, EFI_PHYSICAL_ADDRESS)
EFI_QUERY_CAPSULE_CAPABILITIES = FUNCPTR(EFI_STATUS, PTR(
    PTR(EFI_CAPSULE_HEADER)), UINTN, PTR(UINT64), PTR(EFI_RESET_TYPE))
EFI_QUERY_VARIABLE_INFO = FUNCPTR(
    EFI_STATUS, UINT32, PTR(UINT64), PTR(UINT64), PTR(UINT64))


EFI_EVENT_NOTIFY = FUNCPTR(VOID, EFI_EVENT, PTR(VOID))


class EFI_OPEN_PROTOCOL_INFORMATION_ENTRY(STRUCT):
    _fields_ = [
        ('AgentHandle',        EFI_HANDLE),
        ('ControllerHandle', EFI_HANDLE),
        ('Attributes',        UINT32),
        ('OpenCount',        UINT32)
    ]


EFI_RAISE_TPL = FUNCPTR(EFI_TPL, EFI_TPL)
EFI_RESTORE_TPL = FUNCPTR(VOID, EFI_TPL)
EFI_ALLOCATE_PAGES = FUNCPTR(
    EFI_STATUS, EFI_ALLOCATE_TYPE, EFI_MEMORY_TYPE, UINTN, PTR(EFI_PHYSICAL_ADDRESS))
EFI_FREE_PAGES = FUNCPTR(EFI_STATUS, EFI_PHYSICAL_ADDRESS, UINTN)
EFI_GET_MEMORY_MAP = FUNCPTR(EFI_STATUS, PTR(UINTN), PTR(
    EFI_MEMORY_DESCRIPTOR), PTR(UINTN), PTR(UINTN), PTR(UINT32))
EFI_ALLOCATE_POOL = FUNCPTR(EFI_STATUS, EFI_MEMORY_TYPE, UINTN, PTR(PTR(VOID)))
EFI_FREE_POOL = FUNCPTR(EFI_STATUS, PTR(VOID))
EFI_CREATE_EVENT = FUNCPTR(EFI_STATUS, UINT32, EFI_TPL,
                           EFI_EVENT_NOTIFY, PTR(VOID), PTR(EFI_EVENT))
EFI_SET_TIMER = FUNCPTR(EFI_STATUS, EFI_EVENT, EFI_TIMER_DELAY, UINT64)
EFI_WAIT_FOR_EVENT = FUNCPTR(EFI_STATUS, UINTN, PTR(EFI_EVENT), PTR(UINTN))
EFI_SIGNAL_EVENT = FUNCPTR(EFI_STATUS, EFI_EVENT)
EFI_CLOSE_EVENT = FUNCPTR(EFI_STATUS, EFI_EVENT)
EFI_CHECK_EVENT = FUNCPTR(EFI_STATUS, EFI_EVENT)
EFI_INSTALL_PROTOCOL_INTERFACE = FUNCPTR(EFI_STATUS, PTR(
    EFI_HANDLE), PTR(EFI_GUID), EFI_INTERFACE_TYPE, PTR(VOID))
EFI_REINSTALL_PROTOCOL_INTERFACE = FUNCPTR(
    EFI_STATUS, EFI_HANDLE, PTR(EFI_GUID), PTR(VOID), PTR(VOID))
EFI_UNINSTALL_PROTOCOL_INTERFACE = FUNCPTR(
    EFI_STATUS, EFI_HANDLE, PTR(EFI_GUID), PTR(VOID))
EFI_HANDLE_PROTOCOL = FUNCPTR(
    EFI_STATUS, EFI_HANDLE, PTR(EFI_GUID), PTR(PTR(VOID)))
EFI_REGISTER_PROTOCOL_NOTIFY = FUNCPTR(
    EFI_STATUS, PTR(EFI_GUID), EFI_EVENT, PTR(PTR(VOID)))
EFI_LOCATE_HANDLE = FUNCPTR(EFI_STATUS, EFI_LOCATE_SEARCH_TYPE, PTR(
    EFI_GUID), PTR(VOID), PTR(UINTN), PTR(EFI_HANDLE))
EFI_LOCATE_DEVICE_PATH = FUNCPTR(EFI_STATUS, PTR(EFI_GUID), PTR(
    PTR(EFI_DEVICE_PATH_PROTOCOL)), PTR(EFI_HANDLE))
EFI_INSTALL_CONFIGURATION_TABLE = FUNCPTR(EFI_STATUS, PTR(EFI_GUID), PTR(VOID))
EFI_IMAGE_LOAD = FUNCPTR(EFI_STATUS, BOOLEAN, EFI_HANDLE, PTR(
    EFI_DEVICE_PATH_PROTOCOL), PTR(VOID), UINTN, PTR(EFI_HANDLE))
EFI_IMAGE_START = FUNCPTR(EFI_STATUS, EFI_HANDLE, PTR(UINTN), PTR(PTR(CHAR16)))
EFI_EXIT = FUNCPTR(EFI_STATUS, EFI_HANDLE, EFI_STATUS, UINTN, PTR(CHAR16))
EFI_IMAGE_UNLOAD = FUNCPTR(EFI_STATUS, EFI_HANDLE)
EFI_EXIT_BOOT_SERVICES = FUNCPTR(EFI_STATUS, EFI_HANDLE, UINTN)
EFI_GET_NEXT_MONOTONIC_COUNT = FUNCPTR(EFI_STATUS, PTR(UINT64))
EFI_STALL = FUNCPTR(EFI_STATUS, UINTN)
EFI_SET_WATCHDOG_TIMER = FUNCPTR(EFI_STATUS, UINTN, UINT64, UINTN, PTR(CHAR16))
EFI_CONNECT_CONTROLLER = FUNCPTR(EFI_STATUS, EFI_HANDLE, PTR(
    EFI_HANDLE), PTR(EFI_DEVICE_PATH_PROTOCOL), BOOLEAN)
EFI_DISCONNECT_CONTROLLER = FUNCPTR(
    EFI_STATUS, EFI_HANDLE, EFI_HANDLE, EFI_HANDLE)
EFI_OPEN_PROTOCOL = FUNCPTR(EFI_STATUS, EFI_HANDLE, PTR(
    EFI_GUID), PTR(PTR(VOID)), EFI_HANDLE, EFI_HANDLE, UINT32)
EFI_CLOSE_PROTOCOL = FUNCPTR(
    EFI_STATUS, EFI_HANDLE, PTR(EFI_GUID), EFI_HANDLE, EFI_HANDLE)
EFI_OPEN_PROTOCOL_INFORMATION = FUNCPTR(EFI_STATUS, EFI_HANDLE, PTR(
    EFI_GUID), PTR(PTR(EFI_OPEN_PROTOCOL_INFORMATION_ENTRY)), PTR(UINTN))
EFI_PROTOCOLS_PER_HANDLE = FUNCPTR(
    EFI_STATUS, EFI_HANDLE, PTR(PTR(PTR(EFI_GUID))), PTR(UINTN))
EFI_LOCATE_HANDLE_BUFFER = FUNCPTR(EFI_STATUS, EFI_LOCATE_SEARCH_TYPE, PTR(
    EFI_GUID), PTR(VOID), PTR(UINTN), PTR(PTR(EFI_HANDLE)))
EFI_LOCATE_PROTOCOL = FUNCPTR(EFI_STATUS, PTR(
    EFI_GUID), PTR(VOID), PTR(PTR(VOID)))
# ...
EFI_INSTALL_MULTIPLE_PROTOCOL_INTERFACES = FUNCPTR(EFI_STATUS, PTR(EFI_HANDLE))
# ...
EFI_UNINSTALL_MULTIPLE_PROTOCOL_INTERFACES = FUNCPTR(EFI_STATUS, EFI_HANDLE)
EFI_CALCULATE_CRC32 = FUNCPTR(EFI_STATUS, PTR(VOID), UINTN, PTR(UINT32))
EFI_COPY_MEM = FUNCPTR(VOID, PTR(VOID), PTR(VOID), UINTN)
EFI_SET_MEM = FUNCPTR(VOID, PTR(VOID), UINTN, UINT8)
EFI_CREATE_EVENT_EX = FUNCPTR(EFI_STATUS, UINT32, EFI_TPL, EFI_EVENT_NOTIFY, PTR(
    VOID), PTR(EFI_GUID), PTR(EFI_EVENT))


class EFI_CONFIGURATION_TABLE(STRUCT):
    _fields_ = [
        ('VendorGuid',    EFI_GUID),
        ('VendorTable',    PTR(VOID)),
    ]


# TODO: to be implemented
# @see: MdePkg\Include\Protocol\SimpleTextIn.h
EFI_SIMPLE_TEXT_INPUT_PROTOCOL = STRUCT

# TODO: to be implemented
# @see: MdePkg\Include\Protocol\SimpleTextOut.h
# EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL = STRUCT


# __all__ = [
#     'EFI_TIME_ADJUST_DAYLIGHT',
#     'EFI_TIME_IN_DAYLIGHT',
#     'EFI_UNSPECIFIED_TIMEZONE',
#     'EFI_RUNTIME_SERVICES',
#     'EFI_BOOT_SERVICES',
#     'EFI_CONFIGURATION_TABLE',
#     'EFI_SYSTEM_TABLE',
#     'EFI_ALLOCATE_TYPE',
#     'EFI_INTERFACE_TYPE',
#     'EFI_LOCATE_SEARCH_TYPE',
#     'EFI_OPEN_PROTOCOL_INFORMATION_ENTRY',
#     'EFI_IMAGE_UNLOAD'
# ]
