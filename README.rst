
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

.. code-block:: python

    from adafruit_usb_descriptor import standard
    from adafruit_usb_descriptor import cdc

    # langid must always be first
    langid = standard.StringDescriptor("\u0409")
    manufacturer = standard.StringDescriptor("Manufacturer name")
    product = standard.StringDescriptor("Product name")
    # Placeholder for the serial number. C code should dynamically overwrite it.
    serial_number = standard.StringDescriptor("serial number. you should fill in a unique serial number here."[:args.serial_number_length])
    strings = [langid, manufacturer, product, serial_number]

    device = standard.DeviceDescriptor(
        idVendor=0x1234,
        idProduct=0x0001,
        iManufacturer=strings.index(manufacturer),
        iProduct=strings.index(product),
        iSerialNumber=strings.index(serial_number))

    # Interface numbers are interface set local and endpoints are interface local
    # until standard.join_interfaces renumbers them.
    cdc_interfaces = [
        standard.InterfaceDescriptor(
            bInterfaceClass=0x2,  # Communications Device Class
            bInterfaceSubClass=0x02,  # Abstract control model
            bInterfaceProtocol=0x01,  # Common AT Commands
            subdescriptors=[
                cdc.Header(bcdCDC=0x0110),
                cdc.CallManagement(bmCapabilities=0x03, bDataInterface=0x01),
                cdc.AbstractControlManagement(bmCapabilities=0x02),
                cdc.Union(bMasterInterface=0x00,
                          bSlaveInterface=[0x01]),
                standard.EndpointDescriptor(
                    bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_IN,
                    bmAttributes=standard.EndpointDescriptor.TYPE_INTERRUPT,
                    wMaxPacketSize=0x8,
                    bInterval=10)
            ]
        ),
        standard.InterfaceDescriptor(
            bInterfaceClass=0x0a,
            subdescriptors=[
                standard.EndpointDescriptor(
                    bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_IN,
                    bmAttributes=standard.EndpointDescriptor.TYPE_BULK),
                standard.EndpointDescriptor(
                    bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_OUT,
                    bmAttributes=standard.EndpointDescriptor.TYPE_BULK)
            ]
        )
    ]

    msc_interfaces = [
        standard.InterfaceDescriptor(
            bInterfaceClass=0x08,
            bInterfaceSubClass=0x06,
            bInterfaceProtocol=0x50,
            subdescriptors=[
                standard.EndpointDescriptor(
                    bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_IN,
                    bmAttributes=standard.EndpointDescriptor.TYPE_BULK),
                standard.EndpointDescriptor(
                    bEndpointAddress=0x1 | standard.EndpointDescriptor.DIRECTION_OUT,
                    bmAttributes=standard.EndpointDescriptor.TYPE_BULK)
            ]
        )
    ]

    interfaces = standard.join_interfaces(cdc_interfaces, msc_interfaces)

    cdc_function = standard.InterfaceAssociationDescriptor(
        bFirstInterface=interfaces.index(cdc_interfaces[0]),
        bInterfaceCount=len(cdc_interfaces),
        bFunctionClass=0x2,  # Communications Device Class
        bFunctionSubClass=0x2,  # Abstract control model
        bFunctionProtocol=0x1)  # Common AT Commands

    configuration = standard.ConfigurationDescriptor(
        wTotalLength=(standard.ConfigurationDescriptor.bLength +
                      cdc_function.bLength +
                      sum([len(bytes(x)) for x in interfaces])),
        bNumInterfaces=len(interfaces))

    # At this point you can do bytes(<descriptor>) to convert each to a byte
    # string that can be output using normal Python code.
    # Individual descriptors:
    #   device, configuration, cdc_function
    # Lists of descriptors:
    #   interfaces, strings

At this point the output format will vary. For a full example for MicroChip's
ASF4 see `here <https://github.com/adafruit/circuitpython/blob/master/ports/atmel-samd/tools/gen_usb_descriptor.py>`_ in CircuitPython.

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
