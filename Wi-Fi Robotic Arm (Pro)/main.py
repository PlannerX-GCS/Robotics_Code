from machine import UART, Pin
from time import sleep
from ROBOT_ACTIONS import *
import ure

esp = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# === Servo state ===
locking_position = [0, 0]
release_position = [180, 180]
current_position = [90, 110]
move_servo(0, current_position[0])
move_servo(1, current_position[1])

def move_one_step(servo_id, up=True):
    target = release_position[servo_id] if up else locking_position[servo_id]
    if current_position[servo_id] == target:
        return
    step = 10 if target > current_position[servo_id] else -10
    new_angle = current_position[servo_id] + step
    move_servo(servo_id, new_angle)
    current_position[servo_id] = new_angle

# === HTML Page ===
html_page = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n\r\n"
    "<html><body>"
    "<h2>Servo Arm Control</h2>"
    "<form method='GET'>"
    "<button name='cmd' value='UP0'>Lower Arm Up</button>"
    "<button name='cmd' value='DOWN0'>Lower Arm Down</button><br><br>"
    "<button name='cmd' value='UP1'>Upper Arm Up</button>"
    "<button name='cmd' value='DOWN1'>Upper Arm Down</button>"
    "</form></body></html>"
)

# === ESP AT HELPERS ===
def send(cmd, wait=2):
    esp.write((cmd + "\r\n").encode())
    sleep(wait)
    while esp.any():
        esp.read()

def extract_cmd(data):
    match = ure.search(r"GET /([A-Z0-9]+)", data)
    if match:
        return match.group(1)
    return None

def send_http_response(conn_id):
    esp.write(f"AT+CIPSEND={conn_id},{len(html_page)}\r\n".encode())
    t = 1000
    while t > 0:
        if esp.any() and b">" in esp.read():
            break
        sleep(0.01)
        t -= 1
    if t > 0:
        esp.write(html_page.encode())
        sleep(0.3)
        esp.write(f"AT+CIPCLOSE={conn_id}\r\n".encode())

# === ESP SERVER SETUP ===
send("AT+RST", 2)
send("ATE0", 1)
send("AT+CWMODE=2", 1)
send('AT+CWSAP="ServoBot","12345678",5,3', 3)
send("AT+CIPMUX=1", 1)
send("AT+CIPSERVER=1,80", 1)

print("📡 Ready! Connect to 'ServoBot' and go to http://192.168.4.1")

# === Main Loop ===
buffer = ""
while True:
    if esp.any():
        try:
            buffer += esp.read().decode("utf-8")
            if "\n" in buffer:
                lines = buffer.split("\n")
                for line in lines:
                    if "+IPD" in line:
                        print("[INFO] Got request:", line)
                        conn_id = line.split(",")[1].strip()
                        cmd = extract_cmd(line)
                        if cmd:
                            print("🔧 Command:", cmd)
                            if cmd in ["UP0", "DOWN0", "UP1", "DOWN1"]:
                                sid = int(cmd[-1])
                                move_one_step(sid, up=("UP" in cmd))
                        send_http_response(conn_id)
                buffer = ""
        except Exception as e:
            print("[ERROR]", e)
            buffer = ""
    sleep(0.1)
