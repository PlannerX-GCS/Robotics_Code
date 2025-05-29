#This project was developed by
#Rakshita

from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import internal_sensor_datas
from time import sleep  

SHAKE_X_THRESHOLD = 0.5     
SHAKE_Y_THRESHOLD = 0.5   

SAFE_DISTANCE = 10

mode = "none"  

write_on_lcd("Multi-Bot Ready", 0, 0)
write_on_lcd("Shake to Choose", 1, 0)
sleep(2)

while True:
    ax, ay, az, gx, gy, gz, error, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()
    
    print(ax)
    
    if ax > SHAKE_X_THRESHOLD:
        mode = "line"
        clean_lcd()
        write_on_lcd("Converted to", 0, 0)
        write_on_lcd("Line Follower", 1, 0)
        sleep(2)

    elif ay > SHAKE_Y_THRESHOLD:
        mode = "obstacle"
        clean_lcd()
        write_on_lcd("Converted to", 0, 0)
        write_on_lcd("Obstacle Avoider", 1, 0)
        sleep(2)

    if mode == "line":        
        left_ir = read_left_ir()
        right_ir = read_right_ir()
        
        clean_lcd()
        write_on_lcd("IR-1:", 0, 0)
        write_on_lcd(left_ir, 0, 6)
        write_on_lcd("IR-2:", 1, 0)
        write_on_lcd(right_ir, 1, 6)

        if left_ir == 0 and right_ir == 0:
            robot_forward(0.5, 0.5)  
        elif left_ir == 0 and right_ir == 1:
            run_left_motors_only(0.5, 0.0) 
        elif left_ir == 1 and right_ir == 0:
            run_right_motors_only(0.0, 0.5) 
        else:
            robot_stop() 

    elif mode == "obstacle":
        distance = obstacle_distance()
        
        clean_lcd()
        write_on_lcd("IR-1:", 0, 0)
        write_on_lcd(distance, 1, 0)

        if distance != -1:
            if distance < SAFE_DISTANCE:
                robot_stop()
                write_on_lcd("Obstacle Ahead!", 0, 0)
            else:
                robot_forward(0.6, 0.6)
        else:
            write_on_lcd("Ultrasonic Fail", 0, 0)

    sleep(0.0001)