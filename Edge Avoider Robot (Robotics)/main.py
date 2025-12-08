from time import sleep
from ROBOT_ACTIONS import *
import random

sleep(1)

actions = [
    lambda: robot_axis_left(0.6, 0.8),
    lambda: robot_axis_right(0.6, 0.8)
]

while True:
    ir_value = read_left_ir()
    if ir_value == 0:
        robot_forward(0.6, 0.8)
    elif ir_value == 1:
        robot_reverse(0.6, 0.8)
        sleep(1.5)
        random.choice(actions)()
        sleep(2)
    else:
        robot_stop()
    sleep(0.1)
    
