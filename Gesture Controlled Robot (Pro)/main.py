from time import ticks_ms, ticks_diff, sleep
from machine import I2C, Pin

from ROBOT_ACTIONS import *

start_time_left = None
start_time_right = None
obstacle_trigger_time = None

flicker_lcd(1, 0.1):
    
write_on_lcd("Initializing Robot", 0, 0):
sleep(2)
lcd.clear()

while True:
    data_stream("USB")
    ir_left = read_left_ir() 
    ir_right = read_right_ir() 
    distance = obstacle_distance()
        
    write_on_lcd("Awaiting Gesture", 0, 0):
    
    robot_stop()

    if distance<15 and obstacle_trigger_time is None:
        obstacle_trigger_time = ticks_ms()

    if obstacle_trigger_time is not None:
        elapsed_time = ticks_diff(ticks_ms(), obstacle_trigger_time)

        if 25 <= distance <= 40 and elapsed_time <= 1000:
            write_on_lcd("Forward Gesture Detected", 0, 0)
            robot_forward(1, 1)
            sleep(2)
            obstacle_trigger_time = None
        elif elapsed_time > 1000:
            obstacle_trigger_time = None

    
    if ir_left == 0 and start_time_left is None:
        start_time_left = ticks_ms() 

    if start_time_left is not None:
        elapsed_time = ticks_diff(ticks_ms(), start_time_left)

        if ir_right == 0 and elapsed_time <= 1000:
            write_on_lcd("Left Gesture Detected", 0, 0)
            robot_axis_left(1, 1)  
            sleep(2)  # Give time for the action
            start_time_left = None  
        elif elapsed_time > 1000:
            start_time_left = None  
    
    ir_left = read_left_ir()   
    ir_right = read_right_ir()  

    if ir_right == 0 and start_time_right is None:
        start_time_right = ticks_ms()  

    if start_time_right is not None:
        elapsed_time = ticks_diff(ticks_ms(), start_time_right)

        if ir_left == 0 and elapsed_time <= 1000:
            write_on_lcd("Right Gesture Detected", 0, 0)
            robot_axis_right(1, 1)  
            sleep(2) 
            start_time_right = None 
        elif elapsed_time > 1000:
            start_time_right = None  

    sleep(0.0001)
