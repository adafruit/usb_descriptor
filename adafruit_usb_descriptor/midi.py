# The MIT License (MIT)
#
# Copyright (c) 2018 Scott Shawcroft for Adafruit Industries
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
Audio specific descriptors
================================

* Author(s): Scott Shawcroft
"""

ENDPOINT_DESCRIPTOR_SUBTYPE_UNDEFINED = 0x00
ENDPOINT_DESCRIPTOR_SUBTYPE_GENERAL = 0x01

JACK_TYPE_UNDEFINED = 0x00
JACK_TYPE_EMBEDDED = 0x01
JACK_TYPE_EXTERNAL = 0x02

class Header:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x01
    fmt = "<BBB" + "HH"
    bLength = struct.calcsize(fmt)

    def __init__(self, *, jacks_and_elements=[]):
        self.jacks_and_elements = jacks_and_elements

    def notes(self):
        notes = [str(self)]
        for jack in self.jacks_and_elements:
            notes.extend(jack.notes())
        return notes

    def __bytes__(self):
        for i, element in enumerate(self.jacks_and_elements):
            element.id = i + 1

        jacks_and_elements_encoded = b''.join(map(bytes, self.jacks_and_elements))
        header_encoded = struct.pack(self.fmt,
                                     self.bLength,
                                     self.bDescriptorType,
                                     self.bDescriptorSubtype,
                                     0x0100,
                                     self.bLength + len(jacks_and_elements_encoded))
        return header_encoded + jacks_and_elements_encoded

class InJackDescriptor:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x02
    fmt = "<BBB" + "BBB"
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 bJackType,
                 iJack=0):
        self.description = description
        self.id = 0 # auto assigned by the parent midi.Header
        self.bJackType = bJackType
        self.iJack = iJack

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           self.bJackType,
                           self.id,
                           self.iJack)

class OutJackDescriptor:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x03
    fixed_fmt = "<BBB" + "BBB"     # not including pin list
    fixed_bLength = struct.calcsize(fixed_fmt)

    def __init__(self, *,
                 description,
                 bJackType,
                 input_pins=[],
                 iJack=0):
        self.description = description
        self.id = 0 # auto assigned by the parent midi.Header
        self.bJackType = bJackType
        self.iJack = iJack
        self.input_pins = input_pins

    @property
    def bLength(self):
        return self.fixed_bLength + len(self.input_pins) * 2 + 1

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        input_pins = bytearray(len(self.input_pins) * 2)
        for i, input_pin in enumerate(self.input_pins):
            element, pin_number = input_pin
            input_pins[2 * i] = element.id
            input_pins[2 * i + 1] = pin_number

        return struct.pack(self.fixed_fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           self.bJackType,
                           self.id,
                           len(self.input_pins)) + input_pins + bytes([self.iJack])

class ElementDescriptor:
    bDescriptorSubtype = 0x04

    def notes(self):
        return [str(self)]

class DataEndpointDescriptor:
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = ENDPOINT_DESCRIPTOR_SUBTYPE_GENERAL
    fixed_fmt = "<BBB" + "B" # not including jack list
    fixed_bLength = struct.calcsize(fixed_fmt)

    def __init__(self, *,
                 baAssocJack=[]):
        self.baAssocJack = baAssocJack

    @property
    def bLength(self):
        return self.fixed_bLength + len(self.baAssocJack)

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        baAssocJack = bytes([x.id for x in self.baAssocJack])
        return struct.pack(self.fixed_fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           len(self.baAssocJack)) + baAssocJack
