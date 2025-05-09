from time import sleep
from ROBOT_ACTIONS import *

flicker_lcd(1, 0.1) 

write_on_lcd("Initialising", 0, 0 )
sleep(2)
lcd.clear()

prev_distance = 0

while True:
    data_stream("USB")
    distance = obstacle_distance()
    if distance == -1:
        write_on_lcd(prev_distance, 0, 0 )
    else:
        prev_distance = distance
        write_on_lcd(distance, 0, 0 )
    sleep(0.002)
    lcd.clear()
    
