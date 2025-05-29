#This project was developed by
#Poojyanth

from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import internal_sensor_datas
from time import sleep

PITCH_THRESHOLD = 30
ROLL_THRESHOLD = 30
FORWARD_SPEED = 0.6
TURN_SPEED = 0.5
FORWARD_TIME = 2
TURN_TIME = 1

write_on_lcd("Motion Control", 0, 0)
write_on_lcd("Ready...", 1, 0)
sleep(2)

while True:
    ax, ay, az, gx, gy, gz, error, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()

    if error != 0:
        clean_lcd()
        write_on_lcd("Sensor Error!", 0, 0)
        write_on_lcd("Check Sensor", 1, 0)
        sleep(1)
        continue

    if roll > PITCH_THRESHOLD:
        clean_lcd()
        write_on_lcd("Robot Will Move", 0, 0)
        write_on_lcd("Forward after 2s", 1, 0)
        sleep(2)
        robot_forward(FORWARD_SPEED, FORWARD_SPEED)
        sleep(FORWARD_TIME)
        robot_stop()
        
    elif roll < -PITCH_THRESHOLD:
        clean_lcd()
        write_on_lcd("Robot Will Move", 0, 0)
        write_on_lcd("Backward in 2s", 1, 0)
        sleep(2)
        robot_reverse(FORWARD_SPEED, FORWARD_SPEED)
        sleep(FORWARD_TIME)
        robot_stop()

    elif pitch < -ROLL_THRESHOLD:
        clean_lcd()
        write_on_lcd("Turning Left", 0, 0)
        write_on_lcd("after 2 sec", 1, 0)
        sleep(2)
        robot_axis_left(TURN_SPEED, TURN_SPEED)
        sleep(TURN_TIME)
        robot_stop()

    elif pitch > ROLL_THRESHOLD:
        clean_lcd()
        write_on_lcd("Turning Right", 0, 0)
        write_on_lcd("after 2 sec", 1, 0)
        sleep(2)
        robot_axis_right(TURN_SPEED, TURN_SPEED)
        sleep(TURN_TIME)
        robot_stop()

    else:
        clean_lcd()
        write_on_lcd("Motion Control", 0, 0)
        write_on_lcd("Standing By", 1, 0)
        robot_stop()

    sleep(0.001)