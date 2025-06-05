from ROBOT_ACTIONS import *
from time import sleep, ticks_ms, ticks_diff

# === Servo Pin Assignments ===
rear_left_upper = 3
rear_left_lower = 7

forward_left_upper = 1
forward_left_lower = 5

forward_right_upper = 2
forward_right_lower = 6

rear_right_upper = 0
rear_right_lower = 4

head = 8  # Unused in pose transitions

# === Servo Pins Order ===
servo_pins = [
    rear_left_upper, rear_left_lower,
    forward_left_upper, forward_left_lower,
    forward_right_upper, forward_right_lower,
    rear_right_upper, rear_right_lower
]

# === Pose Definitions ===
pose_standing = [110, 90, 90, 75, 130, 140, 75, 75]
pose_sitting  = [145, 125, 45, 45, 175, 180, 45, 45]
pose_prawl    = [165, 125, 110, 75, 115, 145, 25, 45]

initial_head = 98

LR_diagonal_walk = [90, 70, 90, 75, 130, 140, 75, 75]
RF_diagonal_walk = [110, 90, 70, 55, 130, 140, 75, 75]
LF_diagonal_walk = [110, 90, 90, 75, 150, 160, 75, 75]
RR_diagonal_walk = [110, 90, 90, 75, 130, 140, 95, 95]

LR_reverse_walk = [100, 80, 90, 75, 130, 140, 75, 75]
RF_reverse_walk = [110, 90, 80, 65, 130, 140, 75, 75]
LF_reverse_walk = [110, 90, 90, 75, 140, 150, 75, 75]
RR_reverse_walk = [110, 90, 90, 75, 130, 140, 85, 85]

LR_left_walk = [90, 70, 90, 75, 130, 140, 75, 75]
RF_left_walk = [110, 90, 80, 65, 130, 140, 75, 75]
LF_left_walk = [110, 90, 90, 75, 150, 160, 75, 75]
RR_left_walk = [110, 90, 90, 75, 130, 140, 85, 85]

LR_right_walk = [120, 100, 90, 75, 130, 140, 75, 75]
RF_right_walk = [110, 90, 110, 95, 130, 140, 75, 75]
LF_right_walk = [110, 90, 90, 75, 120, 130, 75, 75]
RR_right_walk = [110, 90, 90, 75, 130, 140, 55, 55]

ginger_lean_down = [110, 90, 70, 55, 150, 160, 75, 75]
ginger_lean_up = [110, 90, 110, 95, 110, 120, 75, 75]

# === Smooth Movement Functions ===
def smooth_transition(servo_pins, start_angles, end_angles, steps=30, delay=0.02):
    for step in range(steps + 1):
        for pin, start, end in zip(servo_pins, start_angles, end_angles):
            angle = int(start + (end - start) * step / steps)
            move_servo(pin, angle)
        sleep(delay)

# === Generic Transition Between Poses ===
def ginger_transition(from_pose, to_pose, steps=30, delay=0.02):
    smooth_transition(servo_pins, from_pose, to_pose, steps, delay)

# === Initialize to Stand Pose Smoothly ===
def initial_ginger_stand():
    for pin, angle in zip(servo_pins, pose_standing):
        move_servo(pin, angle)
        sleep(0.01)
        
    move_servo(head, initial_head)
        
def ginger_head(angle):
    move_servo(head, angle)
    
def ginger_no():
    for i in range(98, 135):
        move_servo(head, i)
        sleep(0.01)

    for i in range(135, 65, -1):
        move_servo(head, i)
        sleep(0.01)
        
    for i in range(65, 98, 1):
        move_servo(head, i)
        sleep(0.01)
        
def ginger_yes():
    ginger_transition(pose_standing, ginger_lean_down, steps=30)
    current_pose = ginger_lean_down
    
    sleep(0.5)
    
    ginger_transition(ginger_lean_down, pose_standing, steps=30)
    current_pose = pose_standing
    
    sleep(0.5)
    
    ginger_transition(pose_standing, ginger_lean_down, steps=30)
    current_pose = ginger_lean_down
    
    sleep(0.5)
    
    ginger_transition(ginger_lean_down, pose_standing, steps=30)
    current_pose = pose_standing
    
    sleep(0.5)
    
def ginger_walk(direction):
    if direction == "F":
        ginger_transition(pose_standing, RF_diagonal_walk, steps=10)
        current_pose = RF_diagonal_walk
        
        ginger_transition(RF_diagonal_walk, RR_diagonal_walk, steps=10)
        current_pose = RR_diagonal_walk
        
        ginger_transition(RR_diagonal_walk, LF_diagonal_walk, steps=10)
        current_pose = LF_diagonal_walk
        
        ginger_transition(LF_diagonal_walk, LR_diagonal_walk, steps=10)
        current_pose = LR_diagonal_walk
        
    if direction == "B":
        ginger_transition(pose_standing, LR_reverse_walk, steps=10)
        current_pose = LR_reverse_walk
        
        ginger_transition(LR_reverse_walk, RF_reverse_walk, steps=10)
        current_pose = RF_reverse_walk
        
        ginger_transition(RF_reverse_walk, LF_reverse_walk, steps=10)
        current_pose = LF_reverse_walk
        
        ginger_transition(LF_reverse_walk, RR_reverse_walk, steps=10)
        current_pose = RR_reverse_walk
    
def ginger_turn(turn_side):
    if turn_side == "L":
        ginger_transition(pose_standing, LR_left_walk, steps=10)
        current_pose = LR_left_walk
        
        ginger_transition(LR_left_walk, RF_left_walk, steps=10)
        current_pose = RF_left_walk
        
        ginger_transition(RF_left_walk, LF_left_walk, steps=10)
        current_pose = LF_left_walk
        
        ginger_transition(LF_left_walk, RR_left_walk, steps=10)
        current_pose = RR_left_walk
        
    elif turn_side == "R":
        ginger_transition(pose_standing, LR_right_walk, steps=10)
        current_pose = LR_right_walk
        
        ginger_transition(LR_right_walk, RF_right_walk, steps=10)
        current_pose = RF_right_walk
        
        ginger_transition(RF_right_walk, LF_right_walk, steps=10)
        current_pose = LF_right_walk
        
        ginger_transition(LF_right_walk, RR_right_walk, steps=10)
        current_pose = RR_right_walk

initial_ginger_stand()
current_pose = pose_standing

walk_time= 8000
turn_time = 4000

while True:
    # Walk forward
    start_time = ticks_ms()
    
    while ticks_diff(ticks_ms(), start_time) < walk_time:
        ginger_walk("F")
    current_pose = LR_diagonal_walk
    sleep(2)
    
    # Walk Backward
    start_time = ticks_ms()
    
    while ticks_diff(ticks_ms(), start_time) < walk_time:
        ginger_walk("B")
    current_pose = RR_reverse_walk
    sleep(2)
    
    #Stand
    ginger_transition(RR_reverse_walk, pose_standing)
    current_pose = pose_standing
    sleep(2)
    
    #Prawl
    ginger_transition(pose_standing, pose_prawl)
    current_pose = pose_prawl
    sleep(2)
    
    #Nod
    ginger_no()
    sleep(1)
    
    #Sit
    ginger_transition(pose_prawl, pose_sitting)
    current_pose = pose_sitting
    sleep(15)
    
    #Nod
    ginger_no()
    sleep(2)
    
    #Stand
    ginger_transition(pose_sitting, pose_standing)
    current_pose = pose_standing
    sleep(2)
    
    #Turn left
    start_time = ticks_ms()
    
    while ticks_diff(ticks_ms(), start_time) < turn_time:
        ginger_turn("L")
    current_pose = RR_left_walk
    sleep(2)
    
    #Turn right
    start_time = ticks_ms()
    
    while ticks_diff(ticks_ms(), start_time) < turn_time:
        ginger_turn("R")
    current_pose = RR_right_walk
    sleep(2)
    
    #Stand
    ginger_transition(RR_right_walk, pose_standing)
    current_pose = pose_standing
    sleep(2)
