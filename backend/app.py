import threading
import time
from PIL import Image, ImageDraw
from subprocess import check_output
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from repositories.MCP import MCP
from repositories.oled import OLED
import random
import RPi.GPIO as GPIO
import os
from repositories.RTC import RTC
GPIO.setmode(GPIO.BCM)


####### Callback functions
lasttime = {
    "solar": time.monotonic(),
    "house": time.monotonic(),
    "eco": time.monotonic()
}
lastpower = {
    "solar": 0,
    "house": 0,
    "eco": 0
}
# measure pulse and write to db
# filters out false pulses by waiting
def pulse(pin):
    starttime = time.monotonic()
    global lasttime
    global lastpower
    if pin == 1:
        name = DataRepository.write_pulse(pin)
        power = 3600 / (time.monotonic() - lasttime[name])
        socketio.emit("B2F_update_power", {"name": name, "power": power})
        lastpower[name] = power
        lasttime[name] = time.monotonic()
    else:
        while GPIO.input(pin):
            if time.monotonic() - starttime > 0.01:
                name = DataRepository.write_pulse(pin)
                power = 3600 / (time.monotonic() - lasttime[name])
                socketio.emit("B2F_update_power", {"name": name, "power": power})
                lastpower[name] = power
                lasttime[name] = time.monotonic()
                return

    
def button(pin):
    global oled
    buttonPress = not GPIO.input(pinButton)
    delay = time.time()
    while buttonPress:
        buttonPress = not GPIO.input(pinButton)
        if time.time() > (delay + 2):
            oled.display("Shutting down...")
            os.system("sudo poweroff")
            return
    oled.display_network()
    time.sleep(5)
    oled.clear_display()

#######

####### Pins define
pinServo = 21
pinButton = 22

pinLed1 = 14
pinLed2 = 15
pinLed3 = 18

ledIds = {
    7: pinLed1,
    8: pinLed2,
    9: pinLed3
}

ledCount = 0
threshold = 1000

pinRelais = 17

# Pins setup
GPIO.setup(pinServo, GPIO.OUT)
servo = GPIO.PWM(pinServo, 50)

GPIO.setup(pinButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pinButton, GPIO.FALLING, callback=button, bouncetime=200)

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(5, GPIO.RISING, callback=pulse, bouncetime=80)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(6, GPIO.RISING, callback=pulse, bouncetime=80)

GPIO.setup(pinLed1, GPIO.OUT)
GPIO.setup(pinLed2, GPIO.OUT)
GPIO.setup(pinLed3, GPIO.OUT)

GPIO.setup(pinRelais, GPIO.OUT)

GPIO.output(pinRelais, 1)
GPIO.output(pinLed1, 0)
GPIO.output(pinLed3, 0)
GPIO.output(pinLed2, 0)




mcp_obj = MCP(0, 0)
oled = OLED()

# set time if no internet connection
rtc = RTC()
rtc.update()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)

# convert percentage for servo control
def convert_percentage(data):
    if 0 >= data:
        return 0
    elif data >= 2046:
        return 1
    percentage = (data)/float(2046)
    return percentage


def main():
    global ledCount

    # init appliances to match database values
    try:
        for i in DataRepository.get_appliances()["data"]:
            global ledCount
            ledCount += i["value"]
            GPIO.output(ledIds[i["id"]], i["value"])
    except Exception as ex:
        pass

    # rotate servo
    last_hoek = -5000
    try:
        while True:
            oost = mcp_obj.read_channel(0)
            west = mcp_obj.read_channel(1)
            hoek = (west - oost) * 3
            servoControl = 2.5 + 10 * (180*convert_percentage((hoek)+1023)) / 180
            if not (last_hoek - 3000 < hoek < last_hoek + 3000):
                servo.start(0)
                servo.ChangeDutyCycle(servoControl)
                time.sleep(0.5)
                servo.stop()
                last_hoek = hoek
            time.sleep(2)

            # simulate energymeter pulses based on how many appliances
            if not random.randint(0, round(10 / (ledCount + 1))) and ledCount:
                pulse(1)

            # drop live wattage when pulses are further apart
            # prevents values to stay high when power consumption is 0
            for i in lastpower:
                if i == "grid":
                    break
                if 3600 / (time.monotonic() - lasttime[i]) <= lastpower[i]:
                    power = 3600 / (time.monotonic() - lasttime[i])
                    if power < 100:
                        power = 0
                    socketio.emit("B2F_update_power", {"name": i, "power": power})
                    lastpower[i] = power

                if i == "solar" and lastpower[i] > threshold + lastpower["house"]:
                    GPIO.output(pinRelais, 1)
                elif i== "solar":
                    GPIO.output(pinRelais, 0)
            # calculate grid usage and send
            try:
                lastpower["grid"] = lastpower["house"] - (lastpower["solar"]-lastpower["eco"])
                socketio.emit("B2F_update_power", {"name": "grid", "power": lastpower["grid"]})
            except Exception as ex:
                pass

    

    except Exception as e:
        mcp_obj.closepi()
    finally:
        GPIO.output(pinRelais, 0)
        time.sleep(1)
        GPIO.cleanup()





def start_thread():
    t = threading.Thread(target=main, daemon=True)
    t.start()


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running", 200

@app.route('/api/v1/power/<scale>/')
def power(scale):
    result = jsonify(DataRepository.get_power_usage(int(scale)))
    if result:
        return result, 200
    else:
        return jsonify("bad request"), 400
    
@app.route('/api/v1/appliances/')
def appliance():
    return DataRepository.get_appliances()

    
@app.route('/api/v1/threshold/')
def get_threshold():
    return {"threshold": threshold}, 200


# SOCKET IO
@socketio.on('F2B_get_power')
def initial_connection():
    for i in lastpower:
        socketio.emit("B2F_update_power", {"name": i, "power": lastpower[i]})
        
@socketio.on('F2B_update_threshold')
def update_threshold(obj):
    global threshold
    try:
        threshold = int(obj["threshold"])
    except ValueError as ex:
        pass


@socketio.on('F2B_appliance')
def appliance_update(obj):
    global ledCount
    if DataRepository.write_appliance(obj["appliance"], not int(obj["state"])):
        if int(obj["state"]):
            ledCount -=  1
        else:
            ledCount += 1
        GPIO.output(ledIds[int(obj["appliance"])], not int(obj["state"]))
        socketio.emit('B2F_appliance', {"id": obj["appliance"], "state": not int(obj["state"])})
    

if __name__ == '__main__':
    try:
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
