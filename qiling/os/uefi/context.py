from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Mapping, MutableSequence, Optional, Tuple
from uuid import UUID

from qiling import Qiling
from qiling.os.memory import QlMemoryHeap
from qiling.os.uefi.ProcessorBind import STRUCT, CPU_STACK_ALIGNMENT
from qiling.os.uefi.UefiInternalFormRepresentation import *
from qiling.os.uefi.UefiInternalFormRepresentation import EFI_HII_PACKAGE_STRINGS, EFI_HII_PACKAGE_END
from qiling.os.uefi.protocols.EfiLDevicePathProtocol import EFI_DEVICE_PATH_PROTOCOL
from qiling.os.uefi.UefiSpec import EFI_CONFIGURATION_TABLE
from qiling.os.uefi.smst import EFI_SMM_SYSTEM_TABLE2
from qiling.os.uefi.st import EFI_SYSTEM_TABLE
from qiling.os.uefi import utils

class UefiContext(ABC):
    def __init__(self, ql: Qiling):
        self.ql = ql
        self.heap: QlMemoryHeap
        self.top_of_stack: int
        self.protocols = {}
        self.loaded_image_protocol_modules: MutableSequence[int] = []
        self.next_image_base: int

        # These members must be initialized before attempting to install a configuration table.
        self.conf_table_data_ptr = 0
        self.conf_table_data_next_ptr = 0

        self.conftable: UefiConfTable
        self.end_of_execution_ptr: int

    # TODO: implement save state
    def save(self) -> Mapping[str, Any]:
        return {}

    # TODO: implement restore state
    def restore(self, saved_state: Mapping[str, Any]):
        pass

    def init_heap(self, base: int, size: int):
        self.heap = QlMemoryHeap(self.ql, base, base + size)

    def init_stack(self, base: int, size: int):
        self.ql.mem.map(base, size, info='[stack]')
        self.top_of_stack = (base + size - 1) & ~(CPU_STACK_ALIGNMENT - 1)

    def install_protocol(self, proto_desc: Mapping, handle: int, address: int = None, from_hook: bool = False):
        guid = proto_desc['guid']

        if handle not in self.protocols:
            self.protocols[handle] = {}

        if guid in self.protocols[handle]:
            self.ql.log.warning(f'a protocol with guid {guid} is already installed')

        if 'struct' in proto_desc:
            if address is None:
                struct_class = proto_desc['struct']
                address = self.heap.alloc(struct_class.sizeof())

            instance = utils.init_struct(self.ql, address, proto_desc)
            instance.saveTo(self.ql, address)

        # Nothing must be stored here, these kind of protocols should only add the pointer to the 
        #   handle-guid-database and return it
        elif 'pointer_name' in proto_desc:
            if address is None:
                address = proto_desc['address']

            pointer_class = proto_desc['pointer_name']

            self.ql.log.info(f'Initializing {pointer_class.__name__}')
            self.ql.log.info(f" | {'->':36s} {hex(address)}")

        self.protocols[handle][guid] = address
        return self.notify_protocol(handle, guid, address, from_hook)

    def notify_protocol(self, handle: int, protocol: str, interface: int, from_hook: bool):
        for (event_id, event_dic) in self.ql.loader.events.items():
            if event_dic['Guid'] == protocol:
                if event_dic['CallbackArgs'] == None:
                    # To support smm notification, we use None for CallbackArgs on SmmRegisterProtocolNotify 
                    # and updare it here.
                    guid = utils.str_to_guid(protocol)
                    guid_ptr = self.heap.alloc(guid.sizeof())
                    guid.saveTo(self.ql, guid_ptr)

                    event_dic['CallbackArgs'] = [guid_ptr, interface, handle]

                # The event was previously registered by 'RegisterProtocolNotify'.
                utils.signal_event(self.ql, event_id)

        return utils.execute_protocol_notifications(self.ql, from_hook)

class DxeContext(UefiContext):
    def __init__(self, ql: Qiling):
        super().__init__(ql)

        self.conftable = DxeConfTable(ql)
        self.hii_context = HiiContext(ql)


class SmmContext(UefiContext):
    def __init__(self, ql: Qiling):
        super().__init__(ql)

        self.conftable = SmmConfTable(ql)

        self.smram_base: int
        self.smram_size: int

        # assume tseg is inaccessible to non-smm
        self.tseg_open = False

        # assume tseg is locked
        self.tseg_locked = True

        # registered sw smi handlers
        self.swsmi_handlers: Mapping[int, Tuple[int, Mapping]] = {}

class UefiConfTable:
    _struct_systbl: STRUCT
    _fname_arrptr: str
    _fname_nitems: str

    def __init__(self, ql: Qiling):
        self.ql = ql

        self.__arrptr_off = self._struct_systbl.offsetof(self._fname_arrptr)
        self.__nitems_off = self._struct_systbl.offsetof(self._fname_nitems)

    @property
    @abstractmethod
    def system_table(self) -> int:
        pass

    @property
    def baseptr(self) -> int:
        addr = self.system_table + self.__arrptr_off

        return utils.read_int64(self.ql, addr)

    @property
    def nitems(self) -> int:
        addr = self.system_table + self.__nitems_off

        return utils.read_int64(self.ql, addr)    # UINTN

    @nitems.setter
    def nitems(self, value: int):
        addr = self.system_table + self.__nitems_off

        utils.write_int64(self.ql, addr, value)

    def install(self, guid: str, table: int):
        ptr = self.find(guid)
        append = ptr is None

        if append:
            ptr = self.baseptr + self.nitems * EFI_CONFIGURATION_TABLE.sizeof()
            append = True

        instance = EFI_CONFIGURATION_TABLE()
        instance.VendorGuid = utils.str_to_guid(guid)
        instance.VendorTable = table
        instance.saveTo(self.ql, ptr)

        if append:
            self.nitems += 1

    def find(self, guid: str) -> Optional[int]:
        ptr = self.baseptr
        nitems = self.nitems
        efi_guid = utils.str_to_guid(guid)

        for _ in range(nitems):
            entry = EFI_CONFIGURATION_TABLE.loadFrom(self.ql, ptr)

            if utils.CompareGuid(entry.VendorGuid, efi_guid):
                return ptr

            ptr += EFI_CONFIGURATION_TABLE.sizeof()

        return None

    def get_vendor_table(self, guid: str) -> Optional[int]:
        ptr = self.find(guid)

        if ptr is not None:
            entry = EFI_CONFIGURATION_TABLE.loadFrom(self.ql, ptr)

            return entry.VendorTable.value

        # not found
        return None


class DxeConfTable(UefiConfTable):
    _struct_systbl = EFI_SYSTEM_TABLE
    _fname_arrptr = 'ConfigurationTable'
    _fname_nitems = 'NumberOfTableEntries'

    @property
    def system_table(self) -> int:
        return self.ql.loader.gST


class HiiContext:
    def __init__(self, ql: Qiling) -> None:
        self.ql = ql
        self.guid_to_package_list_handle: dict[str, int] = {}  # {guid: package_list_handle, ...}
        self.package_list_handle_to_device_handle: dict[int, int] = {}  # {package_list_handle: device_handle, ...}
        self.package_lists: dict[int, list[Any]] = {}  # {package_list_handle: [package, package, ...], ...}
        self.supported_languages: dict[int, Any]= defaultdict(set)  # {package_list_handle: }
        self.next_handle: int = 0x10
    
    def add_form_package(self, package_list_handle, package_header_ptr):
        form_package_header: EFI_HII_FORM_PACKAGE_HDR = EFI_HII_FORM_PACKAGE_HDR.loadFrom(self.ql, package_header_ptr)
        # data seems to be in sub-headers again
        self.ql.log.warning(f"Hii forms are not implemented and will not be added to the package list")

    def add_string_package(self, package_list_handle, package_header_ptr):
        string_package_header: EFI_HII_STRING_PACKAGE_HDR = EFI_HII_STRING_PACKAGE_HDR.loadFrom(self.ql, package_header_ptr)
        language_ptr = package_header_ptr + string_package_header.offsetof('Language')
        language = self.ql.os.utils.read_cstring(language_ptr)
        self.ql.log.debug(f"Language: {language}")
        self.supported_languages[package_list_handle] |= {language}

    def add_device_path_package(self, package_list_handle, device_path):
        # @see: MdeModulePkg\Universal\HiiDatabaseDxe\Database.c
        # this adds a simple package like
        # ---
        # EFI_HII_PACKAGE_HEADER
        # | Length
        # | Type
        # EFI_DEVICE_PATH_PROTOCOL
        # ---
        # Still requires device path protocol to be implemented, which is massive 
        self.ql.log.warning(f"EFI_DEVICE_PATH_PROTOCOL is not implemented and will not be added to the package list")


    # data is a complete packagelistheader, but we are too lazy to read the guid from the header here
    def add_package_list(self, address: int, package_list_header: EFI_HII_PACKAGE_LIST_HEADER) -> int:
        package_list_guid = UUID(bytes_le=bytes(package_list_header.PackageListGuid))

        if package_list_guid in self.guid_to_package_list_handle:
            package_list_handle = self.guid_to_package_list_handle[package_list_guid]
        else:
            package_list_handle = self.next_handle
            self.guid_to_package_list_handle[package_list_guid] = package_list_handle
            self.next_handle += 1

        # first package header comes directly after package list header
        package_header_ptr = address + EFI_HII_PACKAGE_LIST_HEADER.sizeof()

        # TODO iterate over packages in list and add them (and extact their language)
        while package_header_ptr < address + package_list_header.PackagLength:
            package_header: EFI_HII_PACKAGE_HEADER = EFI_HII_PACKAGE_HEADER.loadFrom(self.ql, package_header_ptr)
            package_length = (package_header.LengthHigh << 16) + package_header.LengthLow
            package_type: int = package_header.Type

            self.ql.log.debug(f"Length: {hex(package_length)}")
            self.ql.log.debug(f"Type: {hex(package_type)}")

            if package_type == EFI_HII_PACKAGE_FORMS:
                self.add_form_package(package_list_handle, package_header_ptr)
            elif package_type == EFI_HII_PACKAGE_STRINGS:
                self.add_string_package(package_list_handle, package_header_ptr)
            elif package_type == EFI_HII_PACKAGE_DEVICE_PATH:
                self.add_device_path_package(package_list_handle, None)
            elif package_type == EFI_HII_PACKAGE_END:
                pass
            else:
                self.ql.log.warning(f"Cannot handle package type {package_type}, skipping")

            package_header_ptr += package_length

        self.package_lists[package_list_handle] = package_list_guid

        return package_list_handle

    def get_package_list(self, handle):
        return self.package_lists[handle]


class SmmConfTable(UefiConfTable):
    _struct_systbl = EFI_SMM_SYSTEM_TABLE2
    _fname_arrptr = 'SmmConfigurationTable'
    _fname_nitems = 'NumberOfTableEntries'

    @property
    def system_table(self) -> int:
        return self.ql.loader.gSmst
