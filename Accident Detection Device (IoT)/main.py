#This project was developed by
#Manyashree

from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import internal_sensor_datas
from time import *

ROLL_THRESHOLD = 20.0     # degrees
PITCH_THRESHOLD = 20.0    # degrees
CHECK_INTERVAL = 0.2      # seconds
DAMAGE_SCALER = 2.5       # damage % per degree beyond threshold
ACCIDENT_HOLD_TIME = 5    # seconds before reset display

clean_lcd()
write_on_lcd("Detecting", 0, 0)

def calculate_damage(pitch, roll):
    pitch_damage = max(0, abs(pitch) - PITCH_THRESHOLD) * DAMAGE_SCALER
    roll_damage = max(0, abs(roll) - ROLL_THRESHOLD) * DAMAGE_SCALER
    total_damage = min(100, round(pitch_damage + roll_damage))
    return total_damage

def detect_accident():
    prev_pitch, prev_roll = 0, 0
    while True:
        sensor_data = internal_sensor_datas()
        error_code = sensor_data[6]

        if error_code == 0:
            pitch = sensor_data[7]
            roll = sensor_data[8]

            delta_pitch = abs(pitch - prev_pitch)
            delta_roll = abs(roll - prev_roll)

            if delta_pitch > PITCH_THRESHOLD or delta_roll > ROLL_THRESHOLD:
                xlean_lcd()
                damage = calculate_damage(pitch, roll)
                display_accident_alert(damage)
                log_impact(pitch, roll, damage)
                sleep(ACCIDENT_HOLD_TIME)

            else:
                clean_lcd()
                write_on_lcd("Detecting", 0, 0)
                prev_pitch, prev_roll = pitch, roll

        sleep(CHECK_INTERVAL)

def display_accident_alert(damage):
    write_on_lcd("Accident Occurred", 0, 0)
    write_on_lcd(f"Damage: {damage}%", 1, 0)

def log_impact(pitch, roll, damage):
    t = localtime()
    timestamp = "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])
    
    print("[{}] Accident Detected".format(timestamp))
    print("Pitch: {:.2f}, Roll: {:.2f}, Damage: {}%".format(pitch, roll, damage))

detect_accident()
