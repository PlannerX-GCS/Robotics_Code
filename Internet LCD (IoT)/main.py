from machine import UART, Pin
from time import sleep
from ROBOT_ACTIONS import *
import ure

esp = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

def send(cmd, wait=2):
    esp.write((cmd + "\r\n").encode())
    sleep(wait)
    while esp.any():
        print(esp.read().decode("utf-8"))

html_page = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n\r\n"
    "<html><body>"
    "<h2>Pico LCD Messenger</h2>"
    "<form method='GET'>"
    "<input name='msg' placeholder='Enter message'/>"
    "<input type='submit' value='Send'/>"
    "</form>"
    "</body></html>"
)

send("AT+RST", 2)
send("ATE0", 1)
send("AT+CWMODE=2", 1)
send('AT+CWSAP="Safear Robotics","12345678",5,3', 3)
send("AT+CIPMUX=1", 1)
send("AT+CIPSERVER=1,80", 1)

def extract_msg(data):
    match = ure.search(r"GET /\?msg=([^ ]+)", data)
    if match:
        return match.group(1).replace("%20", " ")[:32]  # limit to 32 chars
    return None

def send_http_response(conn_id):
    esp.write(f"AT+CIPSEND={conn_id},{len(html_page)}\r\n".encode())

    # Wait for ">" prompt
    t = 1000
    while t > 0:
        if esp.any():
            if b">" in esp.read():
                break
        sleep(0.01)
        t -= 1

    if t > 0:
        esp.write(html_page.encode())
        sleep(0.5)
        esp.write(f"AT+CIPCLOSE={conn_id}\r\n".encode())
    else:
        print("[ERROR] > prompt not received")

buffer = ""

write_on_lcd("Initializing", 0, 0)
sleep(1)
write_on_lcd(">>192.168.4.1", 0, 0)

while True:
    if esp.any():
        try:
            buffer += esp.read().decode("utf-8")
            if "\n" in buffer:
                lines = buffer.split("\n")
                for line in lines:
                    if "+IPD" in line:
                        conn_id = line.split(",")[1].strip()
                        msg = extract_msg(line)
                        if msg:
                            clean_lcd()
                            write_on_lcd(">>192.168.4.1", 0, 0)
                            write_on_lcd(msg[:16], 1, 0)
                        send_http_response(conn_id)
                buffer = ""
        except Exception as e:
            print("[ERROR]", e)
            buffer = ""
    sleep(0.1)

