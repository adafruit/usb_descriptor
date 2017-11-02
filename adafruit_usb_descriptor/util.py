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

from . import standard

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
                        standard.EndpointDescriptor.bDescriptorType):
                    subdescriptor.bEndpointAddress += base_endpoint_number
                    endpoint_address = subdescriptor.bEndpointAddress & 0xf
                    max_endpoint_address = max(max_endpoint_address,
                                               endpoint_address)
            base_endpoint_number = max_endpoint_address + 1
    return interfaces
