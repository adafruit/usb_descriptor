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

DESCRIPTOR_TYPE_CLASS_SPECIFIC_DEVICE = 0x21
DESCRIPTOR_TYPE_CLASS_SPECIFIC_CONFIGURATION = 0x22
DESCRIPTOR_TYPE_CLASS_SPECIFIC_STRING = 0x23
DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE = 0x24
DESCRIPTOR_TYPE_CLASS_SPECIFIC_ENDPOINT = 0x25

class EndpointDescriptor:
    """Single endpoint configuration"""
    bDescriptorType = 0x5
    fmt = "<BB" + "BBHB"
    bLength = struct.calcsize(fmt)

    TYPE_CONTROL = 0b00
    TYPE_ISOCHRONOUS = 0b01
    TYPE_BULK = 0b10
    TYPE_INTERRUPT = 0b11

    DIRECTION_IN =  0x80
    DIRECTION_OUT = 0x00
    DIRECTION_MASK = DIRECTION_IN | DIRECTION_OUT
    NUMBER_MASK = ~DIRECTION_MASK

    def __init__(self, *,
                 description,
                 bEndpointAddress,
                 bmAttributes,
                 wMaxPacketSize=0x40,
                 bInterval=0x10):
        self.description = description
        self.bEndpointAddress = bEndpointAddress
        self.bmAttributes = bmAttributes
        self.wMaxPacketSize = wMaxPacketSize
        self.bInterval = bInterval

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bEndpointAddress,
                           self.bmAttributes,
                           self.wMaxPacketSize,
                           self.bInterval)


class InterfaceDescriptor:
    """Single interface that includes ``subdescriptors`` such as endpoints.

    ``subdescriptors`` can also include other class and vendor specific
    descriptors. They are serialized in order after the `InterfaceDescriptor`.
    They have their own bLength, and are not included in this descriptor's bLength.
    """
    bDescriptorType = 0x4
    fmt = "<BB" + "B"*7
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 bInterfaceNumber=0,
                 bAlternateSetting=0,
                 bNumEndpoints=0,
                 bInterfaceClass,
                 bInterfaceSubClass=0,
                 bInterfaceProtocol=0,
                 iInterface=0,
                 subdescriptors=[]):
        self.description = description
        self.bInterfaceNumber = bInterfaceNumber
        self.bAlternateSetting = bAlternateSetting
        self.bNumEndpoints = bNumEndpoints
        self.bInterfaceClass = bInterfaceClass
        self.bInterfaceSubClass = bInterfaceSubClass
        self.bInterfaceProtocol = bInterfaceProtocol
        self.iInterface = iInterface
        self.subdescriptors = subdescriptors

    def notes(self):
        notes = [str(self)]
        for s in self.subdescriptors:
            notes.extend(s.notes())
        return notes

    def __bytes__(self):
        endpoint_count = 0
        subdescriptor_bytes = []
        for desc in self.subdescriptors:
            subdescriptor_bytes.append(bytes(desc))
            if desc.bDescriptorType == EndpointDescriptor.bDescriptorType:
                endpoint_count += 1
        self.bNumEndpoints = endpoint_count
        initial_bytes = struct.pack(self.fmt,
                                    self.bLength,
                                    self.bDescriptorType,
                                    self.bInterfaceNumber,
                                    self.bAlternateSetting,
                                    self.bNumEndpoints,
                                    self.bInterfaceClass,
                                    self.bInterfaceSubClass,
                                    self.bInterfaceProtocol,
                                    self.iInterface)
        return initial_bytes + b''.join(subdescriptor_bytes)


class InterfaceAssociationDescriptor:
    """Groups interfaces into a single function"""
    bDescriptorType = 0xB
    fmt = "<BB" + "B"*6
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 bFirstInterface,
                 bInterfaceCount,
                 bFunctionClass,
                 bFunctionSubClass,
                 bFunctionProtocol,
                 iFunction = 0):
        self.description = description
        self.bFirstInterface = bFirstInterface
        self.bInterfaceCount = bInterfaceCount
        self.bFunctionClass = bFunctionClass
        self.bFunctionSubClass = bFunctionSubClass
        self.bFunctionProtocol = bFunctionProtocol
        self.iFunction = iFunction

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bFirstInterface,
                           self.bInterfaceCount,
                           self.bFunctionClass,
                           self.bFunctionSubClass,
                           self.bFunctionProtocol,
                           self.iFunction)


class ConfigurationDescriptor:
    """High level configuration that prepends the interfaces."""
    bDescriptorType = 0x2
    fmt = "<BB" + "HBBBBB"
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 wTotalLength,
                 bNumInterfaces,
                 bConfigurationValue=0x1,
                 iConfiguration=0,
                 # bus powered (bit 6), no remote wakeup (bit 5),
                 # bit 7 is always 1 and 0-4 are always 0
                 bmAttributes=0x80,
                 # 100 mA by default (50 means 100ma)
                 bMaxPower=50):
        self.description = description
        self.wTotalLength = wTotalLength
        self.bNumInterfaces = bNumInterfaces
        self.bConfigurationValue = bConfigurationValue
        self.iConfiguration = iConfiguration
        self.bmAttributes = bmAttributes
        self.bMaxPower = bMaxPower

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.wTotalLength,
                           self.bNumInterfaces,
                           self.bConfigurationValue,
                           self.iConfiguration,
                           self.bmAttributes,
                           self.bMaxPower)


class DeviceDescriptor:
    """Holds basic device level info."""
    bDescriptorType = 0x1
    fmt = "<BB" + "HBBBBHHHBBBB"
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description="unknown DeviceDescriptor",
                 bcdUSB=0x200,
                 bDeviceClass=0x00,
                 bDeviceSubClass=0x00,
                 bDeviceProtocol=0x00,
                 bMaxPacketSize=0x40,
                 idVendor,
                 idProduct,
                 bcdDevice=0x100,
                 iManufacturer,
                 iProduct,
                 iSerialNumber,
                 bNumConfigurations=1):
        self.description = description
        self.bcdUSB = bcdUSB
        self.bDeviceClass = bDeviceClass
        self.bDeviceSubClass = bDeviceSubClass
        self.bDeviceProtocol = bDeviceProtocol
        self.bMaxPacketSize = bMaxPacketSize
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.bcdDevice = bcdDevice
        self.iManufacturer = iManufacturer
        self.iProduct = iProduct
        self.iSerialNumber = iSerialNumber
        self.bNumConfigurations = bNumConfigurations

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bcdUSB,
                           self.bDeviceClass,
                           self.bDeviceSubClass,
                           self.bDeviceProtocol,
                           self.bMaxPacketSize,
                           self.idVendor,
                           self.idProduct,
                           self.bcdDevice,
                           self.iManufacturer,
                           self.iProduct,
                           self.iSerialNumber,
                           self.bNumConfigurations)


class StringDescriptor:
    """Holds a string referenced by another descriptor by index.

       It's recommended to hold these in a dict or list and look them up in subsequent
       descriptors to link to them.
    """
    bDescriptorType = 0x03

    def __init__(self, value):
        self.description = '"{}"'.format(value)
        if type(value) == str:
            self._bString = value.encode("utf-16-le")
            self._bLength = len(self._bString) + 2
        elif len(value) > 1:
            self._bLength = value[0]
            if value[1] != 3:
                raise ValueError("Sequence not a StringDescriptor")
            self._bString = value[2:2+self.bLength]

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack("BB{}s".format(len(self._bString)), self.bLength,
                           self.bDescriptorType, self._bString)

    @property
    def bString(self):
        return self._bString.decode("utf-16-le")

    @bString.setter
    def bString(self, value):
        self._bString = value.encode("utf-16-le")
        self._bLength = len(self.encoded) + 2

    @property
    def bLength(self):
        return self._bLength
