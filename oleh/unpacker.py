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

    def _unpack_struct(self, fmt, cursor, data):
        fmt_size = struct.calcsize(fmt)
        struct_f = struct.unpack(fmt, data[cursor:cursor + fmt_size])
        return fmt_size, struct_f

    def _unpack_string(self, cursor, data):
        int_length = 4
        l = struct.unpack('<i', data[cursor:cursor + int_length])[0]
        string = struct.unpack(
            '{0}s'.format(l),
            data[cursor + int_length:cursor + int_length + l])[0]
        return int_length + l, string

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

        cursor = 0

        if not self._b:
            return Img(None, bytes())

        offset, pkg_header_f = self._unpack_struct(PKG_H_FMT, cursor, self._b)
        pkg_header = PackageHeader(*pkg_header_f)
        cursor += (offset + pkg_header.l_class_name + pkg_header.l_name)

        offset, ole_header_f = self._unpack_struct(OLE_H_FMT, cursor, self._b)
        ole_header = OleHeader(*ole_header_f)
        cursor += offset

        offset, class_name = self._unpack_string(cursor, self._b)
        cursor += offset
        offset, topic_name = self._unpack_string(cursor, self._b)
        cursor += offset

        offset, item_name = self._unpack_string(cursor, self._b)
        cursor += offset

        offset, data_h_f = self._unpack_struct(DATA_H_FMT, cursor, self._b)
        data_header = DataHeader(*data_h_f)
        cursor += offset

        # Both file name and file path are between 02 (short) and 0 (short)
        # and 3 (short)
        for i in range(len(self._b[cursor:])):
            offset, word = self._unpack_struct('>BB', cursor, self._b)
            if word == FILE_NAME_END_FLAG:
                break
            else:
                cursor += offset

        cursor += offset
        offset, file_temp_name = self._unpack_string(cursor, self._b)
        cursor += offset

        offset, data_len = self._unpack_struct('i', cursor, self._b)
        cursor += offset
        data = self._b[cursor:cursor + data_len[0]]

        return Img(what_is_it(data), bytes(data))
