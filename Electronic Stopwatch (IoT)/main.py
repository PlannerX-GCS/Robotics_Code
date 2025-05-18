from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import internal_sensor_datas
from time import *

flicker_lcd(1, 0.05)

START_ROLL = 25      
STOP_ROLL = -25     
RESET_PITCH = 25   

hours = 0
minutes = 0
seconds = 0

stopwatch_running = False

write_on_lcd("Stopwatch", 0, 0)
write_on_lcd("00:00:00", 1, 0)

while True:
    ax, ay, az, gx, gy, gz, error, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()

    if error == 0:
        if roll > START_ROLL:
            stopwatch_running = True

        elif roll < STOP_ROLL:
            stopwatch_running = False

        if pitch > RESET_PITCH:
            hours = 0
            minutes = 0
            seconds = 0
            clean_lcd()
            stopwatch_running = False
            write_on_lcd("Reset Done!", 0, 0)
            sleep(1.5)
            clean_lcd()

        if stopwatch_running:
            seconds += 1
            if seconds == 60:
                seconds = 0
                minutes += 1
            if minutes == 60:
                minutes = 0
                hours += 1

        stopwatch_text = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
        
        write_on_lcd("Stopwatch", 0, 0)
        write_on_lcd(stopwatch_text, 1, 0)

    else:
        clean_lcd()
        write_on_lcd("Sensor error!", 0, 0)

    sleep(1)