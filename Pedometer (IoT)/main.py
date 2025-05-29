#This project was developed by
#Poojyanth M

from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import internal_sensor_datas
from time import sleep, time
from math import *

STEP_THRESHOLD = 0.1        
STEP_COOLDOWN = 0.5
SPEED_FACTOR = 0.1
step_count = 0
last_step_time = 0
start_time = time()        

write_on_lcd("Fitness Tracker", 0, 0)
write_on_lcd("Steps: 0", 1, 0)
sleep(2)

def pad_right(text, width=16):
    return text + " " * (width - len(text)) if len(text) < width else text[:width]

while True:
    ax, ay, az, gx, gy, gz, error, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()

    current_time = time()
    
    print(ax)
    
    if abs(ax) > STEP_THRESHOLD and (current_time - last_step_time) > STEP_COOLDOWN:
        step_count += 1
        last_step_time = current_time

    total_time = int(current_time - start_time)
    minutes = total_time // 60
    seconds = total_time % 60

    if total_time > 0:
        speed = int((step_count / total_time) * 60)
    else:
        speed = 0
        
    if abs(ax) <= STEP_THRESHOLD:
        speed = 0

    line1 = "Steps:{} Spd:{}".format(step_count, speed*SPEED_FACTOR)
    line2 = "Time {:02d}:{:02d}".format(minutes, seconds)

    write_on_lcd(pad_right(line1), 0, 0)
    write_on_lcd(pad_right(line2), 1, 0)

    sleep(0.0001)