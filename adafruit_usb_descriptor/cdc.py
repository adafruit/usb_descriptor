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

import struct

from . import standard

"""
CDC specific descriptors
========================

This PDF is a good reference:
    https://cscott.net/usb_dev/data/devclass/usbcdc11.pdf

* Author(s): Scott Shawcroft
"""

CDC_CLASS_DEVICE = 0x02
CDC_CLASS_COMM = 0x02
CDC_CLASS_DATA = 0x0A

CDC_SUBCLASS_DLCM = 0x01
CDC_SUBCLASS_ACM = 0x02  # Abstract Control Model
CDC_SUBCLASS_TCM = 0x03
CDC_SUBCLASS_MCCM = 0x04
CDC_SUBCLASS_CCM = 0x05
CDC_SUBCLASS_ETH = 0x06
CDC_SUBCLASS_ATM = 0x07

CDC_PROTOCOL_NONE = 0x0
CDC_PROTOCOL_V25TER = 0x01   # Common AT commands
# Many other protocols omitted.

class Header:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x00
    fmt = "<BBB" + "H"
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 bcdCDC):
        self.description = description
        self.bcdCDC = bcdCDC

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           self.bcdCDC)


class CallManagement:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x01
    fmt = "<BBB" + "BB"
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 bmCapabilities,
                 bDataInterface):
        self.description = description
        self.bmCapabilities = bmCapabilities
        self.bDataInterface = bDataInterface

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           self.bmCapabilities,
                           self.bDataInterface)


class AbstractControlManagement:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x02
    fmt = "<BBB" + "B"
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 bmCapabilities):
        self.description = description
        self.bmCapabilities = bmCapabilities

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           self.bmCapabilities)



class DirectLineManagement:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x03
    fmt = "<BBB" + "B"
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 bmCapabilities):
        self.description = description
        self.bmCapabilities = bmCapabilities

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           self.bmCapabilities)


class Union:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x06
    fixed_fmt = "<BBB" + "B"     # not including bSlaveInterface_list
    fixed_bLength = struct.calcsize(fixed_fmt)

    @property
    def bLength(self):
        return self.fixed_bLength + len(self.bSlaveInterface_list)

    def __init__(self, *,
                 description,
                 bMasterInterface,
                 bSlaveInterface_list):
        self.description = description
        self.bMasterInterface = bMasterInterface
        # bSlaveInterface_list is a list of one or more slave interfaces.
        self.bSlaveInterface_list = bSlaveInterface_list

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fixed_fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           self.bMasterInterface) + bytes(self.bSlaveInterface_list)
