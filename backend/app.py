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
            DataRepository.write_pulse(pin)
            print("pulse")
            # print(pin)
            # DataRepository.write_pulse()
            # tijd = time.monotonic() - lasttime
            # wH = 3600 / tijd
            # print(f"tijd {tijd}")
            # print(f"wH: {wH}wH")
            # lasttime = time.monotonic()
            return
    print("FILTER")

    
def button(pin):
    pass

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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)


def convert_percentage(data):
    if -2046 >= data:
        return 0
    elif data >= 2046:
        return 1
    percentage = (data)/float(2046)
    return percentage


def main():
    # init appliances to match database values
    for i in DataRepository.get_appliances()["data"]:
        GPIO.output(ledIds[i["id"]], i["value"])

    last_hoek = -5000
    try:
        while True:
            oost = mcp_obj.read_channel(0)
            west = mcp_obj.read_channel(1)
            hoek = (west - oost) * 3
            servoControl = 2.5 + 10 * (180*convert_percentage((hoek)+1023)) / 180
            if not (last_hoek - 400 < hoek < last_hoek + 400):
                servo.start(0)
                servo.ChangeDutyCycle(servoControl)
                time.sleep(0.5)
                servo.stop()
                last_hoek = hoek
            time.sleep(2)
    except Exception as e:
        mcp_obj.closepi()
        GPIO.cleanup()
    finally:
        GPIO.output(pinRelais, 0)
        time.sleep(1)
        GPIO.cleanup()





def start_thread():
    # threading.Timer(10, all_out).start()
    t = threading.Thread(target=main, daemon=True)
    t.start()
    print("thread started")


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


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')


@socketio.on('F2B_appliance')
def appliance_update(obj):
    DataRepository.write_appliance(obj["appliance"], not int(obj["state"]))
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
