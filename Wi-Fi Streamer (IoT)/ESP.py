from machine import UART, Pin
import time
from INTERNAL_SENSOR_STREAM import *
from ROBOT_CONFIGURATIONS import *
from GPS_DATA_STREAM import *

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

password = "Maverick@1"
port = "80"
ip_address = "192.168.4.1"
latency = "0.05"

def send_at_command(command, delay=float(latency)):
    """Sends AT command to ESP-01 and waits for response."""
    uart.write(command + "\r\n")
    time.sleep(delay)
    if uart.any():
        response = uart.read().decode()
        #print(f"Response: {response}")
        return response
    return ""

def get_mac_address():
    """Retrieves the MAC address of the ESP-01."""
    response = send_at_command("AT+CIFSR")  # Get IP and MAC address information
    for line in response.splitlines():
        if "MAC" in line:
            mac = line.split("\"")[1]  # Extract MAC address from response
            #print(f"MAC Address: {mac}")
            return mac.replace(":", "")[-6:]  # Use last 6 characters for uniqueness
    return "UNKNOWN"

global mac_suffix

def setup_esp_as_server():
    global mac_suffix    
    mac_suffix = get_mac_address()
    ssid = f"PilotX Maverick@{mac_suffix}"
        
    send_at_command("AT+RST", 2)                       # Reset ESP-01
    send_at_command("AT+CWMODE=2")                     # Set to Access Point mode
    send_at_command(f'AT+CWSAP="{ssid}","{password}",1,3')  # Set up AP with SSID and password
    send_at_command("AT+CIPMUX=1")                     # Enable multiple connections
    send_at_command(f"AT+CIPSERVER=1,{port}")
    send_at_command("AT+CIFSR") # Start server on port 80

def send_data():
    from ROBOT_ACTIONS import read_left_ir, read_right_ir, obstacle_distance

    global mac_suffix
    """Continuously sends data packets to any client connected to the ESP-01."""
    count = 0
    while True:
        ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()
        left_ir_value = read_left_ir()
        right_ir_value = read_right_ir()
        distance = obstacle_distance()
        latitude, longitude, satellites = gps_data()
        
        data = [ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude,left_ir_value, right_ir_value, distance, latitude, longitude, satellites, battery_voltage, mac_suffix]
        data_string = ",".join(map(str, data)) + "\n"
        
        # Send data over UART to ESP-01
        send_at_command(f'AT+CIPSEND=0,{len(data_string)}')   # Specify the data length
        uart.write(data_string)                               # Send the actual data
        count += 1
        time.sleep(float(latency))                                 # Send data every second


setup_esp_as_server()
