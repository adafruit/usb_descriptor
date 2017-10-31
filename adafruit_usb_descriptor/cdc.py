# The MIT License (MIT)
#
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from . import core
import struct

"""
CDC specific descriptors
========================

This PDF is a good reference:
    https://cscott.net/usb_dev/data/devclass/usbcdc11.pdf

* Author(s): Scott Shawcroft
"""


class FunctionalDescriptor(core.Descriptor):
    """Common functional descriptor parent. Subclasses must specify
       bDescriptorSubtype in addition to the fields needed by
       `core.Descriptor`.
    """
    bDescriptorType = 0x24

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fmt = "<BBB" + self.fmt[3:]

    def __bytes__(self):
        return struct.pack(self.fmt, self.bLength, self.bDescriptorType,
                           self.bDescriptorSubtype, *self.data)


class Header(FunctionalDescriptor):
    fields = [('bcdCDC', "H", None)]
    bLength = 0x05
    bDescriptorSubtype = 0x0


class CallManagement(FunctionalDescriptor):
    fields = [('bmCapabilities', "b", None),
              ('bDataInterface', "b", None)]
    bLength = 0x05
    bDescriptorSubtype = 0x01


class AbstractControlManagement(FunctionalDescriptor):
    fields = [('bmCapabilities', "b", None)]
    bLength = 0x04
    bDescriptorSubtype = 0x02


class DirectLineManagement(FunctionalDescriptor):
    fields = [('bmCapabilities', "b", None)]
    bLength = 0x04
    bDescriptorSubtype = 0x03


class Union(FunctionalDescriptor):
    fields = [('bMasterInterface', "b", None)]
    bDescriptorSubtype = 0x06

    def __init__(self, *args, **kwargs):
        self.bSlaveInterface = kwargs["bSlaveInterface"]
        super().__init__(*args, **kwargs)

    def __bytes__(self):
        return super().__bytes__() + bytes(self.bSlaveInterface)

    @property
    def bLength(self):
        return 0x4 + len(self.bSlaveInterface)
