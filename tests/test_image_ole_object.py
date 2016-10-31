import pytest

from .util import get_test_data_file_contents
from .context import oleh


def stest_unpacking_images_returns_correct_img_type():
    test_cases = [
        ('ole_object_bmp', 'bmp'),
        ('ole_object_png', 'png'),
        ('ole_object_jpg', 'jpeg')
    ]
    for ole_obj_filename, img_ext in test_cases:
        ole = get_test_data_file_contents(ole_obj_filename)
        assert oleh.unpack(ole).what == img_ext


def test_unpacking_images_returns_correct_bytes():
    test_cases = [
         #('test.bmp', 'ole_object_bmp'),
         #('test.png', 'ole_object_png'),
         #('test.jpg', 'ole_object_jpg'),
         ('test.bmp', 'ole_object_0')
    ]
    for img_filename, ole_obj_filename in test_cases:
        img = get_test_data_file_contents(img_filename)
        ole_object = get_test_data_file_contents(ole_obj_filename)
        assert oleh.unpack(ole_object).bytes == img
