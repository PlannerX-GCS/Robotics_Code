from ROBOT_ACTIONS import *
from machine import Pin, PWM
from time import *

base_speed = float(0.8) #Keep it 0.8 or higher (max is 1.0, min is 0.0)
turn_speed = float(0.5) #Keep it greater than 0.35 and lesser than base speed (max is 1.0, min is 0.35)
follow_black_line = True #Make True if robot needs to follow black line, to follow white line keep False
action_at_off_line = "Stop" #This can be "Take U-Turn", "Take Left", "Take Right" or "Stop", depending on what you want the robot to do when both sensors are off the line


def off_line_action():
    if action_at_off_line == "Take U-Turn":
        robot_axis_right(base_speed, base_speed)
        time.sleep(0)
        
    elif action_at_off_line == "Take Left":
        robot_axis_left(base_speed, base_speed)
        time.sleep(0.0)
        
    elif action_at_off_line == "Take Right":
        robot_axis_right(base_speed, base_speed)
        time.sleep(0.0)
        
    elif action_at_off_line == "Stop":
        robot_stop()

    else:
        pass

while True:
    data_stream("USB")
    
    left_value = int(read_left_ir())
    right_value = int(read_right_ir())
        
    if follow_black_line == True:
        if left_value and not right_value:
            robot_forward(base_speed, turn_speed)
        elif right_value and not left_value:
            robot_forward(turn_speed, base_speed)
        elif left_value and right_value:
            off_line_action()
            integral = 0
        else:
            robot_forward(base_speed, base_speed)
    
    if follow_black_line == False:
        if not left_value and right_value:
            robot_forward(base_speed, turn_speed)
        elif not right_value and left_value:
            robot_forward(turn_speed, base_speed)
        elif not left_value and not right_value:
            off_line_action()
            integral = 0
        else:
            robot_forward(base_speed, base_speed)
    
    time.sleep(0.00000001)


