![Travis-CI Status](https://travis-ci.org/juan-fdz-hawa/oleh.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/juan-fdz-hawa/oleh/badge.svg?branch=master)](https://coveralls.io/github/juan-fdz-hawa/oleh?branch=master)

# Problem
You want to extract 'Packaged' OLE files on an Access database.

# Solution
```python
import oleh

img = oleh.unpack(ole_object_bytes)

# Returns type of image {'rgb', 'gif', 'pbm', 'pgm', 'tiff', 'rast','xbm', 'jpeg', 'bmp', 'png', None}
img.what

# The creamy binary filling of the OLE object
img.bytes
```

# Anatomy of an OLE Object
- Package header
- OLE header
- Data length (uint)
- Data (with can either be a compound file structure or just data).
- Metafilepict block: If present - like in the case of images - it will be composed of a Metafilepict header (45 bytes) + data
- OLE footer

#### Package header:
- Signature (short): Indicates whether file is a compound or not
- Header size (short)
- Object type (uint): 0 = linked, 1 = embedded, 2 = either
- Length of friendly name in the header (short)
- Length of class name in the header (short)
- Offset of the friendly name (short)
- Offset of the class name (short)
- Size of object (int)
- Friendly name (string, variable length)
- Class name (string, variable length)

#### Ole header
- OLE version (uint)
- Format (uint)
- Class name length (int)
- Class name (string, var length)
- Topic name length (int)
- Topic name (string)
- Item name length (int)
- Item name (string)

##### Additional notes
Ole header format must be either:
- 01: Ole header is followed by LinkedObject structure
- 02: Ole header must followed by EmbeddedObject structure

When dealing with embedded objects, both topic name and item name will be empty
