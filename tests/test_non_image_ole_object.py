import pytest

from .util import get_test_data_file_contents
from .context import oleh


def unpacking_non_image_object_should_throw_up():
    with pytest.raises(ValueError) as e:
        word_ole_obj = get_test_data_file_contents('ole_object_word')
        oleh.unpack(word_ole_obj)
    assert str(e.value) == "Can only unpack non-images!!"
