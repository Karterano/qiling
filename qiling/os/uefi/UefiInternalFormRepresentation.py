from .ProcessorBind import *
from .UefiBaseType import *

# @see: BaseTools/Source/C/Include/Common/UefiInternalFormRepresentation.h
EFI_HII_HANDLE = PTR(VOID)
EFI_STRING = PTR(UINT16)
EFI_IMAGE_ID = UINT16

EFI_STRING_ID = UINT16

EFI_HII_FONT_STYLE = UINT32


EFI_HII_PACKAGE_STRINGS = 0x04
EFI_HII_PACKAGE_END     = 0xDF


class EFI_HII_PACKAGE_LIST_HEADER(STRUCT):
    _fields_ = [
        ('PackageListGuid',   EFI_GUID),
        ('PackagLength',    UINT32)
    ]

class EFI_HII_PACKAGE_HEADER(STRUCT):
    _fields_ = [
        # Necessary as ctypes do not permit 24 bit fields
        ('LengthLow', UINT16),  # UINT32  Length:24;
        ('LengthHigh', UINT8),
        ('Type', UINT8),        # UINT32  Type:8;
        # ('Data', PTR(UINT8))  # Array
    ]


class EFI_HII_STRING_PACKAGE_HDR(STRUCT):
    _fields_ = [
        ('Header',              EFI_HII_PACKAGE_HEADER),
        ('HdrSize',             UINT32),
        ('StringInfoOffset',    UINT32),
        ('LanguageWindow',      CHAR16 * 16),
        ('LanguageName',        EFI_STRING_ID),
        ('Language',            CHAR8 * 1)      # CHAR8 Language [... ];
    ]


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
        # ('Descriptors', PTR(EFI_KEY_DESCRIPTOR))  # Array
    ]