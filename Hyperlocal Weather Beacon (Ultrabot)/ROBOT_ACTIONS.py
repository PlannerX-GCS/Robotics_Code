from ROBOT_CONFIGURATIONS import *
from machine import Pin,PWM, time_pulse_us, I2C
import time
from pico_i2c_lcd import I2cLcd
from lcd_api import *
from INTERNAL_SENSOR_STREAM import *
from time import sleep
from EXTERNAL_SENSOR_STREAM import *
from ESP import *

LEFT_IR, RIGHT_IR, LEFT_MOTORS, RIGHT_MOTORS, LEFT_MOTOR_SPEED, RIGHT_MOTOR_SPEED, ECHO, TRIGGER, SERVO, RGB_RED, RGB_BLUE, RGB_GREEN, RGB_SINGLE, LDR, KEYPAD_R1, KEYPAD_R2, KEYPAD_R3, KEYPAD_R4, KEYPAD_C1, KEYPAD_C2, KEYPAD_C3, KEYPAD_C4, JOYSTICK_LR, JOYSTICK_UD, JOYSTICK_SW, SOIL_SENSOR = robot_node_mapping()

LEFT_IR_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in LEFT_IR if pin]
RIGHT_IR_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in RIGHT_IR if pin]

LEFT_MOTORS_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in LEFT_MOTORS if pin]
RIGHT_MOTORS_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RIGHT_MOTORS if pin]

LEFT_MOTOR_SPEED_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in LEFT_MOTOR_SPEED if pin]
RIGHT_MOTOR_SPEED_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RIGHT_MOTOR_SPEED if pin]

ECHO_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in ECHO if pin]
TRIGGER_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in TRIGGER if pin]

SERVO_PINS = [PWM(Pin(int(pin))) for pin in SERVO if pin]

RGB_RED_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RGB_RED if pin]
RGB_BLUE_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RGB_BLUE if pin]
RGB_GREEN_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RGB_GREEN if pin]
RGB_SINGLE_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RGB_SINGLE if pin]

LDR_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in LDR if pin]

KEYPAD_R1_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in KEYPAD_R1 if pin]
KEYPAD_R2_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in KEYPAD_R2 if pin]
KEYPAD_R3_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in KEYPAD_R3 if pin]
KEYPAD_R4_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in KEYPAD_R4 if pin]

KEYPAD_C1_PINS = [machine.Pin(int(pin), machine.Pin.IN, machine.Pin.PULL_DOWN) for pin in KEYPAD_C1 if pin]
KEYPAD_C2_PINS = [machine.Pin(int(pin), machine.Pin.IN, machine.Pin.PULL_DOWN) for pin in KEYPAD_C2 if pin]
KEYPAD_C3_PINS = [machine.Pin(int(pin), machine.Pin.IN, machine.Pin.PULL_DOWN) for pin in KEYPAD_C3 if pin]
KEYPAD_C4_PINS = [machine.Pin(int(pin), machine.Pin.IN, machine.Pin.PULL_DOWN) for pin in KEYPAD_C4 if pin]

JOYSTICK_LR_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in JOYSTICK_LR if pin]
JOYSTICK_UD_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in JOYSTICK_UD if pin]
JOYSTICK_SW_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in JOYSTICK_SW if pin]

SOIL_SENSOR_PINS = [machine.Pin(int(pin), machine.Pin.IN) for SOIL_SENSOR in LDR if pin]

SPEED_PIN_LEFT = PWM(LEFT_MOTOR_SPEED_PINS[0]) if LEFT_MOTOR_SPEED_PINS else None
SPEED_PIN_RIGHT = PWM(RIGHT_MOTOR_SPEED_PINS[0]) if RIGHT_MOTOR_SPEED_PINS else None

try:
    i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
    lcd = I2cLcd(i2c, 39, 2, 16)
except:
    pass

row_pins = KEYPAD_R1_PINS + KEYPAD_R2_PINS + KEYPAD_R3_PINS + KEYPAD_R4_PINS
col_pins = KEYPAD_C1_PINS + KEYPAD_C2_PINS + KEYPAD_C3_PINS + KEYPAD_C4_PINS

# Define key mapping (row major)
KEYPAD_MAP = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

if SPEED_PIN_LEFT:
    SPEED_PIN_LEFT.freq(1000)

if SPEED_PIN_RIGHT:
    SPEED_PIN_RIGHT.freq(1000)

def robot_forward(left_speed, right_speed):
    LEFT_MOTORS_PINS[0].high()
    LEFT_MOTORS_PINS[1].low()
    
    RIGHT_MOTORS_PINS[0].high()
    RIGHT_MOTORS_PINS[1].low()

    if SPEED_PIN_LEFT:
        SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

    if SPEED_PIN_RIGHT:
        SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))


def robot_reverse(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].low()
        LEFT_MOTORS_PINS[1].high()
        
        RIGHT_MOTORS_PINS[0].low()
        RIGHT_MOTORS_PINS[1].high()
        
        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
    
    except:
        pass


def robot_stop():
    try:
        LEFT_MOTORS_PINS[0].low()
        LEFT_MOTORS_PINS[1].low()
        
        RIGHT_MOTORS_PINS[0].low()
        RIGHT_MOTORS_PINS[1].low()
        
    except:
        pass
        
def robot_axis_right(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].high()
        LEFT_MOTORS_PINS[1].low()
        
        RIGHT_MOTORS_PINS[0].low()
        RIGHT_MOTORS_PINS[1].high()
        
        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
            
    except:
        pass

    
def robot_axis_left(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].low()
        LEFT_MOTORS_PINS[1].high()
        
        RIGHT_MOTORS_PINS[0].high()
        RIGHT_MOTORS_PINS[1].low()

        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
            
    except:
        pass
    
def run_left_motors_only(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].high()
        LEFT_MOTORS_PINS[1].low()
        
        RIGHT_MOTORS_PINS[0].low()
        RIGHT_MOTORS_PINS[1].low()
        
        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
            
    except:
        pass

    
def run_right_motors_only(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].low()
        LEFT_MOTORS_PINS[1].low()
        
        RIGHT_MOTORS_PINS[0].high()
        RIGHT_MOTORS_PINS[1].low()

        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
            
    except:
        pass

def move_servo(servo_number, angle):
    try:
        SERVO_PINS[servo_number].freq(50)
        pulse_width = 500 + (angle / 180) * (2500 - 500)
        duty = int(pulse_width * 65535 / 20000)  # Convert microseconds to duty cycle (20ms period)
        
        SERVO_PINS[servo_number].duty_u16(duty)
    except:
        pass
            
def read_left_ir():
    try:
        left_ir_value = LEFT_IR_PINS[0].value()
        return left_ir_value
    
    except:
        return 0

def read_right_ir():
    try:
        right_ir_value = RIGHT_IR_PINS[0].value()
        return right_ir_value
    
    except:
        return 0
    
def read_ldr():
    try:
        ldr_value = LDR_PINS[0].value()
        return ldr_value
    
    except:
        return 0

def obstacle_distance():
    try:
        TRIGGER_PINS[0].low()
        time.sleep_us(2)
        TRIGGER_PINS[0].high()
        time.sleep_us(10)
        TRIGGER_PINS[0].low()

        pulse_duration = time_pulse_us(ECHO_PINS[0], 1, 30000)  # Wait for echo to go high (max 30ms)
        if pulse_duration < 0:
            return -1

        distance = (pulse_duration * 34300) / 2 / 1000000  # Convert microseconds to seconds, then to cm
        return distance
    
    except:
        return -1
    
def flicker_lcd(startup_time, time_interval):
    while startup_time >= 0:
        lcd.backlight_off()
        sleep(time_interval)
        lcd.backlight_on()
        sleep(time_interval)
        startup_time -= time_interval
        
def write_on_lcd(text, line_number, character_number):
    lcd.move_to(character_number, line_number)
    lcd.putstr(str(text))

def clean_lcd():
    lcd.clear()  

def data_stream(type):
    if type == "USB":
        ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()
        left_ir_value, right_ir_value, distance, latitude, longitude, satellites = external_sensor_datas()
        mac_suffix = get_mac_address()
        
        data = [ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude,left_ir_value, right_ir_value, distance, latitude, longitude, satellites, battery_voltage, mac_suffix]
        #print(data)
        return data
        
    elif type == "Wifi":
        send_data()
        
def read_from_keypad():
    try:
        for c_idx, c_pin in enumerate(row_pins):
            c_pin.init(machine.Pin.OUT)
            c_pin.value(1)
            time.sleep_us(10)

            for r_idx, r_pin in enumerate(col_pins):
                if r_pin.value():
                    time.sleep_ms(10)
                    if r_pin.value():
                        c_pin.init(machine.Pin.IN)
                        return KEYPAD_MAP[r_idx][c_idx]

            c_pin.init(machine.Pin.IN)
        return None
    
    except:
        return None


def read_from_joystick():
    try:
        x_axis = JOYSTICK_LR_PINS[0].value()
        y_axis = JOYSTICK_UD_PINS[0].value()
        switch = JOYSTICK_SW_PINS[0].value()
        return x_axis, y_axis, switch
    
    except:
        return 0
    
def read_soil_moisture():
    try:
        soil_moisture_data = SOIL_SENSOR_PINS[0].value()
        return soil_moisture_data
    
    except:
        return 0
        

    

