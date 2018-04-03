
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-usb-descriptor/badge/?version=latest
    :target: http://adafruit-usb-descriptor.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

The `adafruit_usb_descriptor` library provides Python classes that make it
easier to generate a binary USB descriptor. It can be used in place of a series
of C macros.

Dependencies
=============
This library has no external dependencies. It only uses Python `struct`.

Usage Example
=============

A current usage example that generates descriptors MicroChip's
ASF4 can be found `here <https://github.com/adafruit/circuitpython/blob/master/ports/atmel-samd/tools/gen_usb_descriptor.py>`_ in CircuitPython.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/usb_descriptor/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

API Reference
=============

.. toctree::
   :maxdepth: 2

   api
