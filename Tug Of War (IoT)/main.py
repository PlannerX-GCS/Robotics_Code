from machine import Pin
from time import sleep
import random
from ROBOT_ACTIONS import *

while True:  # Outer loop to restart game indefinitely
    character = 7
    
    clean_lcd()
    write_on_lcd(" <Game Starts> ", 0, 0)
    sleep(2)
    clean_lcd()

    prev_left_ir = 1
    prev_right_ir = 1

    while True:  # Inner game loop
        write_on_lcd("[", 0, 0)
        write_on_lcd("[", 1, 0)
        write_on_lcd("]", 0, 15)
        write_on_lcd("]", 1, 15)

        write_on_lcd("#", 0, character)
        write_on_lcd("#", 1, character)    
        write_on_lcd("#", 0, character+1)
        write_on_lcd("#", 1, character+1)

        current_left_ir = read_left_ir()
        current_right_ir = read_right_ir()

        if prev_left_ir == 1 and current_left_ir == 0:
            clean_lcd()
            character -= 1

        if prev_right_ir == 1 and current_right_ir == 0:
            clean_lcd()
            character += 1

        prev_left_ir = current_left_ir
        prev_right_ir = current_right_ir

        if character >= 15:
            clean_lcd()
            write_on_lcd("Left Player Won", 0, 0)
            break  # Break inner loop to restart game

        if character <= 0:
            clean_lcd()
            write_on_lcd("Right Player Won", 0, 0)
            break  # Break inner loop to restart game

        sleep(0.00001)

    sleep(2)  # Pause before restarting the game

