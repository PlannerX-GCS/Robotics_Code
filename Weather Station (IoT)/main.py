from ROBOT_ACTIONS import * 
from INTERNAL_SENSOR_STREAM import internal_sensor_datas 
import time

flicker_lcd(0.5, 0.05)
write_on_lcd("Weather Station", 0, 0)
sleep(1)
clean_lcd()

prev_temp = None
prev_pres = None

while True: 
    (_, _, _, _, _, _, error, _, _, tempC, pres_hPa, _, _) = internal_sensor_datas() 

    if error == 0: 
        line1 = "T:{:>2}C P:{:>4}h".format(tempC, pres_hPa)

        # Decide weather comment
        if prev_temp is not None and prev_pres is not None:
            temp_change = tempC - prev_temp
            pres_change = pres_hPa - prev_pres

            if temp_change >= 2:
                line2 = "Hot Weather"
            elif temp_change <= -2:
                line2 = "Cool Breeze"
            elif pres_change <= -5:
                line2 = "Might Rain"
            elif pres_change >= 5:
                line2 = "Dry Weather"
            else:
                line2 = "Usual Weather"
        else:
            line2 = "Usual Weather"

        # Update previous values
        prev_temp = tempC
        prev_pres = pres_hPa

    else: 
        line1 = ""
        line2 = ""

    write_on_lcd(line1, 0, 0) 
    write_on_lcd(line2, 1, 0) 
    sleep(2)  # Slower refresh for stability

