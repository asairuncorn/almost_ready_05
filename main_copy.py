from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import RPi.GPIO as GPIO
from switch import Switch
from led import LED
from pump import Pump
from timer import Timer
from sensor import PressureSensor
import threading
import os
from PiControler import*
import eventlet
from data_file_render import *

# Set GPIO pins for switch, LED, and pump relay
SWITCH_PIN = 17  # GPIO pin for the start switch
LED_PIN = 27     # GPIO pin for the LED
RELAY_PIN = 22   # GPIO pin for the pump relay




app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Use environment variable or default key
socketio = SocketIO(app, cors_allowed_origins="*")

progress_state = {
    1: {'status': 'Idle', 'progress': 0, 'pressure': 0},
    2: {'status': 'Idle', 'progress': 0, 'pressure': 0},
    3: {'status': 'Idle', 'progress': 0, 'pressure': 0},
    4: {'status': 'Idle', 'progress': 0, 'pressure': 0},
}





GPIO.setmode(GPIO.BCM)  # Set GPIO mode
eventlet.monkey_patch()
def monitor_switch():
    while True:
        if switch.is_pressed():
            progress_state[1]['status'] = 'Ready'

            socketio.emit('switch_status', {'status': 'Ready'})

            if  progress_state[1]['status'] == 'Finished':

                    socketio.emit('switch_status', {'status': 'Finished'})

        else:
            socketio.emit('switch_status', {'status': 'install cartridge'})


        socketio.sleep(1)  # Poll the switch status every second

def update_progress_dial( progres):
    emit('update_state', {'bay_id': 1, 'status': 'Running', 'progress': progres}, broadcast=True)

    if progres == 100:
        progress_state[1]['status'] = 'Finished'
        time.sleep(2)
        emit('update_state', {'bay_id': 1, 'status': 'Finished', 'progress': 0}, broadcast=True)
        print(progress_state)





switch = Switch(SWITCH_PIN)
led = LED(LED_PIN)


@app.route('/')
def index():
    return render_template('index_n.html')



# Store the state for each bay


# Send initial state to new client
@socketio.on('connect')
def handle_connect():
    emit('initialize_state', progress_state)





# Handle button press events
@socketio.on('start_progress')
def handle_start_progress(data):
    bay_id = data['bay_id']
    progress_state[bay_id]['status'] = 'Running'
    progress_state[bay_id]['progress'] = 0

    emit('update_state', {'bay_id': bay_id, 'status': 'Running', 'progress': 0}, broadcast=True)
    print(bay_id, progress_state[bay_id]['progress'])

    print(progress_state)


    pump = Pump(RELAY_PIN)
    pressure_sensor = PressureSensor()
    timer = Timer(5, pressure_sensor)
    timer.start(update_progress_dial)
    # timer.start(update_progress_dial, bay_id, progres)
    # progres = timer.send_time()
    # emit('update_state', {'bay_id': bay_id, 'status': 'Running', 'progress': progres}, broadcast=True)
    # #
    # # pump_controller = PiPumpController(switch, led, pump, timer)
    # # pump_controller.check_and_run()

@socketio.on('stop_progress')
def handle_stop_progress(data):
    bay_id = data['bay_id']
    progress_state[bay_id]['status'] = 'Stopped'
    emit('update_state', {'bay_id': bay_id, 'status': 'Stopped', 'progress': progress_state[bay_id]['progress']}, broadcast=True)

@socketio.on('update_pressure')
def handle_update_pressure(data):
    bay_id = data['bay_id']
    pressure = data['pressure']
    progress_state[bay_id]['pressure'] = pressure
    emit('update_pressure', {'bay_id': bay_id, 'pressure': pressure}, broadcast=True)

# Handle setting time or any other configuration
@socketio.on('set_time')
def handle_set_time(data):
    bay_id = data['bay_id']
    time = data['time']
    # Update time for the bay
    # If needed, store time to progress_state and notify other clients
    emit('update_time', {'bay_id': bay_id, 'time': time}, broadcast=True)





# Run the server using socketio.run for WebSocket support
if __name__ == '__main__':
    print("Starting Flask-SocketIO server...")
    socketio.run(app, host='127.0.0.1', port=5001, debug=True, allow_unsafe_werkzeug=True)
    thread = threading.Thread(target=monitor_switch, daemon=True)
    thread.start()




