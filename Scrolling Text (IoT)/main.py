from machine import Pin
from time import sleep
import random
from ROBOT_ACTIONS import *

text = "Hello"
scroll_type = "L"  # This can be L, R, T, B
scroll_speed = 0.3  # This should be between 0.1 and 1

while True:
    if scroll_type == "L":
        for i in range(15, -len(text), -1):  # Scroll from right to left
            clean_lcd()
            write_on_lcd(text, 0, i)
            sleep(scroll_speed)

    elif scroll_type == "R":
        for i in range(-len(text), 16):  # Scroll from left to right
            clean_lcd()
            write_on_lcd(text, 0, i)
            sleep(scroll_speed)

    elif scroll_type == "T":
        for i in range(0, 2):
            clean_lcd()
            write_on_lcd(text, i, 0)
            sleep(scroll_speed)

    elif scroll_type == "B":
        for i in range(1, -1, -1):  # Scroll from bottom to top (line 1 → 0)
            clean_lcd()
            write_on_lcd(text, i, 0)
            sleep(scroll_speed)

