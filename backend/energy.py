import time
import RPi.GPIO as GPIO



def pulse(pin):
    start = time.monotonic()
    while GPIO.input(pin):
        if time.monotonic() - start > 0.01:
            print("pulse")
            return
    print("FILTER")

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.RISING, callback=pulse, bouncetime=80)

GPIO.output(5, 1)

try:
    while True:
        time.sleep(0.1)
except Exception as e:
    print(e)
    GPIO.cleanup()
finally:
    GPIO.cleanup()
    
