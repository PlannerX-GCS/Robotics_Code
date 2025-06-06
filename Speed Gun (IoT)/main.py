#This project was developed by
#Shashi

from ROBOT_ACTIONS import *
from time import *

distance = 8 #Enter the distance between the IR Sensors

while True:
    if read_left_ir() == 0:
        clean_lcd()
        write_on_lcd("LeftIR Triggered", 0, 0)
        start_time = ticks_ms()

        while read_right_ir() != 0:
            sleep(0.001)

        end_time = ticks_ms()
        clean_lcd()
        write_on_lcd("RightIR Triggered", 0, 0)

        dt = ticks_diff(end_time, start_time)
        print(dt)
        if dt > 0:
            speed_mps = distance / dt
            speed_kmph = speed_mps * 3.6
            clean_lcd()
            write_on_lcd(f"Speed: {speed_mps:.2f} m/s", 0, 0)
            write_on_lcd(f"{speed_kmph:.2f} km/h", 1, 0)
            sleep(3)
        else:
            clean_lcd()
            write_on_lcd("Invalid Reading", 0, 0)
            sleep(1)
    
    else:
        clean_lcd()
        write_on_lcd("Waiting for     Vehicles!", 0, 0)

    sleep(0.001)

