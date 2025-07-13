from ROBOT_ACTIONS import *
from GPS_DATA_STREAM import *

def external_sensor_datas():
    try:
        left_ir_value = read_left_ir()
        right_ir_value = read_right_ir()
        
        distance = obstacle_distance()
        
        latitude, longitude, satellites = gps_data()
    
    except Exception as e:
        left_ir_value = int(0)
        right_ir_value = int(0)
        
        distance = int(0)
        
        latitude = int(0)
        longitude = int(0)
        satellites = int(0)
    
    return left_ir_value, right_ir_value, distance, latitude, longitude, satellites
