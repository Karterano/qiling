#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import time

from qiling import Qiling
from qiling.os.const import *
from .const import *
from .utils import *
from .fncc import *
from .ProcessorBind import *
from .UefiBaseType import EFI_TIME
from .UefiSpec import *

class EFI_RUNTIME_SERVICES(STRUCT):
    _fields_ = [
        ('Hdr',                            EFI_TABLE_HEADER),
        ('GetTime',                        EFI_GET_TIME),
        ('SetTime',                        EFI_SET_TIME),
        ('GetWakeupTime',                EFI_GET_WAKEUP_TIME),
        ('SetWakeupTime',                EFI_SET_WAKEUP_TIME),
        ('SetVirtualAddressMap',        EFI_SET_VIRTUAL_ADDRESS_MAP),
        ('ConvertPointer',                EFI_CONVERT_POINTER),
        ('GetVariable',                    EFI_GET_VARIABLE),
        ('GetNextVariableName',            EFI_GET_NEXT_VARIABLE_NAME),
        ('SetVariable',                    EFI_SET_VARIABLE),
        ('GetNextHighMonotonicCount',    EFI_GET_NEXT_HIGH_MONO_COUNT),
        ('ResetSystem',                    EFI_RESET_SYSTEM),
        ('UpdateCapsule',                EFI_UPDATE_CAPSULE),
        ('QueryCapsuleCapabilities',    EFI_QUERY_CAPSULE_CAPABILITIES),
        ('QueryVariableInfo',            EFI_QUERY_VARIABLE_INFO)
    ]

    @dxeapi(params={
        "Time"            : POINTER,    # OUT PTR(EFI_TIME)
        "Capabilities"    : POINTER    # OUT PTR(EFI_TIME_CAPABILITIES)
    })
    def hook_GetTime(ql: Qiling, address: int, params):
        Time = params['Time']

        if not Time:
            return EFI_INVALID_PARAMETER

        localtime = time.localtime()

        efitime = EFI_TIME()
        efitime.Year = localtime.tm_year
        efitime.Month = localtime.tm_mon
        efitime.Day = localtime.tm_mday
        efitime.Hour = localtime.tm_hour
        efitime.Minute = localtime.tm_min
        efitime.Second = localtime.tm_sec
        efitime.Nanosecond = 0

        # tz and dst settings are stored in the "RtcTimeSettings" nvram variable.
        # we just use the default settings instead
        efitime.TimeZone = EFI_UNSPECIFIED_TIMEZONE
        efitime.Daylight = 0

        efitime.saveTo(ql, Time)

        return EFI_SUCCESS

    @dxeapi(params={
        "Time": POINTER    # IN PTR(EFI_TIME)
    })
    def hook_SetTime(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params={
        "Enabled"    : POINTER,    # OUT PTR(BOOLEAN)
        "Pending"    : POINTER,    # OUT PTR(BOOLEAN)
        "Time"        : POINTER    # OUT PTR(EFI_TIME)
    })
    def hook_GetWakeupTime(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params={
        "Enable": BOOL,        # BOOLEAN
        "Time"    : POINTER    # PTR(EFI_TIME)
    })
    def hook_SetWakeupTime(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params={
        "MemoryMapSize"        : UINT,        # UINTN
        "DescriptorSize"    : UINT,        # UINTN
        "DescriptorVersion"    : UINT,        # UINT32
        "VirtualMap"        : POINTER    # PTR(EFI_MEMORY_DESCRIPTOR)
    })
    def hook_SetVirtualAddressMap(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params={
        "DebugDisposition"    : UINT,        # UINTN
        "Address"            : POINTER    # OUT PTR(PTR(VOID))
    })
    def hook_ConvertPointer(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params={
        "VariableName"    : WSTRING,    # PTR(CHAR16)
        "VendorGuid"    : GUID,        # PTR(EFI_GUID)
        "Attributes"    : POINTER,    # OUT PTR(UINT32)
        "DataSize"        : POINTER,    # IN OUT PTR(UINTN)
        "Data"            : POINTER    # OUT PTR(VOID)
    })
    def hook_GetVariable(ql: Qiling, address: int, params):
        name = params['VariableName']

        if name in ql.env:
            var = ql.env[name]
            read_len = read_int64(ql, params['DataSize'])

            if params['Attributes'] != 0:
                write_int64(ql, params['Attributes'], 0)

            write_int64(ql, params['DataSize'], len(var))

            if read_len < len(var):
                return EFI_BUFFER_TOO_SMALL

            if params['Data'] != 0:
                ql.mem.write(params['Data'], var)

            return EFI_SUCCESS

        ql.log.warning(f'variable with name {name} not found')

        return EFI_NOT_FOUND

    @dxeapi(params={
        "VariableNameSize"    : POINTER,    # IN OUT PTR(UINTN)
        "VariableName"        : POINTER,    # IN OUT PTR(CHAR16)
        "VendorGuid"        : GUID        # IN OUT PTR(EFI_GUID)
    })
    def hook_GetNextVariableName(ql: Qiling, address: int, params):
        var_name_size = params["VariableNameSize"]
        var_name = params["VariableName"]

        if (var_name_size == 0) or (var_name == 0):
            return EFI_INVALID_PARAMETER

        name_size = read_int64(ql, var_name_size)
        last_name = ql.os.utils.read_wstring(var_name)

        vars = ql.env['Names'] # This is a list of variable names in correct order.

        if last_name not in vars:
            return EFI_NOT_FOUND

        idx = vars.index(last_name)

        # make sure it is not the last one (i.e. we have a next one to pull)
        if idx == len(vars) - 1:
            return EFI_NOT_FOUND

        # get next var name, and add null terminator
        new_name = vars[idx + 1] + '\x00'

        # turn it into a wide string
        new_name = ''.join(f'{c}\x00' for c in new_name)

        if len(new_name) > name_size:
            write_int64(ql, var_name_size, len(new_name))
            return EFI_BUFFER_TOO_SMALL

        ql.mem.write(var_name, new_name.encode('ascii'))

        return EFI_SUCCESS

    @dxeapi(params={
        "VariableName"    : WSTRING,    # PTR(CHAR16)
        "VendorGuid"    : GUID,        # PTR(EFI_GUID)
        "Attributes"    : UINT,        # UINT32
        "DataSize"        : UINT,        # UINTN
        "Data"            : POINTER    # PTR(VOID)
    })
    def hook_SetVariable(ql: Qiling, address: int, params):
        ql.env[params['VariableName']] = bytes(ql.mem.read(params['Data'], params['DataSize']))
        return EFI_SUCCESS

    @dxeapi(params={
        "HighCount": POINTER    # OUT PTR(UINT32)
    })
    def hook_GetNextHighMonotonicCount(ql: Qiling, address: int, params):
        ql.os.monotonic_count += 0x0000000100000000
        hmc = ql.os.monotonic_count
        hmc = (hmc >> 32) & 0xffffffff
        write_int32(ql, params["HighCount"], hmc)
        return EFI_SUCCESS

    @dxeapi(params={
        "ResetType"        : INT,        # EFI_RESET_TYPE
        "ResetStatus"    : INT,        # EFI_STATUS
        "DataSize"        : UINT,        # UINTN
        "ResetData"        : POINTER    # PTR(VOID)
    })
    def hook_ResetSystem(ql: Qiling, address: int, params):
        ql.emu_stop()

        return EFI_SUCCESS

    @dxeapi(params={
        "CapsuleHeaderArray": POINTER,    # PTR(PTR(EFI_CAPSULE_HEADER))
        "CapsuleCount"        : UINT,        # UINTN
        "ScatterGatherList"    : ULONGLONG    # EFI_PHYSICAL_ADDRESS
    })
    def hook_UpdateCapsule(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params={
        "CapsuleHeaderArray": POINTER,    # PTR(PTR(EFI_CAPSULE_HEADER))
        "CapsuleCount"        : UINT,        # UINTN
        "MaximumCapsuleSize": POINTER,    # OUT PTR(UINT64)
        "ResetType"            : POINTER    # OUT PTR(EFI_RESET_TYPE)
    })
    def hook_QueryCapsuleCapabilities(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params={
        "Attributes"                    : UINT,        # UINT32
        "MaximumVariableStorageSize"    : POINTER,    # OUT PTR(UINT64)
        "RemainingVariableStorageSize"    : POINTER,    # OUT PTR(UINT64)
        "MaximumVariableSize"            : POINTER    # OUT PTR(UINT64)
    })
    def hook_QueryVariableInfo(ql: Qiling, address: int, params):
        return EFI_SUCCESS

descriptor = {
        'struct' : EFI_RUNTIME_SERVICES,
        'fields' : (
            ('Hdr',                            None),
            ('GetTime',                        EFI_RUNTIME_SERVICES.hook_GetTime),
            ('SetTime',                        EFI_RUNTIME_SERVICES.hook_SetTime),
            ('GetWakeupTime',                EFI_RUNTIME_SERVICES.hook_GetWakeupTime),
            ('SetWakeupTime',                EFI_RUNTIME_SERVICES.hook_SetWakeupTime),
            ('SetVirtualAddressMap',        EFI_RUNTIME_SERVICES.hook_SetVirtualAddressMap),
            ('ConvertPointer',                EFI_RUNTIME_SERVICES.hook_ConvertPointer),
            ('GetVariable',                    EFI_RUNTIME_SERVICES.hook_GetVariable),
            ('GetNextVariableName',            EFI_RUNTIME_SERVICES.hook_GetNextVariableName),
            ('SetVariable',                    EFI_RUNTIME_SERVICES.hook_SetVariable),
            ('GetNextHighMonotonicCount',    EFI_RUNTIME_SERVICES.hook_GetNextHighMonotonicCount),
            ('ResetSystem',                    EFI_RUNTIME_SERVICES.hook_ResetSystem),
            ('UpdateCapsule',                EFI_RUNTIME_SERVICES.hook_UpdateCapsule),
            ('QueryCapsuleCapabilities',    EFI_RUNTIME_SERVICES.hook_QueryCapsuleCapabilities),
            ('QueryVariableInfo',            EFI_RUNTIME_SERVICES.hook_QueryVariableInfo)
        )
    }
