import os


def get_test_data_file_contents(name):
    with open(os.path.join('tests', 'data', name), 'rb') as f:
        return f.read()
