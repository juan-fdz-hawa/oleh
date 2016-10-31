from oleh.unpacker import Unpacker


def unpack(ole_object_bytes):
    return Unpacker(ole_object_bytes).unpack()
