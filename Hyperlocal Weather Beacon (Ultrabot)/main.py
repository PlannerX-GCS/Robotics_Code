from machine import UART, Pin, ADC
from ROBOT_ACTIONS import *
from math import *
import time

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

data = data_stream("USB")

sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)

reading = sensor_temp.read_u16() 
voltage = reading * conversion_factor
temperature = 21 - (voltage - 0.706) / 0.001721

offset = 10

rain_meter = Pin(10, Pin.IN)
air_quality_meter = Pin(11, Pin.IN)

pin7 = Pin(7, Pin.OUT)
pin8 = Pin(8, Pin.OUT)
pin9 = Pin(9, Pin.OUT)

pin7.value(1)
pin8.value(0)
pin9.value(0)

def average(data1, data2):
    return (data1 + data2) / 2

def send_at(cmd, delay=2):
    print("\n>>", cmd)
    uart.write(cmd + '\r\n')
    time.sleep(delay)
    if uart.any():
        response = uart.read().decode()
        print(response)
        return response
    return ""

# Wi-Fi & ThingSpeak credentials
ssid = "JOHNSRIVASTAVA 2445"
password = "abcdefgh"
api_key = "46TMPY5G8DW8ZKYR"
host = "api.thingspeak.com"

# 1. Initialize ESP-01
send_at("AT+RST", 2)
send_at("AT+CWMODE=1")
send_at(f'AT+CWJAP="{ssid}","{password}"', 8)
send_at("AT+CIFSR", 2)  # Show IP to confirm connection

# 2. Send data loop
i = 0
while True:
    rain_drop = 1 - rain_meter.value()   # Read pin value (0 or 1)
    air_quality = 1 - air_quality_meter.value()  # Read pin value (0 or 1)
    
    i += 1
    
    reading = sensor_temp.read_u16()  # 16-bit analog reading
    voltage = reading * conversion_factor
    
    Temp_Sensor_1 = 21 - (voltage - 0.706) / 0.001721
    Temp_Sensor_2 = data[9]+offset
    True_Temp = data[9]-offset
    Pressure = data[10]

    print(rain_drop)
    if rain_drop == 1:
        pin9.value(1)
    elif rain_drop == 0:
        pin9.value(0)
    
    # Format HTTP GET request for all 5 fields
    url = f"/update?api_key={api_key}&field1={Temp_Sensor_1:.2f}&field2={Temp_Sensor_2:.2f}&field3={True_Temp}&field4={Pressure}&field5={rain_drop}&field6={air_quality}"
    http = f"GET {url} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    # Send to ThingSpeak
    send_at(f'AT+CIPSTART="TCP","{host}",80', 4)
    send_at(f'AT+CIPSEND={len(http)}', 2)
    uart.write(http)
    
    pin8.value(1)
    time.sleep(1)
    pin8.value(0)
    
    time.sleep(15)

