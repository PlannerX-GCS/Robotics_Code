from time import sleep
from ROBOT_ACTIONS import obstacle_distance

flicker_lcd(1, 0.1) #Initialises your LCD Screen with an flickering animation (First value (1) is total flicker time, and Second Value (0.1) is time interval at which flickering happens)

write_on_lcd("Initialising", 0, 0 )
sleep(2)
lcd.clear()

prev_distance = 0

while True:
    data_stream("USB")
    distance = obstacle_distance()
    if distance == -1:
        te_on_lcd(prev_distance, 0, 0 )
    else:
        prev_distance = distance
        te_on_lcd(distance, 0, 0 )
    sleep(0.2)
    lcd.clear()
    
