import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# TODO: GPIO


# ///// CONFIG \\\\\ #

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)


# ///// MAIN \\\\\ #

pinServo = 21
pinButton = 20

mcp_obj = MCP(0, 0)

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

servo = GPIO.PWM(pinServo, 50)
servo.start(0)

def convert_percentage(data):
    percentage = (data)/float(2046)
    return percentage

def main():
    try:
        while True:
            oost = mcp_obj.read_channel(0)
            west = mcp_obj.read_channel(1)
            mult = 3
            hoek = 2.5 + 10 * (180*convert_percentage(((oost-west)*mult)+1023)) / 180
            servo.ChangeDutyCycle(hoek)
            time.sleep(0.1)
    except Exception as e:
        print(e)
        mcp_obj.closepi()
        GPIO.cleanup()


def start_thread():
    # threading.Timer(10, all_out).start()
    t = threading.Thread(target=all_out, daemon=True)
    t.start()
    print("thread started")


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/api/v1/power/')
def get_power():
    return DataRepository.get_power_usage(), 200


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    status = DataRepository.read_status_lampen()
    emit('B2F_status_lampen', {'lampen': status}, broadcast=False)


@socketio.on('F2B_switch_light')
def switch_light(data):
    print('licht gaat aan/uit', data)
    lamp_id = data['lamp_id']
    new_status = data['new_status']
    # spreek de hardware aan
    # stel de status in op de DB
    res = DataRepository.update_status_lamp(lamp_id, new_status)
    print(res)
    # vraag de (nieuwe) status op van de lamp
    data = DataRepository.read_status_lamp_by_id(lamp_id)
    socketio.emit('B2F_verandering_lamp',  {'lamp': data})
    # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
    if lamp_id == '3':
        print(f"TV kamer moet switchen naar {new_status} !")
        # Do something


if __name__ == '__main__':
    try:
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("finished")
