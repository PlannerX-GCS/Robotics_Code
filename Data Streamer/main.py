from time import sleep
from ROBOT_ACTIONS import *

flicker_lcd(1, 0.1) 

write_on_lcd("Initialising", 0, 0 )
sleep(2)
lcd.clear()

prev_distance = 0

while True:
    data_stream("USB")
    sleep(0.0002)
    
