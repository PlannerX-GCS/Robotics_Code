import time
from time import sleep
from machine import Pin, I2C
from vl53l0x import VL53L0X
from ROBOT_ACTIONS import *

i2c = I2C(0, sda=Pin(20), scl=Pin(21))
print("I2C Scan:", i2c.scan())

tof = VL53L0X(i2c)

while True:
    for i in range(0, 180, 1):
        move_servo(0, i)
        distance = tof.read()
        print("Servo0:", i, "  Distance:", distance)
        sleep(0.01)

    for j in range(0, 180, 1):
        move_servo(1, j)
        distance = tof.read()
        print("Servo1:", j, "  Distance:", distance)
        sleep(0.01)

    for k in range(180, 0, -1):
        move_servo(0, k)
        distance = tof.read()
        print("Servo0:", k, "  Distance:", distance)
        sleep(0.01)

    for n in range(180, 0, -1):
        move_servo(1, n)
        distance = tof.read()
        print("Servo1:", n, "  Distance:", distance)
        sleep(0.01)
