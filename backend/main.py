import time
import RPi.GPIO as GPIO
from repositories.MCP import MCP
from repositories.oled import OLED
from subprocess import check_output

pinServo = 21
pinButton = 22

pinLed1 = 14
pinLed2 = 15
pinLed3 = 18

pinRelais = 17

mcp_obj = MCP(0, 0)
oled = OLED()
oled.clear_display()
ips = check_output(['hostname', '--all-ip-addresses']).decode('ascii')
ips = ips.split(' ')
oled.draw_image(f"Solar Monitor \nIP: {ips[0]}")

def button(pin):
    buttonPress = not GPIO.input(pinButton)
    delay = time.time()
    while buttonPress:
        buttonPress = not GPIO.input(pinButton)
        if time.time() > (delay + 2):
            print("uit")
            return
    print("show ip")

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinServo, GPIO.OUT)
GPIO.setup(pinButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pinButton, GPIO.FALLING, callback=button, bouncetime=200)

GPIO.setup(pinLed1, GPIO.OUT)
GPIO.setup(pinLed2, GPIO.OUT)
GPIO.setup(pinLed3, GPIO.OUT)

GPIO.setup(pinRelais, GPIO.OUT)

GPIO.output(pinLed1, 0)
GPIO.output(pinLed2, 1)
GPIO.output(pinLed3, 0)

GPIO.output(pinRelais, 1)

servo = GPIO.PWM(pinServo, 50)
servo.start(0)

def convert_volts(data, places):
    volts = (data*3.3)/float(1023)
    volts = round(volts,places)
    return volts

def convert_percentage(data):
    percentage = (data)/float(2046)
    return percentage


last_hoek = 0

try:
    while True:
        oost = mcp_obj.read_channel(0)
        west = mcp_obj.read_channel(1)
        hoek = (west - oost) * 3
        servoControl = 2.5 + 10 * (180*convert_percentage((hoek)+1023)) / 180
        if not (last_hoek - 150 < hoek < last_hoek + 150):
            servo.start(0)
            servo.ChangeDutyCycle(servoControl)
            time.sleep(0.1)
            servo.stop()
            last_hoek = hoek
        time.sleep(2)
except Exception as e:
    print(e)
    mcp_obj.closepi()
    GPIO.cleanup()
finally:
    GPIO.cleanup()
    
