## Micropython implementation of Buderus KM100 to influxdb logger

This project implements a proof of concept on how to read out data from the Buderus KM100 internet gateway of different heating systems and log them to influxdb.

### Installation
* Install micropython on your device.
* Copy config.py.sample to config.py and edit your settings
    * Use the internet to find out how to put the right AES key for your device
    * configure the IP of the KM100 and the host & credentials to your influxdb
* It uses `urequests` and `traceback` from micropython-lib, as I was too stupid to figure out how to use the 
  bundled libraries, I added them to the working directory.

### Run
I run this on a ATH79 OpenWRT device (WDR3600) which works fine, as long as I restart the python script every few hours.
There seems to be a memory leak which is not visible in python stack, e.g. I suspect it in the ssl or socket bindings.
That is why there is `run.sh` which runs the micropython script `run.py` in an endless loop; The python script exits itself after a hundred so points
have been captured. See the script for details.

Feel free to instal the `log_buderus` procd init script on your device.
