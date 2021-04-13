# The MIT License (MIT)
#
# Copyright (c) 2018 Dan Halbert for Adafruit Industries
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

from .standard import Descriptor

"""
HID specific descriptors
========================

* Author(s): Dan Halbert
"""

HID_CLASS = 0x03

# Many other subclasses omitted.

HID_SUBCLASS_NOBOOT = 0x00
HID_SUBCLASS_BOOT = 0x01

HID_PROTOCOL_NONE = 0x00
HID_PROTOCOL_KEYBOARD = 0x01
HID_PROTOCOL_MOUSE = 0x02

class HIDDescriptor(Descriptor):
    """Lists upcoming HID report descriptors."""
    bDescriptorType = 0x21
    fmt = "<BB" + "HBBBH"
    bLength = struct.calcsize(fmt)

    def __init__(self, *,
                 description,
                 bcdHID=0x0111,
                 bCountryCode=0x0,
                 bNumDescriptors=1,
                 bDescriptorType_Class=0x22,
                 wDescriptorLength):
        self.description = description
        self.bcdHID = bcdHID
        self.bCountryCode = bCountryCode
        self.bNumDescriptors = bNumDescriptors
        self.bDescriptorType_Class = bDescriptorType_Class
        self.wDescriptorLength = wDescriptorLength

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return struct.pack(self.fmt,
                           self.bLength,
                           self.bDescriptorType,
                           self.bcdHID,
                           self.bCountryCode,
                           self.bNumDescriptors,
                           self.bDescriptorType_Class,
                           self.wDescriptorLength)

class ReportDescriptor:
    """Describes multiple kinds of reports sent by this HID device.
    """

    def __init__(self, *,
                 description,
                 usage_page,
                 usage,
                 report_length,
                 out_report_length,
                 report_id=0,
                 report_descriptor_before_report_id,
                 report_descriptor_after_report_id,
    ):
        self.description = description
        self.usage_page = usage_page
        self.usage = usage
        self.report_length = report_length
        self.out_report_length = out_report_length
        self.report_id = report_id
        self.report_descriptor_before_report_id = report_descriptor_before_report_id
        self.report_descriptor_after_report_id = report_descriptor_after_report_id

    def report_id_bytes(self):
        """If report_id is None, no report_id is included."""
        if self.report_id is None:
            return b""
        else:
            return bytes((0x85, self.report_id))

    def report_id_index(self):
        """Return the location of the Report ID in the descriptor."""
        if self.report_id is None:
            return None
        return len(self.report_descriptor_before_report_id)

    def notes(self):
        return [str(self)]

    def __bytes__(self):
        return (
            self.report_descriptor_before_report_id +
            self.report_id_bytes() +
            self.report_descriptor_after_report_id)

    @staticmethod
    def keyboard(report_id):
        return ReportDescriptor(
            description="KEYBOARD",
            usage_page=0x01,
            usage=0x06,
            report_length=8,
            out_report_length=1,
            report_id=report_id,
            report_descriptor_before_report_id=(
                # Regular keyboard
                b"\x05\x01"  # Usage Page (Generic Desktop)
                b"\x09\x06"  # Usage (Keyboard)
                b"\xA1\x01"  # Collection (Application)
            ),
            report_descriptor_after_report_id=(
                b"\x05\x07"  #   Usage Page (Keyboard)
                b"\x19, 224"  #   Usage Minimum (224)
                b"\x29, 231"  #   Usage Maximum (231)
                b"\x15\x00"  #   Logical Minimum (0)
                b"\x25\x01"  #   Logical Maximum (1)
                b"\x75\x01"  #   Report Size (1)
                b"\x95\x08"  #   Report Count (8)
                b"\x81\x02"  #   Input (Data, Variable, Absolute)
                b"\x81\x01"  #   Input (Constant)
                b"\x19\x00"  #   Usage Minimum (0)
                b"\x29\xDD"  #   Usage Maximum (221)
                b"\x15\x00"  #   Logical Minimum (0)
                b"\x25\xDD"  #   Logical Maximum (221)
                b"\x75\x08"  #   Report Size (8)
                b"\x95\x06"  #   Report Count (6)
                b"\x81\x00"  #   Input (Data, Array)
                b"\x05\x08"  #   Usage Page (LED)
                b"\x19\x01"  #   Usage Minimum (1)
                b"\x29\x05"  #   Usage Maximum (5)
                b"\x15\x00"  #   Logical Minimum (0)
                b"\x25\x01"  #   Logical Maximum (1)
                b"\x75\x01"  #   Report Size (1)
                b"\x95\x05"  #   Report Count (5)
                b"\x91\x02"  #   Output (Data, Variable, Absolute)
                b"\x95\x03"  #   Report Count (3)
                b"\x91\x01"  #   Output (Constant)
                b"\xC0,"  # End Collection
            ),
        )

    @staticmethod
    def mouse(report_id):
        return ReportDescriptor(
            description="MOUSE",
            usage_page=0x01,
            usage=0x02,
            report_length=4,
            out_report_length=0,
            report_id=report_id,
            report_descriptor_before_report_id=(
                # Regular mouse
                b"\x05\x01"  # Usage Page (Generic Desktop)
                b"\x09\x02"  # Usage (Mouse)
                b"\xA1\x01"  # Collection (Application)
                b"\x09\x01"  #   Usage (Pointer)
                b"\xA1\x00"  #   Collection (Physical)
            ),
            report_descriptor_after_report_id=(
                b"\x05\x09"  #     Usage Page (Button)
                b"\x19\x01"  #     Usage Minimum (1)
                b"\x29\x05"  #     Usage Maximum (5)
                b"\x15\x00"  #     Logical Minimum (0)
                b"\x25\x01"  #     Logical Maximum (1)
                b"\x95\x05"  #     Report Count (5)
                b"\x75\x01"  #     Report Size (1)
                b"\x81\x02"  #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
                b"\x95\x01"  #     Report Count (1)
                b"\x75\x03"  #     Report Size (3)
                b"\x81\x01"  #     Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
                b"\x05\x01"  #     Usage Page (Generic Desktop Ctrls)
                b"\x09\x30"  #     Usage (X)
                b"\x09\x31"  #     Usage (Y)
                b"\x15\x81"  #     Logical Minimum (-127)
                b"\x25\x7F"  #     Logical Maximum (127)
                b"\x75\x08"  #     Report Size (8)
                b"\x95\x02"  #     Report Count (2)
                b"\x81\x06"  #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
                b"\x09\x38"  #     Usage (Wheel)
                b"\x15\x81"  #     Logical Minimum (-127)
                b"\x25\x7F"  #     Logical Maximum (127)
                b"\x75\x08"  #     Report Size (8)
                b"\x95\x01"  #     Report Count (1)
                b"\x81\x06"  #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
                b"\xC0,"  #   End Collection
                b"\xC0,"  # End Collection
            ),
        )

    @staticmethod
    def consumer_control(report_id):
        return ReportDescriptor(
            description="CONSUMER",
            usage_page=0x0C,
            usage=0x01,
            report_length=2,
            out_report_length=0,
            report_id=report_id,
            report_descriptor_before_report_id=(
                # Consumer ("multimedia") keys
                b"\x05\x0C"  # Usage Page (Consumer)
                b"\x09\x01"  # Usage (Consumer Control)
                b"\xA1\x01"  # Collection (Application)
            ),
            report_descriptor_after_report_id=(
                b"\x75\x10"  #   Report Size (16)
                b"\x95\x01"  #   Report Count (1)
                b"\x15\x01"  #   Logical Minimum (1)
                b"\x26\x8C\x02"  #   Logical Maximum (652)
                b"\x19\x01"  #   Usage Minimum (Consumer Control)
                b"\x2A\x8C\x02"  #   Usage Maximum (AC Send)
                b"\x81\x00"  #   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
                b"\xC0,"  # End Collection
            ),
        )

    @staticmethod
    def sys_control(report_id):
        return ReportDescriptor(
            description="SYS_CONTROL",
            usage_page=0x01,
            usage=0x80,
            report_length=1,
            out_report_length=0,
            report_id=report_id,
            report_descriptor_before_report_id=(
                # Power controls
                b"\x05\x01"  # Usage Page (Generic Desktop Ctrls)
                b"\x09\x80"  # Usage (Sys Control)
                b"\xA1\x01"  # Collection (Application)
            ),
            report_descriptor_after_report_id=(
                b"\x75\x02"  #   Report Size (2)
                b"\x95\x01"  #   Report Count (1)
                b"\x15\x01"  #   Logical Minimum (1)
                b"\x25\x03"  #   Logical Maximum (3)
                b"\x09\x82"  #   Usage (Sys Sleep)
                b"\x09\x81"  #   Usage (Sys Power Down)
                b"\x09\x83"  #   Usage (Sys Wake Up)
                b"\x81\x60"  #   Input (Data,Array,Abs,No Wrap,Linear,No Preferred State,Null State)
                b"\x75\x06"  #   Report Size (6)
                b"\x81\x03"  #   Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
                b"\xC0,"  # End Collection
            ),
        )

    @staticmethod
    def gamepad(report_id):
        return ReportDescriptor(
            description="GAMEPAD",
            usage_page=0x01,
            usage=0x05,
            report_length=6,
            out_report_length=0,
            report_id=report_id,
            report_descriptor_before_report_id=(
                b"\x05\x01"  # Usage Page (Generic Desktop)
                b"\x05\x05"  # Usage (Keyboard)
                b"\xA1\x01"  # Collection (Application)
            ),
            report_descriptor_after_report_id=(
                b"\x05\x09"  #   Usage Page (Button)
                b"\x19\x01"  #   Usage Minimum (Button 1)
                b"\x29\x10"  #   Usage Maximum (Button 16)
                b"\x15\x00"  #   Logical Minimum (0)
                b"\x25\x01"  #   Logical Maximum (1)
                b"\x75\x01"  #   Report Size (1)
                b"\x95\x10"  #   Report Count (16)
                b"\x81\x02"  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
                b"\x05\x01"  #   Usage Page (Generic Desktop Ctrls)
                b"\x15\x81"  #   Logical Minimum (-127)
                b"\x25\x7F"  #   Logical Maximum (127)
                b"\x09\x30"  #   Usage (X)
                b"\x09\x31"  #   Usage (Y)
                b"\x09\x32"  #   Usage (Z)
                b"\x09\x35"  #   Usage (Rz)
                b"\x75\x08"  #   Report Size (8)
                b"\x95\x04"  #   Report Count (4)
                b"\x81\x02"  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
                b"\xC0,"  # End Collection
            ),
        )

    @staticmethod
    def digitizer(report_id):
        return ReportDescriptor(
            description="DIGITIZER",
            usage_page=0x0D,
            usage=0x02,
            report_length=5,
            out_report_length=0,
            report_descriptor_before_report_id=(
                b"\x05\x0D"  # Usage Page (Digitizers)
                b"\x09\x02"  # Usage (Pen)
                b"\xA1\x01"  # Collection (Application)
            ),
            report_descriptor_after_report_id=(
                b"\x09\x01"  #   Usage (Stylus)
                b"\xA1\x00"  #   Collection (Physical)
                b"\x09\x32"  #     Usage (In-Range)
                b"\x09\x42"  #     Usage (Tip Switch)
                b"\x09\x44"  #     Usage (Barrel Switch)
                b"\x09\x45"  #     Usage (Eraser Switch)
                b"\x15\x00"  #     Logical Minimum (0)
                b"\x25\x01"  #     Logical Maximum (1)
                b"\x75\x01"  #     Report Size (1)
                b"\x95\x04"  #     Report Count (4)
                b"\x81\x02"  #     Input (Data,Var,Abs)
                b"\x75\x04"  #     Report Size (4) -- Filler
                b"\x95\x01"  #     Report Count (1) -- Filler
                b"\x81\x01"  #     Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
                b"\x05\x01"  #     Usage Page (Generic Desktop Ctrls)
                b"\x15\x00"  #     Logical Minimum (0)
                b"\x26\xFF\x7F"  #     Logical Maximum (32767)
                b"\x09\x30"  #     Usage (X)
                b"\x09\x31"  #     Usage (Y)
                b"\x75\x10"  #     Report Size (16)
                b"\x95\x02"  #     Report Count (2)
                b"\x81\x02"  #     Input (Data,Var,Abs)
                b"\xC0,"  #   End Collection
                b"\xC0,"  # End Collection
            ),
        )

    @staticmethod
    def xac_compatible_gamepad(report_id):
        return ReportDescriptor(
            description="XAC_COMPATIBLE_GAMEPAD",
            usage_page=0x01,
            usage=0x05,
            report_length=3,
            out_report_length=0,
            report_descriptor_before_report_id=(
                b"\x05\x01"  #  Usage Page (Desktop)
                b"\x09\x05"  #  Usage (Gamepad)
                b"\xA1\x01"  #  Collection (Application)
            ),
            report_descriptor_after_report_id=(
                b"\x15\x00"  #      Logical Minimum (0)
                b"\x25\x01"  #      Logical Maximum (1)
                b"\x35\x00"  #      Physical Minimum (0)
                b"\x45\x01"  #      Physical Maximum (1)
                b"\x75\x01"  #      Report Size (1)
                b"\x95\x08"  #      Report Count (8)
                b"\x05\x09"  #      Usage Page (Button)
                b"\x19\x01"  #      Usage Minimum (1)
                b"\x29\x08"  #      Usage Maximum (8)
                b"\x81\x02"  #      Input (Variable)
                b"\x05\x01"  #      Usage Page (Desktop)
                b"\x26\xFF\x00"  #      Logical Maximum (255)
                b"\x46\xFF\x00"  #      Physical Maximum (255)
                b"\x09\x30"  #      Usage (X)
                b"\x09\x31"  #      Usage (Y)
                b"\x75\x08"  #      Report Size (8)
                b"\x95\x02"  #      Report Count (2)
                b"\x81\x02"  #      Input (Variable)
                b"\xC0,"  #  End Collection
            ),
        )

    @staticmethod
    def raw():
        return ReportDescriptor(
            description="RAW",
            usage_page=0xFFAF,
            usage=0xAF,
            report_length=64,
            out_report_length=0,
            report_id=None,
            report_descriptor_before_report_id=(
                b"\x06\xAF\xFF"  #  Usage Page (Vendor 0xFFAF "Adafruit")
                b"\x09\xAF"  #  Usage (AF)
                b"\xA1\x01"  #  Collection (Application)
                b"\x75\x08"  #      Report Size (8)
                b"\x15\x00"  #      Logical Minimum (0)
                b"\x26\xFF\x00"  #      Logical Maximum (255)
                b"\x95\x08"  #      Report Count (8)
                b"\x09\x01"  #      Usage(xxx)
                b"\x81\x02"  #      Input (Variable)
                b"\x95\x08"  #      Report Count (8)
                b"\x09\x02"  #      Usage(xxx)
                b"\x91\x02"  #      Input (Variable)
                b"\xC0,"  #  End Collection
            ),
            report_descriptor_after_report_id=b"",
        )
