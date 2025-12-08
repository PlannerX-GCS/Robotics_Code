from collections import OrderedDict
import machine
import utime

def robot_node_mapping():

    LEFT_IR = []
    RIGHT_IR = []
    LEFT_MOTORS = []
    RIGHT_MOTORS = []
    LEFT_MOTOR_SPEED = []
    RIGHT_MOTOR_SPEED = []
    ECHO = []
    TRIGGER = []
    SERVO = []
    RGB_RED = []
    RGB_BLUE = []
    RGB_GREEN = []
    RGB_SINGLE = []
    LDR = []
    
    KEYPAD_C1 = []
    KEYPAD_C2 = []
    KEYPAD_C3 = []
    KEYPAD_C4 = []
    
    KEYPAD_R1 = []
    KEYPAD_R2 = []
    KEYPAD_R3 = []
    KEYPAD_R4 = []
    
    
    JOYSTICK_LR = []
    JOYSTICK_UD = []
    JOYSTICK_SW = []
    
    SOIL_SENSOR = []
    
    reference = {"A":7, "B":8, "C":9, "D":10, "E":11, "F":12, "G":13, "H":2, "I":3, "J":4, "K":5, "L":6, "M":22}

    # Open the file and read lines
    with open('Nodes_Configuration.txt', 'r') as file:
        lines = file.readlines()
        
    # Extract values from each line and populate the dictionary
    for line in lines:
        values = line.strip().split(',')
        for value in values:
            if "No Connection" in str(value):
                pass
            elif str(value)[-1:] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
                port_number = reference[str(value)[-1:]]
            
                if "Left IR" in value:
                    LEFT_IR.append(port_number)
                elif "Right IR" in value:
                    RIGHT_IR.append(port_number)
                elif "Left DC Motor A1" in value or "Left DC Motor A2" in value:
                    LEFT_MOTORS.append(port_number)
                elif "Right DC Motor B1" in value or "Right DC Motor B2" in value:
                    RIGHT_MOTORS.append(port_number)
                elif "Left DC Motor Speed" in value:
                    LEFT_MOTOR_SPEED.append(port_number)
                elif "Right DC Motor Speed" in value:
                    RIGHT_MOTOR_SPEED.append(port_number)
                elif "Echo" in value:
                    ECHO.append(port_number)
                elif "Trig" in value:
                    TRIGGER.append(port_number)
                elif "Servo" in value:
                    SERVO.append(port_number)
                elif "RGB Red" in value:
                    RGB_RED.append(port_number)
                elif "RGB Blue" in value:
                    RGB_BLUE.append(port_number)
                elif "RGB Green" in value:
                    RGB_GREEN.append(port_number)
                elif "RGB Single" in value:
                    RGB_SINGLE.append(port_number)
                elif "LDR" in value:
                    LDR.append(port_number)
                    
                elif "Keypad Row 1" in value:
                    KEYPAD_R1.append(port_number)
                elif "Keypad Row 2" in value:
                    KEYPAD_R2.append(port_number)
                elif "Keypad Row 3" in value:
                    KEYPAD_R3.append(port_number)
                elif "Keypad Row 4" in value:
                    KEYPAD_R4.append(port_number)
                    
                elif "Keypad Coloumn 1" in value:
                    KEYPAD_C1.append(port_number)
                elif "Keypad Coloumn 2" in value:
                    KEYPAD_C2.append(port_number)
                elif "Keypad Coloumn 3" in value:
                    KEYPAD_C3.append(port_number)
                elif "Keypad Coloumn 4" in value:
                    KEYPAD_C4.append(port_number)
                    
                elif "Joystick X" in value:
                    JOYSTICK_LR.append(port_number)
                elif "Joystick Y" in value:
                    JOYSTICK_UD.append(port_number)
                elif "Joystick Switch" in value:
                    JOYSTICK_SW.append(port_number)
                    
                elif "Soil Moisture" in value:
                    SOIL_SENSOR.append(port_number)
                                                            
    return LEFT_IR, RIGHT_IR, LEFT_MOTORS, RIGHT_MOTORS, LEFT_MOTOR_SPEED, RIGHT_MOTOR_SPEED, ECHO, TRIGGER, SERVO, RGB_RED, RGB_BLUE, RGB_GREEN, RGB_SINGLE, LDR, KEYPAD_C1, KEYPAD_C2, KEYPAD_C3, KEYPAD_C4, KEYPAD_R1, KEYPAD_R2, KEYPAD_R3, KEYPAD_R4, JOYSTICK_LR, JOYSTICK_UD, JOYSTICK_SW, SOIL_SENSOR

def set_servo_angle(pwm, angle, min_angle=None, max_angle=None):
    # If min_angle or max_angle is None, use default values
    min_angle = min_angle if min_angle is not None else 0
    max_angle = max_angle if max_angle is not None else 180
    
    # Ensure the angle is within the specified limits
    angle = max(min(angle, max_angle), min_angle)
    
    # Map the angle to the pulse duration
    pulse_width = int((angle / 180) * 1000) + 1000
    duty = int(pulse_width * 65535 / 20000)
    pwm.duty_u16(duty)
    
def mode_check(channel, string_condition):
    mode = 0
    operator = string_condition[0]
    if string_condition == "" or string_condition == "NA":
        threshold = 0
    else:   
        threshold = int(string_condition[1:])
    
    if operator == "<":
        if int(channel) < threshold:
            mode = 1
    elif operator == ">":
        if int(channel) > threshold:
            mode = 1
    else:
        mode = 0
    
    return mode
    
def mission_execution(filename):
    seq_number = []
    action = []
    time_deg_rad = []
    dist_time = []
    times = []
    auto = []
    steerable = []
    with_previous = []
    rpm = []
    voltage = []
    diameter = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        values = line.strip().split(',')
        seq_number.append(values[0])
        action.append(values[1])
        time_deg_rad.append(values[2])
        dist_time.append(values[3])
        times.append(values[4])
        auto.append(values[5])
        steerable.append(values[6])
        with_previous.append(values[8])
        rpm.append(values[9])
        voltage.append(values[10])
        diameter.append(values[11])
        mission_repeat.append(values[12])
        
    return seq_number, action, time_deg_rad, dist_time, times, auto, steerable, with_previous, rpm[0], voltage[0], diameter[0], mission_repeat[0]

def mode_checking(switch1, switch2, switch3):
    _, _, mode_triggers = mode_selection()
    if mode_check(switch1, str(mode_triggers[0])) == 1:
        drive_mode = "Default"
        
    elif mode_check(switch2, str(mode_triggers[1])) == 1:
        drive_mode = "Route_Planner"
        
    elif mode_check(switch3, str(mode_triggers[2])) == 1:
        drive_mode = "Remote Control"
        
    else:
        drive_mode = "Default"
        
    return drive_mode


