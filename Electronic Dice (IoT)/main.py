from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import *
import time
import random

flicker_lcd(1, 0.05)

def detect_shake():
    roll_list = []
    start_time = time.time()
    while time.time() - start_time < 0.5:
        data = internal_sensor_datas()
        if data[6] == 0:
            roll = data[8]
            roll_list.append(roll)
        time.sleep(0.05)
    if len(roll_list) >= 2 and (max(roll_list) - min(roll_list)) > 60:
        return True
    return False

def roll_dice():
    clean_lcd()
    number = random.randint(1, 6)
    write_on_lcd("Rolled: " + str(number), 0, 0)
    if number == 6:
        write_on_lcd("Take more chance", 1, 0)
        time.sleep(1.5)
    time.sleep(2)

def main():
    write_on_lcd("Shake to Roll", 0, 0)
    while True:
        if detect_shake():
            roll_dice()
            write_on_lcd("Shake to Roll", 0, 0)

main()