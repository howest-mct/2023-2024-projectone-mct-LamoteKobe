import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

devicePins = [0, 0, 0, 0, 0, 0, 0, 17, 27, 22]

GPIO.setup(devicePins[7], GPIO.OUT)
GPIO.setup(devicePins[8], GPIO.OUT)
GPIO.setup(devicePins[9], GPIO.OUT)

from repositories.MCP import MCP
mcp_obj = MCP(0, 0)


# TODO: GPIO

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
    GPIO.output(devicePins[int(data["id"])], int(data["state"]))
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
