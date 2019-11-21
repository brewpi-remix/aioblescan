Bluetooth Low Energy (BLE) Scan for BrewPi Derivatives using Tilt
=================================================================

aioblescan is a Python 3/asyncio library to listen for BLE advertized packets.  This was `originally created by François Wautier <https://github.com/frawau/aioblescan>`__ and released under the MIT license.  A `plugin for Tilt <https://github.com/baronbrew/aioblescan>`__ was created by Noah Neibaron.  This has been further modified for `BrewPi Remix <https://www.brewpiremix.com>`__, however it should be reverse-compatible with all other implementations.
 
Installation
------------

Clone the repository:

::

    git clone

Move into the Git directory:

::

    cd aioblescan

Execute the installer:

::

    sudo -H python3 setup.py install

Test using the Tilt plugin for aioblescan:

::

    sudo python3 -u -m aioblescan -T

You will see the regular Bluetooth beacons from any Tilt in range:

::

    pi@raspberrypi:~/aioblescan $ sudo python3 -u -m aioblescan -T
    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": -59, "rssi": -58, "mac": "da:d2:af:29:cd:3d"}
    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -74, "mac": "da:d2:af:29:cd:3d"}
    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -57, "mac": "da:d2:af:29:cd:3d"}

Hit `ctrl-c` to stop the scan.

Interpreting the Tilt Data
--------------------------

The information from the default plugin is returned as a valid JSON:

```
{
  "uuid": "a495bb40c5b14b44b5121370f02d74de",
  "major": 69,
  "minor": 1056,
  "tx_power": 31,
  "rssi": -49,
  "mac": "xx:xx:xx:xx:xx:xx"
}
```

These keys may be interpreted as:

- **uuid**:  Tilt name.  The "40" in a495bb`40`c5b14b44b5121370f02d74de is an indication of the color
    - 10: Red
    - 20: Green
    - 30: Black
    - 40: Purple
    - 50: Orange
    - 60: Blue
    - 70: Yellow
    - 80: Ping
- **major**: Temp in degrees F.
- **minor**: Specific gravity x1000
- **tx_power**: Weeks since battery change (0-152 when converted to unsigned 8 bit integer)
- **rssi**: Received Signal Strength Indication (RSSI) is a measurement of the power present in the received radio signal.  A lower negative number is stronger
- **mac**: Media Access Control (MAC) address of the device


Additional Information
======================

Essentially, you create a function to process the incoming information
and you attach it to the ``BTScanRequester``. You then create a
Bluetooth connection, you issue the scan command and wait for incoming
packets and process them.

You can use Eddystone, RuuviWeather or Tilt  to retrieve specific information

The easiest way is to look at the ``__main__.py`` file.

You can run the module with

::

   python3 -m aioblescan

Add ``-h`` for help.

To see the RuuviTag weather information:

::

   python3 -m aioblescan -r

You get:

::

   Weather info {'rssi': -64, 'pressure': 100300, 'temperature': 24, 'mac address': 'fb:86:84:dd:aa:bb', 'tx_power': -7, 'humidity': 36.0}
   Weather info {'rssi': -62, 'pressure': 100300, 'temperature': 24, 'mac address': 'fb:86:84:dd:aa:bb', 'tx_power': -7, 'humidity': 36.0}

To check the Eddystone beacon:

::

   python3 -m aioblescan -e

You get:

::

   Google Beacon {'tx_power': -7, 'url': 'https://ruu.vi/#BEgYAMR8n', 'mac address': 'fb:86:84:dd:aa:bb', 'rssi': -52}
   Google Beacon {'tx_power': -7, 'url': 'https://ruu.vi/#BEgYAMR8n', 'mac address': 'fb:86:84:dd:aa:bb', 'rssi': -53}


To check the Tilt beacon:

::

    python3 -m aioblescan -T

You get:

::

    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -74, "mac": "da:d2:af:29:cd:3d"}
    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -57, "mac": "da:d2:af:29:cd:3d"}

For generic advertise packet scanning:

::

   python3 -m aioblescan

You get:

::

   HCI Event:
       code:
           3e
       length:
           19
       LE Meta:
           code:
               02
           Adv Report:
               num reports:
                   1
               ev type:
                   generic adv
               addr type:
                   public
               peer:
                   54:6c:0e:aa:bb:cc
               length:
                   7
               flags:
                   Simul LE - BR/EDR (Host): False
                   Simul LE - BR/EDR (Control.): False
                   BR/EDR Not Supported: False
                   LE General Disc.: True
                   LE Limited Disc.: False
               Incomplete uuids:
                       ff:30
               rssi:
                   -67
   HCI Event:
       code:
           3e
       length:
           43
       LE Meta:
           code:
               02
           Adv Report:
               num reports:
                   1
               ev type:
                   no connection adv
               addr type:
                   random
               peer:
                   fb:86:84:dd:aa:bb
               length:
                   31
               flags:
                   Simul LE - BR/EDR (Host): False
                   Simul LE - BR/EDR (Control.): False
                   BR/EDR Not Supported: False
                   LE General Disc.: True
                   LE Limited Disc.: True
               Complete uuids:
                       fe:aa
               Advertised Data:
                   Service Data uuid:
                       fe:aa
                   Adv Payload:
                       10:f9:03:72:75:75:2e:76:69:2f:23:42:45:77:59:41:4d:52:38:6e
               rssi:
                   -59

Here the first packet is from a Wynd device, the second from a Ruuvi Tag

aioblescan can also send EddyStone advertising. Try the -a flag when
running the module.

FAQ
===

Q. Why not use scapy?

A. Scapy is great and you can execute the following to get things going. But, the great thing with Scapy is that there is so many versions to choose from.... and not all have all the same functions ... and installation can be haphazard, with some version not installing at all. Also scapy includes a lot of other protocols and could be an overkill... lastly it is never too late to learn.

::

        import scapy.all as sa
        test=sa.BluetoothHCISocket(0)
        command=sa.HCI_Cmd_LE_Set_Scan_Enable(enable=1,filter_dups=0)
        chdr=sa.HCI_Command_Hdr(len=len(command))
        hdr=sa.HCI_Hdr(type=1)
        test.send(hdr / chdr / command)


Q. What can you track?

A. aioblescan will try to parse all the incoming advertised information. You can see the raw data when it does not know what to do. With Eddystone beacon you can see the URL, Telemetry and UID

