from machine import UART, Pin
from time import sleep
from micropyGPS import MicropyGPS

my_gps = MicropyGPS()

gps_serial = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

latitude = 12.84
longitude = 77.67
satellites = 0

def gps_data():
    global latitude, longitude, satellites
    try:
        while gps_serial.any():
            data = gps_serial.read()
            for byte in data:
                stat = my_gps.update(chr(byte))
                if stat:  # only when a sentence is complete
                    latitude = my_gps.latitude[0] + my_gps.latitude[1] / 60.0
                    if my_gps.latitude[2] == 'S':
                        latitude = -latitude

                    longitude = my_gps.longitude[0] + my_gps.longitude[1] / 60.0
                    if my_gps.longitude[2] == 'W':
                        longitude = -longitude

                    satellites = my_gps.satellites_in_use

    except Exception as e:
        pass  # keep last known values

    return latitude, longitude, satellites
