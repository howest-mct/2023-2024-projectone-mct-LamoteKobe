import time
import RPi.GPIO as GPIO
from repositories.MCP import MCP

pinServo = 12
# pinButton = 20

mcp_obj = MCP(0, 0)

# def button(pin):
#     buttonPress = not GPIO.input(pinButton)
#     delay = time.time()
#     while buttonPress:
#         buttonPress = not GPIO.input(pinButton)
#         if time.time() > (delay + 2):
#             print("uit")
#             return
#     print("show ip")

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinServo, GPIO.OUT)
# GPIO.setup(pinButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.add_event_detect(pinButton, GPIO.FALLING, callback=button, bouncetime=200)

servo = GPIO.PWM(pinServo, 50)
servo.start(0)

def convert_volts(data, places):
    volts = (data*3.3)/float(1023)
    volts = round(volts,places)
    return volts

def convert_percentage(data):
    percentage = (data)/float(2046)
    return percentage

try:
    while True:
        oost = mcp_obj.read_channel(0)
        west = mcp_obj.read_channel(1)
        hoek = 2.5 + 10 * (180*convert_percentage(((west-oost)*3)+1023)) / 180
        # hoek = 2.5 + 10 * (180*convert_percentage((0.5)+1023)) / 180
        servo.ChangeDutyCycle(hoek)
        time.sleep(0.1)
except Exception as e:
    print(e)
    mcp_obj.closepi()
    GPIO.cleanup()
finally:
    GPIO.cleanup()
    
