from time import sleep
from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import *

flicker_lcd(1, 0.1) 

write_on_lcd("Starting...", 0, 0 )
sleep(2)
clean_lcd()


while True:
    data_stream("USB")
    ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()

    write_on_lcd("Tilt X:", 0, 0)
    write_on_lcd("Tilt Y:", 1, 0)

    write_on_lcd(pitch, 0, 8)
    write_on_lcd(roll, 1, 8)

    sleep(0.05)
    clean_lcd()
    
