from ROBOT_ACTIONS import *
from time import sleep

locking_position = [0, 0]
release_position = [180, 180]

current_position = [90, 110]
selected_servo = 0
switch_prev_state = 1  # To detect toggle edge

# Initialize both servos
move_servo(0, current_position[0])
move_servo(1, current_position[1])

def move_one_step_towards(servo_id, target_angle):
    global current_position
    current_angle = current_position[servo_id]

    if current_angle == target_angle:
        return

    step = 1 if target_angle > current_angle else -1
    new_angle = current_angle + step
    move_servo(servo_id, new_angle)
    current_position[servo_id] = new_angle
    
clean_lcd()
write_on_lcd("Robot Arm Ready", 0, 0)
write_on_lcd("Lower Arm Engage", 1, 0)

while True:
    x, y, sw = read_from_joystick()

    if sw == 0 and switch_prev_state == 1:
        selected_servo = 1 - selected_servo
        if selected_servo == 0:
            clean_lcd()
            write_on_lcd("Toggled to LowerArm", 0, 0)
        elif selected_servo == 1:
            clean_lcd()
            write_on_lcd("Toggled to UpperArm", 0, 0)
        sleep(0.2)

    switch_prev_state = sw

    if x == 0:
        move_one_step_towards(selected_servo, locking_position[selected_servo])
    elif y == 0:
        move_one_step_towards(selected_servo, release_position[selected_servo])

    sleep(0.01)

