from time import sleep
from ROBOT_ACTIONS import *

while True:
    try:
        data_stream("Wifi")
        sleep(0.2)
    except Exception as e:
        print(e)
        pass
    
