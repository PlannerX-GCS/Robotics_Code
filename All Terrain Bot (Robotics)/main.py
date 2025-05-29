#This project was developed by
#Rakshita

from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import internal_sensor_datas
from time import sleep  

NORMAL_SPEED = 0.6
CLIMB_SPEED = 0.95
SLOW_SPEED = 0.4
INCLINE_UP = 15    
INCLINE_DOWN = -15 

write_on_lcd("All Terrain Mode", 0, 0)
write_on_lcd("Starting...", 1, 0)
sleep(2)

while True:
    ax, ay, az, gx, gy, gz, error, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()

    if error == 0:
        if pitch < -INCLINE_UP:
            clean_lcd()
            run_left_motors_only(SLOW_SPEED, 0.0)
            write_on_lcd("Adjust Left", 0, 0)

        elif pitch > INCLINE_UP:
            clean_lcd()
            run_right_motors_only(0.0, SLOW_SPEED)
            write_on_lcd("Adjust Right", 0, 0)
            
        elif pitch > INCLINE_UP or roll > INCLINE_UP:
            clean_lcd()
            robot_forward(SLOW_SPEED, SLOW_SPEED)
            write_on_lcd("Slowing Down!", 0, 0)

        elif pitch < INCLINE_DOWN or roll < INCLINE_DOWN:
            clean_lcd()
            robot_forward(CLIMB_SPEED, CLIMB_SPEED)
            write_on_lcd("Climbing Up!", 0, 0)

        else:
            clean_lcd()
            robot_forward(NORMAL_SPEED, NORMAL_SPEED)
            write_on_lcd("Moving Forward", 0, 0)

    else:
        write_on_lcd("Sensor Error!", 0, 0)

    sleep(0.001)