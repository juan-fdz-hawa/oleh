import struct


def what_is_it(data):
    """
    Returns file extension of image based on signature:
    https://en.wikipedia.org/wiki/List_of_file_signatures

    Args:
        data: image bytes

    Returns:
        File type, where file type E {'jpeg', 'png', 'gif', 'tiff', 'bmp'}
    """
    tests = [
        lambda b: 'bmp' if b[:2] == b'BM' else None,
        lambda b: 'tiff' if b[:4] in (b'II*.', b'MM.*') else None,
        lambda b: 'jpeg' if b[:4] == b'\xff\xd8\xff\xdb' else None,
        lambda b: 'jpeg' if b[:4] == b'\xff\xd8\xff\xe0' else None,
        lambda b: 'jpeg' if b[:4] == b'\xff\xd8\xff\xe1' else None,
        lambda b: 'png' if b[:8] == b'\211PNG\r\n\032\n' else None,
        lambda b: 'gif' if b[:6] in (b'GIF87a', b'GIF89a') else None
    ]

    # For all extensions, signature is contained in first 12 bytes
    h = bytes(struct.unpack('>8B', data[:8]))
    return next(test(h) for test in tests if test(h))
