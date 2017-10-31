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

def join_interfaces(*args):
    """Renumbers interfaces and endpoints so they are compatible.

       ``args`` is any number of interface sequences (usually lists with
       `InterfaceDescriptor` s inside them). Interfaces within a sequence
       should be numbered beginning at 0x0. Endpoints should be numbered per
       interface."""
    interfaces = []
    base_endpoint_number = 1
    for interface_set in args:
        base_interface_number = len(interfaces)
        for i, interface in enumerate(interface_set):
            interfaces.append(interface)
            interface.bInterfaceNumber = interfaces.index(interface)
            max_endpoint_address = base_endpoint_number
            for subdescriptor in interface.subdescriptors:
                if (subdescriptor.bDescriptorType ==
                        EndpointDescriptor.bDescriptorType):
                    subdescriptor.bEndpointAddress += base_endpoint_number
                    endpoint_address = subdescriptor.bEndpointAddress & 0xf
                    max_endpoint_address = max(max_endpoint_address,
                                               endpoint_address)
            base_endpoint_number = max_endpoint_address + 1
    return interfaces


class Descriptor:
    """Top-level descriptor class.

       Subclasses must provide ``bDescriptorType``, ``bLength`` and ``fields``.

       ``fields`` must be a list of tuples containing the field name, `struct`
       compatible format string and default value. If the default value is
       None, then it will be required as an argument to the constructor."""
    def __init__(self, *args, **kwargs):
        self.fmt = ["<B", "B"]
        for field in self.fields:
            self.fmt.append(field[1])
        self.fmt = "".join(self.fmt)
        if len(args) == 1:
            self.data = struct.unpack(self.fmt, args[0])
            if self.data[1] != self.bDescriptorType:
                raise RuntimeError("Descriptor type doesn't match.")
            return
        elif len(args) > 1:
            raise TypeError("Only one arg or keyword args expected.")
        elif len(kwargs) == 0:
            raise TypeError("Only one arg or keyword args expected.")

        self.data = []
        for field, _, default in self.fields:
            if field in kwargs:
                self.data.append(kwargs[field])
            elif default is not None:
                self.data.append(default)
            else:
                raise ValueError("Missing {} argument.".format(field))

    def __bytes__(self):
        return struct.pack(self.fmt, self.bLength, self.bDescriptorType,
                           *self.data)

    @property
    def bDescriptorType(self):
        return self._bDescriptorType
