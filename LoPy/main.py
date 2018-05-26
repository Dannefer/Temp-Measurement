# main.py

# Import libraries
from loranetwork import LoraNetwork
import pycom
from time import sleep
from machine import Pin
from onewire import DS18X20
from onewire import OneWire
from deepsleep import DeepSleep
from machine import SD

# Set LED off
pycom.heartbeat(False)
# Set Wifi off
pycom.wifi_on_boot(False)

# Address DeepSleep as ds
ds = DeepSleep()

# Mounts SD-card onto pycom board and calls file /sd
sd = SD()
os.mount(sd, '/sd')

# Address LoraNetwork to ln and set blocking off
ln = LoraNetwork()
ln.connect(False)

# Address temperature measurements to temp
ow = OneWire(Pin('P9'))
temp = DS18X20(ow)

# Aquire temperature measurement
temp.start_convertion()

# Open an appendable file at /sd/test.txt and write [
f = open('/sd/measurements.txt', 'a')
f.write("[")

# Start and record temperature measurement for 12 cycles
for cycles in range(12):
    # Measure temperature and address it to tmp
    tmp = temp.read_temp_async()
    temp.start_convertion()
    print(tmp)
    #sleep(5)
    # Write the tmp to SD and TTN, if it's not None
    if tmp != None:
        #print("Writing to SD-Card")
        f.write(str(tmp)+",")
        #sleep(5)
        #print("Sending with LoRaWAN")
        ln.send(str(tmp))
    # Sleep for 5 seconds
    sleep(5)

# Writes ] to SD and closes the file
f.write("]")
f.close()

# Deepsleep for 3540 seconds (59 minutes)
ds.go_to_sleep(3540)
