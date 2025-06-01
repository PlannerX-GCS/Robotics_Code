from machine import UART, Pin
from time import sleep
from micropyGPS import MicropyGPS

my_gps = MicropyGPS()

gps_serial = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

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
                if stat is not None:
                    latitude = my_gps.latitude_string()
                    longitude = my_gps.longitude_string()
                    satellites = my_gps.satellites_in_use
                else:
                    latitude = 12.84
                    longitude = 77.67
                    satellites = 0
            
    except Exception as e:
        latitude = 12.84
        longitude = 77.67
        satellites = 0
        
    return latitude, longitude, satellites
