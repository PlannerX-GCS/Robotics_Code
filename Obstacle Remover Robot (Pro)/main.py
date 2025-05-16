from ROBOT_ACTIONS import *
import random
from time import sleep

robot_speed = 0.55
grab_distance = 6
turn_time = 1

locking_position = [10, 115] #left servo locks at 10 degrees and right at 115 degrees
release_position = [90, 45] #left servo releases at 90 degrees and right at 45 degrees

#Stablise the reading, as multiple devices make distance sensor unstable
def stable_distance(samples=5):
    readings = [obstacle_distance() for _ in range(samples)]
    valid = [d for d in readings if d != -1]
    if not valid:
        return -1
    return sum(valid) / len(valid)

while True:
    #read distance
    
    distance = stable_distance()
    
    #if no object is detected
    if distance > 9:
        robot_forward(robot_speed, robot_speed)

    #if false reading is recieved
    elif distance == -1:
        robot_stop()
        
    #if object is detected
    elif distance !=-1 and distance <=9:
        
        #stop the robot
        robot_stop()
        sleep(1)
        
        #grab the object
        move_servo(0, locking_position[0])
        move_servo(1, locking_position[1])
        sleep(2)
        
        #keep the robot to the left
        robot_axis_left(robot_speed, robot_speed)
        sleep(turn_time)
        
        #stop the robot for a while
        robot_stop()
        sleep(1)
        
        #release the object
        move_servo(0, release_position[0])
        move_servo(1, release_position[1])
        sleep(1)
        
        #reverse the robot to avoid hitting the released object
        robot_reverse(robot_speed, robot_speed)
        sleep(turn_time/2)

        #turn right to go to initial position
        robot_axis_right(robot_speed, robot_speed)
        sleep(turn_time)
        
        #stop the robot
        robot_stop()
        sleep(1)



