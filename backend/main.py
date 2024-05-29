import time
import RPi.GPIO as GPIO
from repositories.MCP import MCP

pinServo = 21

mcp_obj = MCP(0, 0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinServo, GPIO.OUT)

servo = GPIO.PWM(pinServo, 50)
servo.start(0)

def convert_volts(data, places):
    volts = (data*3.3)/float(1023)
    volts = round(volts,places)
    return volts

def convert_percentage(data):
    percentage = (data)/float(2046)
    print(round(percentage*100, 2))
    return percentage

try:
    while True:
        oost = mcp_obj.read_channel(0)
        west = mcp_obj.read_channel(1)
        hoek = 2.5 + 10 * (180*convert_percentage((oost-west)+1023)) / 180
        servo.ChangeDutyCycle(hoek)
        time.sleep(0.1)
except Exception as e:
    print(e)
    mcp_obj.closepi()
    GPIO.cleanup()
    
