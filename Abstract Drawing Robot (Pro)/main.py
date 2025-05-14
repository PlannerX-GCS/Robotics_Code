from ROBOT_ACTIONS import *
import random
from time import sleep

drawing_speed = 0.40
minimum_drawing_time = 0.2
maximum_drawing_time = 1

possible_actions = [
    lambda: robot_forward(drawing_speed,drawing_speed),
    lambda: robot_reverse(drawing_speed,drawing_speed),
    lambda: robot_axis_left(drawing_speed,drawing_speed),
    lambda: robot_axis_right(drawing_speed,drawing_speed)
]

sleep(1)

while True:
    data_stream("USB")
    action = random.choice(possible_actions)
    action()

    time.sleep(random.uniform(minimum_drawing_time,maximum_drawing_time))
