#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

from binascii import crc32

from qiling.os.const import *
from qiling.os.uefi import guids_db
from qiling.os.uefi.ProcessorBind import STRUCT
from qiling.os.uefi.const import *
from qiling.os.uefi.fncc import dxeapi
from qiling.os.uefi.utils import *
from qiling.os.uefi.UefiSpec import *
from qiling.os.uefi.protocols import common

class EFI_BOOT_SERVICES(STRUCT):
    _fields_ = [
        ('Hdr',                            EFI_TABLE_HEADER),
        ('RaiseTPL',                    EFI_RAISE_TPL),
        ('RestoreTPL',                    EFI_RESTORE_TPL),
        ('AllocatePages',                EFI_ALLOCATE_PAGES),
        ('FreePages',                    EFI_FREE_PAGES),
        ('GetMemoryMap',                EFI_GET_MEMORY_MAP),
        ('AllocatePool',                EFI_ALLOCATE_POOL),
        ('FreePool',                    EFI_FREE_POOL),
        ('CreateEvent',                    EFI_CREATE_EVENT),
        ('SetTimer',                    EFI_SET_TIMER),
        ('WaitForEvent',                EFI_WAIT_FOR_EVENT),
        ('SignalEvent',                    EFI_SIGNAL_EVENT),
        ('CloseEvent',                    EFI_CLOSE_EVENT),
        ('CheckEvent',                    EFI_CHECK_EVENT),
        ('InstallProtocolInterface',    EFI_INSTALL_PROTOCOL_INTERFACE),
        ('ReinstallProtocolInterface',    EFI_REINSTALL_PROTOCOL_INTERFACE),
        ('UninstallProtocolInterface',    EFI_UNINSTALL_PROTOCOL_INTERFACE),
        ('HandleProtocol',                EFI_HANDLE_PROTOCOL),
        ('Reserved',                    PTR(VOID)),
        ('RegisterProtocolNotify',        EFI_REGISTER_PROTOCOL_NOTIFY),
        ('LocateHandle',                EFI_LOCATE_HANDLE),
        ('LocateDevicePath',            EFI_LOCATE_DEVICE_PATH),
        ('InstallConfigurationTable',    EFI_INSTALL_CONFIGURATION_TABLE),
        ('LoadImage',                    EFI_IMAGE_LOAD),
        ('StartImage',                    EFI_IMAGE_START),
        ('Exit',                        EFI_EXIT),
        ('UnloadImage',                    EFI_IMAGE_UNLOAD),
        ('ExitBootServices',            EFI_EXIT_BOOT_SERVICES),
        ('GetNextMonotonicCount',        EFI_GET_NEXT_MONOTONIC_COUNT),
        ('Stall',                        EFI_STALL),
        ('SetWatchdogTimer',            EFI_SET_WATCHDOG_TIMER),
        ('ConnectController',            EFI_CONNECT_CONTROLLER),
        ('DisconnectController',        EFI_DISCONNECT_CONTROLLER),
        ('OpenProtocol',                EFI_OPEN_PROTOCOL),
        ('CloseProtocol',                EFI_CLOSE_PROTOCOL),
        ('OpenProtocolInformation',        EFI_OPEN_PROTOCOL_INFORMATION),
        ('ProtocolsPerHandle',            EFI_PROTOCOLS_PER_HANDLE),
        ('LocateHandleBuffer',            EFI_LOCATE_HANDLE_BUFFER),
        ('LocateProtocol',                EFI_LOCATE_PROTOCOL),
        ('InstallMultipleProtocolInterfaces',
         EFI_INSTALL_MULTIPLE_PROTOCOL_INTERFACES),
        ('UninstallMultipleProtocolInterfaces',
         EFI_UNINSTALL_MULTIPLE_PROTOCOL_INTERFACES),
        ('CalculateCrc32',                EFI_CALCULATE_CRC32),
        ('CopyMem',                        EFI_COPY_MEM),
        ('SetMem',                        EFI_SET_MEM),
        ('CreateEventEx',                EFI_CREATE_EVENT_EX)
    ]

    @dxeapi(params = {
        "NewTpl" : ULONGLONG        # EFI_TPL
    })
    def hook_RaiseTPL(ql: Qiling, address: int, params):
        prev_tpl = ql.loader.tpl
        ql.loader.tpl = params["NewTpl"]

        return prev_tpl

    @dxeapi(params = {
        "OldTpl": ULONGLONG            # EFI_TPL
    })
    def hook_RestoreTPL(ql: Qiling, address: int, params):
        ql.loader.tpl = params["OldTpl"]

    @dxeapi(params = {
        "type"        : INT,            # EFI_ALLOCATE_TYPE
        "MemoryType": INT,            # EFI_MEMORY_TYPE
        "Pages"        : ULONGLONG,    # UINTN
        "Memory"    : POINTER        # PTR(EFI_PHYSICAL_ADDRESS)
    })
    def hook_AllocatePages(ql: Qiling, address: int, params):
        alloc_size = params["Pages"] * PAGE_SIZE

        if params['type'] == EFI_ALLOCATE_TYPE.AllocateAddress:
            address = read_int64(ql, params["Memory"])

            # TODO: check the range [address, address + alloc_size] is available first
            ql.mem.map(address, alloc_size)
        else:
            # TODO: allocate memory according to 'MemoryType'
            address = ql.loader.dxe_context.heap.alloc(alloc_size)

            if address == 0:
                return EFI_OUT_OF_RESOURCES

            write_int64(ql, params["Memory"], address)

        return EFI_SUCCESS

    @dxeapi(params = {
        "Memory"    : ULONGLONG,    # EFI_PHYSICAL_ADDRESS
        "Pages"        : ULONGLONG        # UINTN
    })
    def hook_FreePages(ql: Qiling, address: int, params):
        address = params["Memory"]

        ret = ql.loader.dxe_context.heap.free(address)

        return EFI_SUCCESS if ret else EFI_INVALID_PARAMETER

    @dxeapi(params = {
        "MemoryMapSize"        : POINTER,    # PTR(UINTN)
        "MemoryMap"            : POINTER,    # PTR(EFI_MEMORY_DESCRIPTOR)
        "MapKey"            : POINTER,    # PTR(UINTN)
        "DescriptorSize"    : POINTER,    # PTR(UINTN)
        "DescriptorVersion"    : POINTER    # PTR(UINT32)
    })
    def hook_GetMemoryMap(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "PoolType"    : INT,        # EFI_MEMORY_TYPE
        "Size"        : INT,        # UINTN
        "Buffer"    : POINTER    # PTR(PTR(VOID))
    })
    def hook_AllocatePool(ql: Qiling, address: int, params):
        # TODO: allocate memory acording to "PoolType"
        Size = params["Size"]
        Buffer = params["Buffer"]

        address = ql.loader.dxe_context.heap.alloc(Size)
        write_int64(ql, Buffer, address)

        return EFI_SUCCESS if address else EFI_OUT_OF_RESOURCES

    @dxeapi(params = {
        "Buffer": POINTER # PTR(VOID)
    })
    def hook_FreePool(ql: Qiling, address: int, params):
        Buffer = params["Buffer"]

        ret = ql.loader.dxe_context.heap.free(Buffer)

        return EFI_SUCCESS if ret else EFI_INVALID_PARAMETER

    @dxeapi(params = {
        "Type"            : UINT,        # UINT32
        "NotifyTpl"        : UINT,        # EFI_TPL
        "NotifyFunction": POINTER,    # EFI_EVENT_NOTIFY
        "NotifyContext"    : POINTER,    # PTR(VOID)
        "Event"            : POINTER    # PTR(EFI_EVENT)
    })
    def hook_CreateEvent(ql: Qiling, address: int, params):
        return CreateEvent(ql, params)

    @dxeapi(params = {
        "Event"            : POINTER,        # EFI_EVENT
        "Type"            : ULONGLONG,    # EFI_TIMER_DELAY
        "TriggerTime"    : ULONGLONG        # UINT64
    })
    def hook_SetTimer(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "NumberOfEvents": ULONGLONG,    # UINTN
        "Event"            : POINTER,        # PTR(EFI_EVENT)
        "Index"            : POINTER,        # PTR(UINTN)
    })
    def hook_WaitForEvent(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "Event": POINTER # EFI_EVENT
    })
    def hook_SignalEvent(ql: Qiling, address: int, params):
        event_id = params["Event"]

        if event_id not in ql.loader.events:
            return EFI_INVALID_PARAMETER

        signal_event(ql, event_id)

        return EFI_SUCCESS

    @dxeapi(params = {
        "Event": POINTER # EFI_EVENT
    })
    def hook_CloseEvent(ql: Qiling, address: int, params):
        event_id = params["Event"]

        if event_id not in ql.loader.events:
            return EFI_INVALID_PARAMETER

        del ql.loader.events[event_id]

        return EFI_SUCCESS

    @dxeapi(params = {
        "Event": POINTER # EFI_EVENT
    })
    def hook_CheckEvent(ql: Qiling, address: int, params):
        event_id = params["Event"]

        return EFI_SUCCESS if ql.loader.events[event_id]["Set"] else EFI_NOT_READY

    @dxeapi(params = {
        "Handle"        : POINTER,        # PTR(EFI_HANDLE)
        "Protocol"        : GUID,            # PTR(EFI_GUID)
        "InterfaceType"    : ULONGLONG,    # EFI_INTERFACE_TYPE
        "Interface"        : POINTER,        # PTR(VOID)
    })
    def hook_InstallProtocolInterface(ql: Qiling, address: int, params):
        return common.InstallProtocolInterface(ql.loader.dxe_context, params)

    @dxeapi(params = {
        "Handle"        : POINTER,    # EFI_HANDLE
        "Protocol"        : GUID,        # PTR(EFI_GUID)
        "OldInterface"    : POINTER,    # PTR(VOID)
        "NewInterface"    : POINTER    # PTR(VOID)
    })
    def hook_ReinstallProtocolInterface(ql: Qiling, address: int, params):
        handle = params["Handle"]

        if handle not in ql.loader.dxe_context.protocols:
            return EFI_NOT_FOUND

        dic = ql.loader.dxe_context.protocols[handle]
        protocol = params["Protocol"]

        if protocol not in dic:
            return EFI_NOT_FOUND

        dic[protocol] = params["NewInterface"]

        return EFI_SUCCESS

    @dxeapi(params = {
        "Handle"    : POINTER,    # EFI_HANDLE
        "Protocol"    : GUID,        # PTR(EFI_GUID)
        "Interface"    : POINTER    # PTR(VOID)
    })
    def hook_UninstallProtocolInterface(ql: Qiling, address: int, params):
        return common.UninstallProtocolInterface(ql.loader.dxe_context, params)

    @dxeapi(params = {
        "Handle"    : POINTER,    # EFI_HANDLE
        "Protocol"    : GUID,        # PTR(EFI_GUID)
        "Interface"    : POINTER    # PTR(PTR(VOID))
    })
    def hook_HandleProtocol(ql: Qiling, address: int, params):
        return common.HandleProtocol(ql.loader.dxe_context, params)

    @dxeapi(params = {
        "Protocol"        : GUID,        # PTR(EFI_GUID)
        "Event"            : POINTER,    # EFI_EVENT
        "Registration"    : POINTER    # PTR(PTR(VOID))
    })
    def hook_RegisterProtocolNotify(ql: Qiling, address: int, params):
        event = params['Event']
        proto = params["Protocol"]

        if event in ql.loader.events:
            ql.loader.events[event]['Guid'] = proto

            return EFI_SUCCESS

        return EFI_INVALID_PARAMETER

    @dxeapi(params = {
        "SearchType": INT,        # EFI_LOCATE_SEARCH_TYPE
        "Protocol"    : GUID,        # PTR(EFI_GUID)
        "SearchKey"    : POINTER,    # PTR(VOID)
        "BufferSize": POINTER,    # PTR(UINTN)
        "Buffer"    : POINTER    # PTR(EFI_HANDLE)
    })
    def hook_LocateHandle(ql: Qiling, address: int, params):
        return common.LocateHandle(ql.loader.dxe_context, params)

    @dxeapi(params = {
        "Protocol"    : GUID,        # PTR(EFI_GUID)
        "DevicePath": POINTER,    # PTR(PTR(EFI_DEVICE_PATH_PROTOCOL))
        "Device"    : POINTER    # PTR(EFI_HANDLE)
    })
    def hook_LocateDevicePath(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "Guid"    : GUID,        # PTR(EFI_GUID)
        "Table"    : POINTER    # PTR(VOID)
    })
    def hook_InstallConfigurationTable(ql: Qiling, address: int, params):
        return common.InstallConfigurationTable(ql.loader.dxe_context, params)

    @dxeapi(params = {
        "BootPolicy"        : BOOL,            # BOOLEAN
        "ParentImageHandle"    : POINTER,        # EFI_HANDLE
        "DevicePath"        : POINTER,        # PTR(EFI_DEVICE_PATH_PROTOCOL)
        "SourceBuffer"        : POINTER,        # PTR(VOID)
        "SourceSize"        : ULONGLONG,    # UINTN
        "ImageHandle"        : POINTER        # PTR(EFI_HANDLE)
    })
    def hook_LoadImage(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "ImageHandle"    : POINTER,    # EFI_HANDLE
        "ExitDataSize"    : POINTER,    # PTR(UINTN)
        "ExitData"        : POINTER    # PTR(PTR(CHAR16))
    })
    def hook_StartImage(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "ImageHandle"    : POINTER,        # EFI_HANDLE
        "ExitStatus"    : ULONGLONG,    # EFI_STATUS
        "ExitDataSize"    : ULONGLONG,    # UINTN
        "ExitData"        : POINTER        # PTR(CHAR16)
    })
    def hook_Exit(ql: Qiling, address: int, params):
        ql.emu_stop()

        return EFI_SUCCESS

    @dxeapi(params = {
        "ImageHandle" : POINTER # EFI_HANDLE
    })
    def hook_UnloadImage(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "ImageHandle"    : POINTER,    # EFI_HANDLE
        "MapKey"        : ULONGLONG    # UINTN
    })
    def hook_ExitBootServices(ql: Qiling, address: int, params):
        ql.emu_stop()

        # TODO: cleanup BS tableas and data, and notify signal list gEfiEventExitBootServicesGuid
        # @see: MdeModulePkg\Core\Dxe\DxeMain\DxeMain.c, CoreExitBootServices

        return EFI_SUCCESS

    @dxeapi(params = {
        "Count": POINTER # PTR(UINT64)
    })
    def hook_GetNextMonotonicCount(ql: Qiling, address: int, params):
        out = params["Count"]

        ql.os.monotonic_count += 1
        write_int64(ql, out, ql.os.monotonic_count)

        return EFI_SUCCESS

    @dxeapi(params = {
        "Microseconds": ULONGLONG # UINTN
    })
    def hook_Stall(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "Timeout"        : ULONGLONG,    # UINTN
        "WatchdogCode"    : ULONGLONG,    # UINT64
        "DataSize"        : ULONGLONG,    # UINTN
        "WatchdogData"    : POINTER        # PTR(CHAR16)
    })
    def hook_SetWatchdogTimer(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "ControllerHandle"        : POINTER,    # EFI_HANDLE
        "DriverImageHandle"        : POINTER,    #PTR(EFI_HANDLE)
        "RemainingDevicePath"    : POINTER,    # PTR(EFI_DEVICE_PATH_PROTOCOL)
        "Recursive"                : BOOL        # BOOLEAN
    })
    def hook_ConnectController(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "ControllerHandle"    : POINTER,    # EFI_HANDLE
        "DriverImageHandle"    : POINTER,    # EFI_HANDLE
        "ChildHandle"        : POINTER    # EFI_HANDLE
    })
    def hook_DisconnectController(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "Handle"            : POINTER,    # EFI_HANDLE
        "Protocol"            : GUID,        # PTR(EFI_GUID)
        "Interface"            : POINTER,    # PTR(PTR(VOID))
        "AgentHandle"        : POINTER,    # EFI_HANDLE
        "ControllerHandle"    : POINTER,    # EFI_HANDLE
        "Attributes"        : UINT        # UINT32
    })
    def hook_OpenProtocol(ql: Qiling, address: int, params):
        return common.LocateProtocol(ql.loader.dxe_context, params)

    @dxeapi(params = {
        "Handle"            : POINTER,    # EFI_HANDLE
        "Protocol"            : GUID,        # PTR(EFI_GUID)
        "AgentHandle"        : POINTER,    # EFI_HANDLE
        "ControllerHandle"    : POINTER    # EFI_HANDLE
    })
    def hook_CloseProtocol(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "Handle"        : POINTER,    # EFI_HANDLE
        "Protocol"        : GUID,        # PTR(EFI_GUID)
        "EntryBuffer"    : POINTER,    # PTR(PTR(EFI_OPEN_PROTOCOL_INFORMATION_ENTRY))
        "EntryCount"    : POINTER    # PTR(UINTN)
    })
    def hook_OpenProtocolInformation(ql: Qiling, address: int, params):
        return EFI_NOT_FOUND

    @dxeapi(params = {
        "Handle"                : POINTER,    # EFI_HANDLE
        "ProtocolBuffer"        : POINTER,    # PTR(PTR(PTR(EFI_GUID)))
        "ProtocolBufferCount"    : POINTER    # PTR(UINTN)
    })
    def hook_ProtocolsPerHandle(ql: Qiling, address: int, params):
        return EFI_SUCCESS

    @dxeapi(params = {
        "SearchType": INT,        # EFI_LOCATE_SEARCH_TYPE
        "Protocol"    : GUID,        # PTR(EFI_GUID)
        "SearchKey"    : POINTER,    # PTR(VOID)
        "NoHandles"    : POINTER,    # PTR(UINTN)
        "Buffer"    : POINTER    # PTR(PTR(EFI_HANDLE))
    })
    def hook_LocateHandleBuffer(ql: Qiling, address: int, params):
        buffer_size, handles = common.LocateHandles(ql.loader.dxe_context, params)
        write_int64(ql, params["NoHandles"], len(handles))

        if len(handles) == 0:
            return EFI_NOT_FOUND

        address = ql.loader.dxe_context.heap.alloc(buffer_size)
        write_int64(ql, params["Buffer"], address)

        if address == 0:
            return EFI_OUT_OF_RESOURCES

        for handle in handles:
            write_int64(ql, address, handle)
            address += ql.arch.pointersize

        return EFI_SUCCESS

    @dxeapi(params = {
        "Protocol"        : GUID,        # PTR(EFI_GUID)
        "Registration"    : POINTER,    # PTR(VOID)
        "Interface"        : POINTER    # PTR(PTR(VOID))
    })
    def hook_LocateProtocol(ql: Qiling, address: int, params):
        return common.LocateProtocol(ql.loader.dxe_context, params)

    @dxeapi(params = {
        "Handle" : POINTER # PTR(EFI_HANDLE)
        # ...
    })
    def hook_InstallMultipleProtocolInterfaces(ql: Qiling, address: int, params):
        handle = read_int64(ql, params["Handle"])

        if handle == 0:
            handle = ql.loader.dxe_context.heap.alloc(ql.arch.pointersize)

        dic = ql.loader.dxe_context.protocols.get(handle, {})

        # process elipsiss arguments
        index = 1
        while ql.os.fcall.cc.getRawParam(index) != 0:
            GUID_ptr = ql.os.fcall.cc.getRawParam(index)
            protocol_ptr = ql.os.fcall.cc.getRawParam(index + 1)

            GUID = str(ql.os.utils.read_guid(GUID_ptr))
            dic[GUID] = protocol_ptr

            ql.log.info(f'Installing protocol interface {guids_db.get(GUID.upper(), GUID)} to {protocol_ptr:#x}')
            index += 2

        ql.loader.dxe_context.protocols[handle] = dic
        execute_protocol_notifications(ql, True)
        write_int64(ql, params["Handle"], handle)

        return EFI_SUCCESS

    @dxeapi(params = {
        "Handle" : POINTER # EFI_HANDLE
        # ...
    })
    def hook_UninstallMultipleProtocolInterfaces(ql: Qiling, address: int, params):
        handle = params["Handle"]

        if handle not in ql.loader.dxe_context.protocols:
            return EFI_NOT_FOUND

        dic = ql.loader.dxe_context.protocols[handle]

        # process elipsiss arguments
        index = 1
        while ql.os.fcall.cc.getRawParam(index) != 0:
            GUID_ptr = ql.os.fcall.cc.getRawParam(index)
            protocol_ptr = ql.os.fcall.cc.getRawParam(index + 1)

            GUID = str(ql.os.utils.read_guid(GUID_ptr))

            if GUID not in dic:
                return EFI_INVALID_PARAMETER

            del dic[GUID]

            ql.log.info(f'Uninstalling protocol interface {guids_db.get(GUID.upper(), GUID)} from {protocol_ptr:#x}')
            index += 2

        return EFI_SUCCESS

    @dxeapi(params = {
        "Data"        : POINTER,        # PTR(VOID)
        "DataSize"    : ULONGLONG,    # UINTN
        "Crc32"        : POINTER        # PTR(UINT32)
    })
    def hook_CalculateCrc32(ql: Qiling, address: int, params):
        data = bytes(ql.mem.read(params['Data'], params['DataSize']))
        write_int32(ql, params['Crc32'], crc32(data))

        return EFI_SUCCESS

    @dxeapi(params = {
        "Destination"    : POINTER,    # PTR(VOID)
        "Source"        : POINTER,    # PTR(VOID)
        "Length"        : SIZE_T    # UINTN
    })
    def hook_CopyMem(ql: Qiling, address: int, params):
        dst = params["Destination"]
        src = params["Source"]
        length = params["Length"]

        ql.mem.write(dst, bytes(ql.mem.read(src, length)))

    @dxeapi(params = {
        "Buffer": POINTER,    # PTR(VOID)
        "Size"    : SIZE_T,    # UINTN
        "Value"    : BYTE        # UINT8
    })
    def hook_SetMem(ql: Qiling, address: int, params):
        buffer = params["Buffer"]
        value: int = params["Value"] & 0xff
        size = params["Size"]

        ql.mem.write(buffer, bytes([value]) * size)

    @dxeapi(params = {
        "Type"            : UINT,        # UINT32
        "NotifyTpl"        : ULONGLONG,# EFI_TPL
        "NotifyFunction": POINTER,    # EFI_EVENT_NOTIFY
        "NotifyContext"    : POINTER,    # PTR(VOID)
        "EventGroup"    : GUID,        # PTR(EFI_GUID)
        "Event"            : POINTER    # PTR(EFI_EVENT)
    })
    def hook_CreateEventEx(ql: Qiling, address: int, params):
        return CreateEvent(ql, params)

def CreateEvent(ql: Qiling, params):
    event_id = len(ql.loader.events)
    event_dic = {
        "NotifyFunction": params["NotifyFunction"],
        "CallbackArgs"    : [event_id, params["NotifyContext"]],
        "Guid"            : "",
        "Set"            : False
    }

    if "EventGroup" in params:
        event_dic["EventGroup"] = params["EventGroup"]

    ql.loader.events[event_id] = event_dic
    write_int64(ql, params["Event"], event_id)

    return EFI_SUCCESS

def initialize(ql: Qiling, gBS: int):
    descriptor = {
        'struct' : EFI_BOOT_SERVICES,
        'fields' : (
            ('Hdr',                            None),
            ('RaiseTPL',                    EFI_BOOT_SERVICES.hook_RaiseTPL),
            ('RestoreTPL',                    EFI_BOOT_SERVICES.hook_RestoreTPL),
            ('AllocatePages',                EFI_BOOT_SERVICES.hook_AllocatePages),
            ('FreePages',                    EFI_BOOT_SERVICES.hook_FreePages),
            ('GetMemoryMap',                EFI_BOOT_SERVICES.hook_GetMemoryMap),
            ('AllocatePool',                EFI_BOOT_SERVICES.hook_AllocatePool),
            ('FreePool',                    EFI_BOOT_SERVICES.hook_FreePool),
            ('CreateEvent',                    EFI_BOOT_SERVICES.hook_CreateEvent),
            ('SetTimer',                    EFI_BOOT_SERVICES.hook_SetTimer),
            ('WaitForEvent',                EFI_BOOT_SERVICES.hook_WaitForEvent),
            ('SignalEvent',                    EFI_BOOT_SERVICES.hook_SignalEvent),
            ('CloseEvent',                    EFI_BOOT_SERVICES.hook_CloseEvent),
            ('CheckEvent',                    EFI_BOOT_SERVICES.hook_CheckEvent),
            ('InstallProtocolInterface',    EFI_BOOT_SERVICES.hook_InstallProtocolInterface),
            ('ReinstallProtocolInterface',    EFI_BOOT_SERVICES.hook_ReinstallProtocolInterface),
            ('UninstallProtocolInterface',    EFI_BOOT_SERVICES.hook_UninstallProtocolInterface),
            ('HandleProtocol',                EFI_BOOT_SERVICES.hook_HandleProtocol),
            ('Reserved',                    None),
            ('RegisterProtocolNotify',        EFI_BOOT_SERVICES.hook_RegisterProtocolNotify),
            ('LocateHandle',                EFI_BOOT_SERVICES.hook_LocateHandle),
            ('LocateDevicePath',            EFI_BOOT_SERVICES.hook_LocateDevicePath),
            ('InstallConfigurationTable',    EFI_BOOT_SERVICES.hook_InstallConfigurationTable),
            ('LoadImage',                    EFI_BOOT_SERVICES.hook_LoadImage),
            ('StartImage',                    EFI_BOOT_SERVICES.hook_StartImage),
            ('Exit',                        EFI_BOOT_SERVICES.hook_Exit),
            ('UnloadImage',                    EFI_BOOT_SERVICES.hook_UnloadImage),
            ('ExitBootServices',            EFI_BOOT_SERVICES.hook_ExitBootServices),
            ('GetNextMonotonicCount',        EFI_BOOT_SERVICES.hook_GetNextMonotonicCount),
            ('Stall',                        EFI_BOOT_SERVICES.hook_Stall),
            ('SetWatchdogTimer',            EFI_BOOT_SERVICES.hook_SetWatchdogTimer),
            ('ConnectController',            EFI_BOOT_SERVICES.hook_ConnectController),
            ('DisconnectController',        EFI_BOOT_SERVICES.hook_DisconnectController),
            ('OpenProtocol',                EFI_BOOT_SERVICES.hook_OpenProtocol),
            ('CloseProtocol',                EFI_BOOT_SERVICES.hook_CloseProtocol),
            ('OpenProtocolInformation',        EFI_BOOT_SERVICES.hook_OpenProtocolInformation),
            ('ProtocolsPerHandle',            EFI_BOOT_SERVICES.hook_ProtocolsPerHandle),
            ('LocateHandleBuffer',            EFI_BOOT_SERVICES.hook_LocateHandleBuffer),
            ('LocateProtocol',                EFI_BOOT_SERVICES.hook_LocateProtocol),
            ('InstallMultipleProtocolInterfaces',    EFI_BOOT_SERVICES.hook_InstallMultipleProtocolInterfaces),
            ('UninstallMultipleProtocolInterfaces',    EFI_BOOT_SERVICES.hook_UninstallMultipleProtocolInterfaces),
            ('CalculateCrc32',                EFI_BOOT_SERVICES.hook_CalculateCrc32),
            ('CopyMem',                        EFI_BOOT_SERVICES.hook_CopyMem),
            ('SetMem',                        EFI_BOOT_SERVICES.hook_SetMem),
            ('CreateEventEx',                EFI_BOOT_SERVICES.hook_CreateEventEx)
        )
    }

    ql.os.monotonic_count = 0

    instance = init_struct(ql, gBS, descriptor)
    instance.saveTo(ql, gBS)
