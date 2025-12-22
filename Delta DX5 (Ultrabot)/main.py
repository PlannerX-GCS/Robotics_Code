from machine import Pin
import utime
from time import sleep
from math import exp
from ROBOT_ACTIONS import *

# ----------------------------------------------------------
# USER SETTINGS
# ----------------------------------------------------------
STEP = 5       # XY movement step for main servos (0-2)
Z_STEP = 5     # Z axis step
STEP_XY = 5    # Pan-tilt step for Servos 4 & 5

# ----------------------------------------------------------
# IR PIN
# ----------------------------------------------------------
ir_pin = Pin(10, Pin.IN)

# ----------------------------------------------------------
# IR BUTTON HEX CODES
# ----------------------------------------------------------
BTN_HOME       = "0xffa25d"  # 1
BTN_UP         = "0xff18e7"
BTN_DOWN       = "0xff4ab5"
BTN_LEFT       = "0xff10ef"
BTN_RIGHT      = "0xff5aa5"
BTN_Z_PLUS     = "0xff6897"   # *
BTN_Z_MINUS    = "0xffb04f"   # #
BTN_EFF_X_PLUS  = "0xff629d"  # 6
BTN_EFF_X_MINUS = "0xffa857"  # 4
BTN_EFF_Y_PLUS  = "0xff22dd"  # 2
BTN_EFF_Y_MINUS = "0xffc23d"  # 8
BTN_RECORD      = "0xff38c7"  # 0 / Record / OK
BTN_DELETE      = "0xff9867"  # Delete
BTN_RESET       = "0xffe21d"  # Reset
BTN_REPLAY      = "0xff02fd"  # Replay path

RECORD_FILE = "delta_x_path_record.txt"

# ----------------------------------------------------------
# SERVO LIMITS
# ----------------------------------------------------------
s0_min, s0_max = 75, 135
s1_min, s1_max = 71, 125
s2_min, s2_max = 70, 126
s4_min, s4_max = 0, 180
s5_min, s5_max = 0, 180

# Current positions
s0 = 85
s1 = 85
s2 = 85
s4 = 70
s5 = 100

# ----------------------------------------------------------
# EASING FUNCTION
# ----------------------------------------------------------
def ease_out_exp(t):
    return 1 - exp(-5 * t)

# ----------------------------------------------------------
# SMOOTH MOVE (main servos 0-2)
# ----------------------------------------------------------
def smooth_move(target0, target1, target2, duration=0.3, steps=60):
    global s0, s1, s2

    target0 = max(s0_min, min(s0_max, target0))
    target1 = max(s1_min, min(s1_max, target1))
    target2 = max(s2_min, min(s2_max, target2))

    start0, start1, start2 = s0, s1, s2

    for i in range(steps + 1):
        t = i / steps
        e = ease_out_exp(t)
        p0 = int(start0 + (target0 - start0) * e)
        p1 = int(start1 + (target1 - start1) * e)
        p2 = int(start2 + (target2 - start2) * e)
        move_servo(0, p0)
        move_servo(1, p1)
        move_servo(2, p2)
        sleep(duration / steps)

    s0, s1, s2 = target0, target1, target2

# ----------------------------------------------------------
# DECODE IR (NEC Protocol)
# ----------------------------------------------------------
def decode_ir():
    while ir_pin.value() == 1:
        pass

    start = utime.ticks_us()
    while ir_pin.value() == 0:
        pass
    low = utime.ticks_diff(utime.ticks_us(), start)
    if low < 8000 or low > 10000:
        return None

    start = utime.ticks_us()
    while ir_pin.value() == 1:
        pass
    high = utime.ticks_diff(utime.ticks_us(), start)
    if high < 4000 or high > 5000:
        return None

    data = 0
    for _ in range(32):
        while ir_pin.value() == 0:
            pass
        start = utime.ticks_us()
        while ir_pin.value() == 1:
            pass
        high = utime.ticks_diff(utime.ticks_us(), start)
        if high > 1000:
            data = (data << 1) | 1
        else:
            data = (data << 1) | 0
    return data

# ----------------------------------------------------------
# HOME FUNCTION
# ----------------------------------------------------------
def home():
    global s0, s1, s2
    clean_lcd()
    write_on_lcd("Operation", 0, 0)
    write_on_lcd(">> HOMING", 1, 0)
    smooth_move(75, 71, 70, 1.2)
    sleep(0.3)
    move_servo(4, 70)
    move_servo(5, 100)
    s0 = 75
    s1 = 71
    s2 = 70
    s3 = 70
    s4m = 100
    clean_lcd()
    write_on_lcd("Operation", 0, 0)
    write_on_lcd(">> HOMING DONE", 1, 0)
    sleep(1.5)

# ----------------------------------------------------------
# XY MOVEMENT (main servos)
# ----------------------------------------------------------
def move_xy(dx, dy):
    global s0, s1, s2
    if dx != 0 and dy == 0:
        new0 = s0 + dx
        new1 = s1
        new2 = s2 - dx
    elif dy != 0 and dx == 0:
        new0 = s0
        new1 = s1 + dy
        new2 = s2 - dy
    else:
        return
    smooth_move(new0, new1, new2, 0.25)

# ----------------------------------------------------------
# Z MOVEMENT
# ----------------------------------------------------------
def move_z(step):
    global s0, s1, s2
    new0 = s0 + step
    new1 = s1 + step
    new2 = s2 + step
    smooth_move(new0, new1, new2, 0.25)

# ----------------------------------------------------------
# PAN-TILT (Servos 4 & 5)
# ----------------------------------------------------------
def move_effector(dx, dy):
    global s4, s5
    s4 = max(s4_min, min(s4_max, s4 + dx))
    s5 = max(s5_min, min(s5_max, s5 + dy))
    move_servo(4, s4)
    move_servo(5, s5)

# ----------------------------------------------------------
# RECORD / DELETE / RESET / REPLAY
# ----------------------------------------------------------
def record_current():
    with open(RECORD_FILE, "a") as f:
        f.write(f"{s0},{s1},{s2},{s4},{s5}\n")
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> RECORDED", 1, 0)

def delete_last():
    try:
        with open(RECORD_FILE, "r") as f:
            lines = f.readlines()
        if lines:
            lines.pop()
        with open(RECORD_FILE, "w") as f:
            f.writelines(lines)
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> LAST POS DELETE", 1, 0)
    except OSError:
        print("File not found")

def reset_record():
    with open(RECORD_FILE, "w") as f:
        pass
    clean_lcd()
    write_on_lcd("Operation", 0, 0)
    write_on_lcd(">> RECORD RESET", 1, 0)

def replay_path():
    try:
        with open(RECORD_FILE, "r") as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) != 5:
                continue
            clean_lcd()
            write_on_lcd("Operation", 0, 0)
            write_on_lcd(">> POS FOLLOW", 1, 0)
            t0, t1, t2, t4, t5 = map(int, parts)
            move_servo(4, t4)
            move_servo(5, t5)
            smooth_move(t0, t1, t2, 1.5, 60)
            sleep(0.5)
    except OSError:
        print("No recorded path to replay")

# ----------------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------------
flicker_lcd(1, 0.2)
write_on_lcd("Delta-X", 0, 0)
write_on_lcd("by Safear India", 1, 0)
sleep(2)

while True:
    clean_lcd()
    write_on_lcd("Delta-X", 0, 0)
    write_on_lcd(">> IS READY", 1, 0)
    result = decode_ir()
    if result is None:
        continue

    code = hex(result)
    #print("CODE:", code)

    # Home
    if code == BTN_HOME:
        home()

    # Main XY movement
    elif code == BTN_UP:
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> UP", 1, 0)
        move_xy(0, +STEP)
    elif code == BTN_DOWN:
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> DOWN", 1, 0)
        move_xy(0, -STEP)
    elif code == BTN_LEFT:
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> LEFT", 1, 0)
        move_xy(-STEP, 0)
    elif code == BTN_RIGHT:
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> RIGHT", 1, 0)
        move_xy(+STEP, 0)

    # Z axis
    elif code == BTN_Z_PLUS:
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> Z-AXIS +ve", 1, 0)
        move_z(+Z_STEP)
    elif code == BTN_Z_MINUS:
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> Z-AXIS -ve", 1, 0)
        move_z(-Z_STEP)

    # Pan-Tilt
    elif code == BTN_EFF_X_PLUS:
        move_effector(+STEP_XY, 0)
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> EFFECTOR X+", 1, 0)
    elif code == BTN_EFF_X_MINUS:
        move_effector(-STEP_XY, 0)
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> EFFECTOR X-", 1, 0)
    elif code == BTN_EFF_Y_PLUS:
        move_effector(0, +STEP_XY)
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> EFFECTOR Y+", 1, 0)
    elif code == BTN_EFF_Y_MINUS:
        move_effector(0, -STEP_XY)
        clean_lcd()
        write_on_lcd("Operation", 0, 0)
        write_on_lcd(">> EFFECTOR Y-", 1, 0)

    # Record / Delete / Reset / Replay
    elif code == BTN_RECORD:
        record_current()
    elif code == BTN_DELETE:
        delete_last()
    elif code == BTN_RESET:
        reset_record()
    elif code == BTN_REPLAY:
        replay_path()

    utime.sleep_ms(150)

