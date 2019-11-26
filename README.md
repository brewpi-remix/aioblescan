# Bluetooth Low Energy (BLE) Scan for BrewPi Derivatives using Tilt

aioblescan is a Python 3/asyncio library to listen for BLE advertized packets.  This was [originally created by François Wautier](https://github.com/frawau/aioblescan) and released under the MIT license.  A [plugin for Tilt](https://github.com/baronbrew/aioblescan) was created by Noah Neibaron.  This has been further modified for [BrewPi Remix](https://www.brewpiremix.com), however it should be reverse-compatible with all other implementations.

## Installation

Clone the repository:

    git clone https://github.com/brewpi-remix/aioblescan.git

Move into the Git directory:

    cd aioblescan

Execute the installer:

    sudo -H python3 setup.py install

Test using the Tilt plugin for aioblescan:

    sudo python3 -u -m aioblescan -T

You will see the regular Bluetooth beacons from any Tilt in range:

    pi@brewpi:~/aioblescan $ sudo python3 -u -m aioblescan -T
    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -58, "mac": "xx:xx:xx:xx:xx:xx"}
    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -74, "mac": "xx:xx:xx:xx:xx:xx"}
    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -57, "mac": "xx:xx:xx:xx:xx:xx"}

Hit `ctrl-c` to stop the scan.

## Interpreting the Tilt Data

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

- **uuid**:  Tilt name.  The "40" in a495bb`40`c5b14b44b5121370f02d74de is an indication of the color.
    - 10: Red
    - 20: Green
    - 30: Black
    - 40: Purple
    - 50: Orange
    - 60: Blue
    - 70: Yellow
    - 80: Pink
- **major**: Temp in degrees F.
- **minor**: Specific gravity x1000.
- **tx_power**: Weeks since battery change (0-152 when converted to unsigned 8 bit integer).  You will occasionally see `-59` which is there to allow iOS to compute RSSI.  This value should be discarded.
- **rssi**: Received Signal Strength Indication (RSSI) is a measurement of the power present in the received radio signal.  A lower negative number is stronger.
- **mac**: Media Access Control (MAC) address of the device.

## Additional Information

Essentially, you create a function to process the incoming
information and you attach it to the `BTScanRequester`. You then create a Bluetooth
connection, you issue the scan command and wait for incoming packets and process them.

You can use Eddystone, RuuviWeather or Tilt to retrieve specific information

The easiest way is to look at the `__main__.py` file.

You can run the module with

    python3 -m aioblescan

Add `-h` for help.

To see the RuuviTag weather information try:

    python3 -m aioblescan -r

You will get

    Weather info {'rssi': -64, 'pressure': 100300, 'temperature': 24, 'mac address': 'fb:86:84:dd:aa:bb', 'tx_power': -7, 'humidity': 36.0}
    Weather info {'rssi': -62, 'pressure': 100300, 'temperature': 24, 'mac address': 'fb:86:84:dd:aa:bb', 'tx_power': -7, 'humidity': 36.0}

To check the Eddystone beacon

    python3 -m aioblescan -e

You get

    Google Beacon {'tx_power': -7, 'url': 'https://ruu.vi/#BEgYAMR8n', 'mac address': 'fb:86:84:dd:aa:bb', 'rssi': -52}
    Google Beacon {'tx_power': -7, 'url': 'https://ruu.vi/#BEgYAMR8n', 'mac address': 'fb:86:84:dd:aa:bb', 'rssi': -53}

To check the Tilt beacon:

    python3 -m aioblescan -T

You get

    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -74, "mac": "xx:xx:xx:xx:xx:xx"}
    {"uuid": "a495bb40c5b14b44b5121370f02d74de", "major": 70, "minor": 1054, "tx_power": 31, "rssi": -57, "mac": "xx:xx:xx:xx:xx:xx"}

For a generic advertise packet scanning

    python3 -m aioblescan

You get

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

Here the first packet is from a Wynd device, the second from a Ruuvi Tag.
