from machine import UART, Pin
from time import sleep
import re
from collections import deque
import math
from ROBOT_ACTIONS import *

esp = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
esp.init(115200, bits=8, parity=None, stop=1)

clean_lcd()
write_on_lcd("Searching", 0, 4)
write_on_lcd("Network", 1, 5)

def send_at(cmd, delay=3):
    esp.write((cmd + "\r\n").encode())
    sleep(delay)
    response = esp.read()
    if response:
        return response.decode("utf-8")  # <== FIX HERE
    return ""

def estimate_distance(rssi, tx_power=-40, path_loss=2.0):
    return round(10 ** ((tx_power - rssi) / (10 * path_loss)), 2)

send_at("AT+RST", 2)
send_at("AT+CWMODE=1", 1)

signal_history = {}  # BSSID -> deque of RSSI
ssid_lookup = {}     # BSSID -> SSID
channel_lookup = {}  # BSSID -> Channel
encryption_lookup = {}  # BSSID -> Encryption

while True:
    data = send_at("AT+CWLAP", 5)

    for line in data.splitlines():
        if not line.startswith("+CWLAP:"):
            continue

        try:
            raw = line[len("+CWLAP:("):].rstrip(")")
            parts = raw.split(",")

            encryption = int(parts[0])
            ssid = parts[1].strip('"')
            rssi = int(parts[2])
            bssid = parts[3].strip('"')
            channel = int(parts[4])
        except:
            continue

        if bssid not in signal_history:
            signal_history[bssid] = deque([], 3)

        signal_history[bssid].append(rssi)
        ssid_lookup[bssid] = ssid
        channel_lookup[bssid] = channel
        encryption_lookup[bssid] = encryption

    display_list = []

    for bssid, rssi_list in signal_history.items():
        if len(rssi_list) < 2:
            continue  # wait for multiple samples

        avg_rssi = round(sum(rssi_list) / len(rssi_list), 1)
        distance = estimate_distance(avg_rssi)
        ssid = ssid_lookup[bssid]
        display_list.append((ssid, avg_rssi, distance))

    display_list.sort(key=lambda x: x[2])

    for ssid, avg_rssi, distance in display_list:
        clean_lcd()
        display_text = f"{ssid} ({distance:.1f}m)"
        write_on_lcd(display_text, 0, 0)
        sleep(2)
