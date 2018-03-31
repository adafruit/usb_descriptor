
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

    # args defines some command-line arguments.

    langid = standard.StringDescriptor("\u0409")
    manufacturer = standard.StringDescriptor(args.manufacturer)
    product = standard.StringDescriptor(args.product)
    serial_number = standard.StringDescriptor("serial number. you should fill in a unique serial number here."[:args.serial_number_length])
    strings = [langid, manufacturer, product, serial_number]

    # vid = 0x239A
    # pid = 0x8021

    device = standard.DeviceDescriptor(
        description="top",
        idVendor=args.vid,
        idProduct=args.pid,
        iManufacturer=strings.index(manufacturer),
        iProduct=strings.index(product),
        iSerialNumber=strings.index(serial_number))

    # Interface numbers are interface set local and endpoints are interface local
    # until core.join_interfaces renumbers them.
    cdc_interfaces = [
        standard.InterfaceDescriptor(
            description="CDC comm",
            bInterfaceClass=cdc.CDC_CLASS_COMM,  # Communications Device Class
            bInterfaceSubClass=cdc.CDC_SUBCLASS_ACM,  # Abstract control model
            bInterfaceProtocol=cdc.CDC_PROTOCOL_V25TER,  # Common AT Commands
            subdescriptors=[
                # Working 2.x
                # radix: hexadecimal
                # 05 24 00 10 01 header
                # 05 24 01 03 01 call manage
                # 04 24 02 06 acm
                # 05 24 06 00 01 union
                cdc.Header(
                    description="CDC comm",
                    bcdCDC=0x0110),
                cdc.CallManagement(
                    description="CDC comm",
                    bmCapabilities=0x03,
                    bDataInterface=0x01),
                cdc.AbstractControlManagement(
                    description="CDC comm",
                    bmCapabilities=0x02),
                cdc.Union(
                    description="CDC comm",
                    bMasterInterface=0x00,
                    bSlaveInterface_list=[0x01]),
                standard.EndpointDescriptor(
                    description="CDC comm in",
                    bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_IN,
                    bmAttributes=standard.EndpointDescriptor.TYPE_INTERRUPT,
                    wMaxPacketSize=0x0040,
                    bInterval=0x10)
            ]
        ),
        standard.InterfaceDescriptor(
            description="CDC data",
            bInterfaceClass=cdc.CDC_CLASS_DATA,
            subdescriptors=[
                standard.EndpointDescriptor(
                    description="CDC data in",
                    bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_IN,
                    bmAttributes=standard.EndpointDescriptor.TYPE_BULK),
                standard.EndpointDescriptor(
                    description="CDC data out",
                    bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_OUT,
                    bmAttributes=standard.EndpointDescriptor.TYPE_BULK)
            ]
        )
    ]

    msc_interfaces = [
        standard.InterfaceDescriptor(
            description="MSC",
            bInterfaceClass=msc.MSC_CLASS,
            bInterfaceSubClass=msc.MSC_SUBCLASS_TRANSPARENT,
            bInterfaceProtocol=msc.MSC_PROTOCOL_BULK,
            subdescriptors=[
                standard.EndpointDescriptor(
                    description="MSC in",
                    bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_IN,
                    bmAttributes=standard.EndpointDescriptor.TYPE_BULK),
                standard.EndpointDescriptor(
                    description="MSC out",
                    bEndpointAddress=0x1 | standard.EndpointDescriptor.DIRECTION_OUT,
                    bmAttributes=standard.EndpointDescriptor.TYPE_BULK)
            ]
        )
    ]

    hid_report_descriptor = hid.ReportDescriptor.MOUSE_KEYBOARD_CONSUMER_SYS_CONTROL_REPORT
    hid_report_ids = hid.ReportDescriptor.REPORT_IDS
    hid_report_lengths = hid.ReportDescriptor.REPORT_LENGTHS
    hid_max_report_length = max(hid_report_lengths.values())

    hid_endpoint_in_descriptor = standard.EndpointDescriptor(
        description="HID in",
        bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_IN,
        bmAttributes=standard.EndpointDescriptor.TYPE_INTERRUPT,
        wMaxPacketSize=hid_max_report_length + 1, # +1 for the Report ID
        bInterval=0x02)

    hid_endpoint_out_descriptor = standard.EndpointDescriptor(
        description="HID out",
        bEndpointAddress=0x0 | standard.EndpointDescriptor.DIRECTION_OUT,
        bmAttributes=standard.EndpointDescriptor.TYPE_INTERRUPT)

    hid_interfaces = [
        standard.InterfaceDescriptor(
            description="HID Keyboard",
            bInterfaceClass=hid.HID_CLASS,
            bInterfaceSubClass=hid.HID_SUBCLASS_NOBOOT,
            bInterfaceProtocol=hid.HID_PROTOCOL_KEYBOARD,
            subdescriptors=[
                hid.HIDDescriptor(wDescriptorLength=len(bytes(hid_report_descriptor))),
                hid_endpoint_in_descriptor,
                hid_endpoint_out_descriptor,
                ]
            ),
        ]

    # This will renumber the endpoints to make them unique across descriptors.
    interfaces = util.join_interfaces(cdc_interfaces, msc_interfaces, hid_interfaces)

    cdc_function = standard.InterfaceAssociationDescriptor(
        description="CDC function",
        bFirstInterface=interfaces.index(cdc_interfaces[0]),
        bInterfaceCount=len(cdc_interfaces),
        bFunctionClass=0x2,  # Communications Device Class
        bFunctionSubClass=0x2,  # Abstract control model
        bFunctionProtocol=0x1)  # Common AT Commands

    configuration = standard.ConfigurationDescriptor(
        description="Composite configuration",
        wTotalLength=(standard.ConfigurationDescriptor.bLength +
                      cdc_function.bLength +
                      sum([len(bytes(x)) for x in interfaces])),
        bNumInterfaces=len(interfaces))

    descriptor_list = [device, configuration, cdc_function]
    descriptor_list.extend(interfaces)
    descriptor_list.extend(strings)

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
