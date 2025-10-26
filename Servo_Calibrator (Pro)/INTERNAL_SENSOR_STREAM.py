from machine import I2C
from imu import MPU6050
from bmp085 import BMP180
import utime
import math
import machine
import time

# Initialize I2C
i2c = I2C(1, sda=26, scl=27)  # Update pins if necessary

error_code = 0
pitch = 0
roll = 0
tempC = 0
pres_hPa = 0
altitude = 0
battery_voltage = 0

ax = 0
ay = 0
az = 0
gx = 0
gy = 0
gz = 0

# Initialize sensors
mpu_sensor = MPU6050(i2c)
bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 101325

pitch_offset = 0
roll_offset = 0
pitch_correction_factor = 1
roll_correction_factor = 1

def calculate_pitch_roll(ax, ay, az, pitch_offset, roll_offset, pitch_correction_factor, roll_correction_factor):
    """ Calculate pitch and roll from accelerometer data. """
    pitch = math.atan2(ay, math.sqrt(ax**2 + az**2)) * (180 / math.pi)
    roll = math.atan2(ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
    pitch = (pitch+pitch_offset)*pitch_correction_factor
    roll = (roll+roll_offset)*roll_correction_factor
    return pitch, roll

# Initialize ADC for the VBAT pin (pin 36)
vbat_adc = machine.ADC(26)  # Pin 26 is used to read the battery voltage

# Reference voltage (for the Pico, it's typically 3.3V)
reference_voltage = 3.3

def read_battery_voltage():
    # Read ADC value (0-65535)
    adc_value = vbat_adc.read_u16()
    
    # Convert ADC value to voltage (0 to 3.3V range)
    voltage = (adc_value / 65535) * reference_voltage
    
    # Since we are reading the battery voltage, scale it
    # Battery voltage is proportional to (3.3 / ADC value)
    battery_voltage = voltage * (3.3 / voltage)  # For an accurate value, apply calibration if needed.
    
    return battery_voltage


def internal_sensor_datas():
    global error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage
    global ax, ay, az, gx, gy, gz
    try:
        ax=round(mpu_sensor.accel.x,2)
        ay=round(mpu_sensor.accel.y,2)
        az=round(mpu_sensor.accel.z,2)
        gx=round(mpu_sensor.gyro.x)
        gy=round(mpu_sensor.gyro.y)
        gz=round(mpu_sensor.gyro.z)# Read gyroscope values
        # Calculate pitch and roll
        pitch, roll = calculate_pitch_roll(ax, ay, az, pitch_offset, roll_offset, pitch_correction_factor, roll_correction_factor)
        
        error_code = int(0)
        tempC = int(bmp.temperature)   #get the temperature in degree celsius
        pres_hPa = int(bmp.pressure)    #get the pressure in hpa
        altitude = int(bmp.altitude)   #get the altitude
        battery_voltage = float(read_battery_voltage())
        

        utime.sleep(0.0001)  # Delay for 1 second before the next read
    
    except Exception as e:
        error_code = int(1)
        pitch = int(0)
        roll = int(0)
        tempC = int(0)
        pres_hPa = int(0)
        ax = int(0)
        ay = int(0)
        az = int(0)
        gx = int(0)
        gy = int(0)
        gz = int(0)

    return ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage
