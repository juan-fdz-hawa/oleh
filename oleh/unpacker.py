from collections import namedtuple
from oleh.inspector import what_is_it

import struct

PKG_H_FMT = (
    '<'  # little-endian
    'h'  # signature
    'h'  # header size
    'I'  # object type
    'h'  # length of name
    'h'  # lenth of class name in the header
    'h'  # offset of name
    'h'  # offset of the class name
    'i'  # size of the object
)
PackageHeader = namedtuple('PackageHeader', [
    'signature',
    'size',
    'object_type',
    'l_name',
    'l_class_name',
    'offset_name',
    'offset_class_name',
    'object_size'
    ]
)

OLE_H_FMT = (
    '<'  # little-endian
    'I'  # OLE version
    'I'  # format
)
OleHeader = namedtuple('OleHeader', ['version', 'format'])

DATA_H_FMT = (
    '<'
    'I'  # data len
    'h'  # file namd and file path init flag
)
DataHeader = namedtuple('DataHeader', [
    'data_len',
    'file_name_init_flag'
])
FILE_NAME_END_FLAG = (0x03, 0x00)

Img = namedtuple('Img', 'what bytes')


class Unpacker:

    def __init__(self, ole_object_bytes):
        self._b = memoryview(ole_object_bytes)
        self._cursor = 0

    def _extract_struct(self, fmt):
        """
        Extracts struct specified by fmt and moves
        the cursor accordantly
        """
        fmt_size = struct.calcsize(fmt)
        struct_f = struct.unpack(
            fmt,
            self._b[self._cursor:self._cursor + fmt_size])
        self._cursor += fmt_size

        return struct_f

    def _extract_string(self):
        """
        Extract string. Next word must specify the length of the string.
        Moves the cursor accordantly
        """
        int_length = 4
        l = struct.unpack(
            '<i',
            self._b[self._cursor:self._cursor + int_length])[0]
        self._cursor += int_length
        string = struct.unpack(
            '{0}s'.format(l),
            self._b[self._cursor:self._cursor + l])[0]
        self._cursor += l
        return string

    def unpack(self):
        """
        Unpacks image contained inside the OLE object.

        Args:
            ole_object_bytes (bytes): OLE object bytes

        Returns:
            namedtuple('Img', ['what', 'bytes']):
                what: returns image MIME type,
                bytes: returns image bytes.
        """

        if not self._b:
            return Img(None, bytes())

        # Package header
        pkg_header = PackageHeader(*self._extract_struct(PKG_H_FMT))
        self._cursor += (pkg_header.l_class_name + pkg_header.l_name)

        # Ole Header
        ole_header = OleHeader(*self._extract_struct(OLE_H_FMT))
        class_name = self._extract_string()
        topic_name = self._extract_string()
        item_name = self._extract_string()

        data_header = DataHeader(*self._extract_struct(DATA_H_FMT))

        # Both file name and file path are between 02 (short) and 0 (short)
        # and 3 (short)
        for i in range(len(self._b[self._cursor:])):
            if self._extract_struct('>BB') == FILE_NAME_END_FLAG:
                break

        file_temp_name = self._extract_string()
        data_len = self._extract_struct('i')

        data = self._b[self._cursor:self._cursor + data_len[0]]
        return Img(what_is_it(data), bytes(data))
