import time
import RPi.GPIO as GPIO

lasttime = time.monotonic()

def pulse(pin):
    starttime = time.monotonic()
    global lasttime
    while GPIO.input(pin):
        if time.monotonic() - starttime > 0.01:
            # print("pulse")
            tijd = time.monotonic() - lasttime
            wH = 3600 / tijd
            print(f"tijd {tijd}")
            print(f"wH: {wH}wH")
            lasttime = time.monotonic()
            return
    # print("FILTER")

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(13, GPIO.RISING, callback=pulse, bouncetime=80)

GPIO.output(19, 1)

try:
    while True:
        time.sleep(0.1)
except Exception as e:
    print(e)
    GPIO.cleanup()
finally:
    GPIO.cleanup()
    
