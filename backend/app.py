import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from repositories.MCP import MCP
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


####### Callback functions

def pulse(pin):
    starttime = time.monotonic()
    global lasttime
    while GPIO.input(pin):
        if time.monotonic() - starttime > 0.01:
            # print("pulse")
            # DataRepository.
            tijd = time.monotonic() - lasttime
            wH = 3600 / tijd
            print(f"tijd {tijd}")
            print(f"wH: {wH}wH")
            lasttime = time.monotonic()
            return
    # print("FILTER")


def button(pin):
    pass

#######

####### Pins define
pinServo = 21
pinButton = 22

pinLed1 = 14
pinLed2 = 15
pinLed3 = 18

pinRelais = 17

# Pins setup
GPIO.setup(pinServo, GPIO.OUT)
servo = GPIO.PWM(pinServo, 50)

GPIO.setup(pinButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pinButton, GPIO.FALLING, callback=button, bouncetime=200)

GPIO.setup(pinLed1, GPIO.OUT)
GPIO.setup(pinLed2, GPIO.OUT)
GPIO.setup(pinLed3, GPIO.OUT)

GPIO.setup(pinRelais, GPIO.OUT)




mcp_obj = MCP(0, 0)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)


def main():
    sun_last_state = ""
    while True:
        oost = mcp_obj.read_channel(0)
        west = mcp_obj.read_channel(1)
        DataRepository.write_ldr(oost, west)
        if -50 < (west-oost) < 50:
            sun_state = "zuid"
        elif west > oost:
            sun_state = "oost"
        else:
            sun_state = "west"

        if sun_last_state != sun_state:
            socketio.emit("B2F_sunpos", {"pos": sun_state})
            sun_last_state = sun_state

        print(sun_last_state)
        
        time.sleep(1)




def start_thread():
    # threading.Timer(10, all_out).start()
    t = threading.Thread(target=main, daemon=True)
    t.start()
    print("thread started")


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_deviceState')
def test(data):
    # GPIO.output(devicePins[int(data["id"])], int(data["state"]))
    socketio.emit('B2F_deviceUpdate', { "id": data["id"], "state": int(not int(data["state"]))})
    DataRepository.write_device_state(data["id"], data["state"])
    

if __name__ == '__main__':
    try:
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("finished")
