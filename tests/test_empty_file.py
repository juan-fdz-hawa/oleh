from .context import oleh


def test_no_bytes_returns_no_bytes():
    no_bytes = bytes()
    result = oleh.unpack(no_bytes)
    assert len(result.bytes) == 0


def test_no_bytes_returns_none_as_type():
    no_bytes = bytes()
    result = oleh.unpack(no_bytes)
    assert result.what is None
