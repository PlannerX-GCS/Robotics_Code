from ROBOT_ACTIONS import *
import random
from time import sleep

locking_position = [10, 115] #left servo locks at 10 degrees and right at 115 degrees
release_position = [90, 45] #left servo releases at 90 degrees and right at 45 degrees
delay_time = 0.2

while True:
    x, y, z= read_from_joystick()
    
    if int(x) == 0:
        move_servo(0, locking_position[0])
        move_servo(1, locking_position[1])
        
    else:    
        move_servo(0, release_position[0])
        move_servo(1, release_position[1])
        

