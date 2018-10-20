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

"""
Audio specific descriptors
================================

* Author(s): Scott Shawcroft
"""

AUDIO_CLASS_DEVICE = 0x01

AUDIO_SUBCLASS_UNKNOWN = 0x00
AUDIO_SUBCLASS_CONTROL = 0x01
AUDIO_SUBCLASS_AUDIO_STREAMING = 0x02
AUDIO_SUBCLASS_MIDI_STREAMING = 0x03

AUDIO_PROTOCOL_V1 = 0x0
AUDIO_PROTOCOL_V2 = 0x20
AUDIO_PROTOCOL_V3 = 0x30
