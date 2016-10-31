from collections import namedtuple
from oleh.inspector import what_is_it

import struct

PKG_HEADER_FMT = (
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

OLE_HEADER_FMT = (
    '<'  # little-endian
    'I'  # OLE version
    'I'  # format
)
OleHeader = namedtuple('OleHeader', [
    'version',
    'format',
])

DATA_HEADER_FMT = (
    '<'
    'I'  # data len
    'h'  # file namd and file path init flag
)
FILE_NAME_END_FLAG = 0x3000

DataHeader = namedtuple('DataHeader', [
    'data_len',
    'file_name_init_flag'
])


Img = namedtuple('Img', 'what bytes')


class Unpacker:

    def __init__(self, ole_object_bytes):
        self.ole_b = memoryview(ole_object_bytes)
        self.cursor = 0

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
        def _unpack_struct(fmt):
            fmt_size = struct.calcsize(fmt)
            struct_slice = slice(self.cursor, self.cursor + fmt_size)
            struct_f = struct.unpack(fmt, self.ole_b[struct_slice])
            self.cursor += fmt_size
            return struct_f

        def _unpack_string():
            l = struct.unpack('<i', self.ole_b[self.cursor:self.cursor + 4])[0]
            self.cursor += 4
            string_slice = slice(self.cursor, self.cursor + l)
            string = struct.unpack(
                '{0}s'.format(l), self.ole_b[string_slice])[0]
            self.cursor += l
            return string

        if not self.ole_b:
            return Img(None, bytes())

        pkg_header = PackageHeader(*_unpack_struct(PKG_HEADER_FMT))
        self.cursor += (pkg_header.l_class_name + pkg_header.l_name)

        ole_header = OleHeader(*_unpack_struct(OLE_HEADER_FMT))

        # We need to check class name in order to determine what parsing
        # strategy to use
        class_name = _unpack_string()
        if class_name == b'Package\x00':
            # Since we are dealing with an embedded object, both topic name and
            # item name will be empty, here we are just offsetting based on two
            # fields: Length of topic (uint) name and length of item name(uint)
            self.cursor += 4 + 4
            data_header = DataHeader(*_unpack_struct(DATA_HEADER_FMT))

            # Both file name and file path are between 02 (short) and 0 (short)
            # and 3 (short)
            for i in range(len(self.ole_b[self.cursor:])):
                if _unpack_struct('>BB') == (0x03, 0x00):
                    break

            file_temp_name = _unpack_string()
            data_len = _unpack_struct('i')[0]
            data = self.ole_b[self.cursor:self.cursor + data_len]

        return Img(what_is_it(data), bytes(data))
