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

class AudioControlInterface:
    """Single interface that includes ``subdescriptors`` such as endpoints.

    ``subdescriptors`` can also include other class and vendor specific
    descriptors. They are serialized in order after the `InterfaceDescriptor`.
    They have their own bLength, and are not included in this descriptor's bLength.
    """
    bDescriptorType = standard.DESCRIPTOR_TYPE_CLASS_SPECIFIC_INTERFACE
    bDescriptorSubtype = 0x06
    fixed_fmt = "<BBB" + "HHB"     # not including bSlaveInterface_list
    fixed_bLength = struct.calcsize(fixed_fmt)

    def __init__(self, *,
                 description,
                 units_and_terminals=[],
                 audio_streaming_interfaces=[],
                 midi_streaming_interfaces=[]):
        self.description = description
        self.bcdADC = 0x0100
        self.units_and_terminals = units_and_terminals
        self.audio_streaming_interfaces = audio_streaming_interfaces
        self.midi_streaming_interfaces = midi_streaming_interfaces

    @property
    def bLength(self):
        return self.fixed_bLength + len(self.audio_streaming_interfaces) + len(self.midi_streaming_interfaces)

    def notes(self):
        notes = [str(self)]
        for a in self.audio_streaming_interfaces:
            notes.extend(a.notes())
        for m in self.midi_streaming_interfaces:
            notes.extend(m.notes())
        return notes

    def __bytes__(self):
        units_and_terminals = bytes(self.units_and_terminals)
        wTotalLength = self.bLength + len(units_and_terminals)
        baInterfaceNr = bytes([x.bInterfaceNumber for x in self.audio_streaming_interfaces + self.midi_streaming_interfaces])
        subinterfaces = b''.join(map(bytes, self.audio_streaming_interfaces)) + b''.join(map(bytes, self.midi_streaming_interfaces))
        return struct.pack(self.fixed_fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bDescriptorSubtype,
                           self.bcdADC,
                           wTotalLength,
                           len(baInterfaceNr)) + baInterfaceNr + units_and_terminals + subinterfaces

class TerminalDescriptor:
    bLength = None
    bDescriptorType = None
    bDescriptorSubtype = None
    bTerminalId = None

class InputTerminalDescriptor(TerminalDescriptor):
    wTerminalType = None
    bAssocTerminal = None
    bNrChannels = None
    wChannelConfig = None
    iChannelNames = None
    iTerminal = None

class OutputTerminalDescriptor(TerminalDescriptor):
    pass

# TODO: Add unit descriptors.
