from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
import config
import main_threads
import random
import time
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = random.randbytes(32)
socketio = SocketIO(app)

@app.route("/")
def main():
    return redirect("/live-state")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/live-state")
def livestate():
    return render_template("live-state.html")

@app.route("/set_config", methods = ["POST"])
def set_config():
    name = request.args.get('name')
    value = request.args.get('value')
    print("Setting", name, "to", value)
    config.config[name] = value
    config.save()
    return "success"

@socketio.on('connect')
def connect_event():
    print('Client connected')


def send_sensor_data():
    while True:
        time.sleep(1)  # Wait for 10 seconds
        # socketio.emit('sensors', {
        #     "temperature": 21.0,
        #     "humidity": 32,
        #     "flammable_gas": False,
        #     "earthquake": False,
        #     "smoke": False,
        #     "time": time.strftime("%H:%M", time.gmtime())
        # })
        data = main_threads.get_latest_sensor_data_entry()
        if (len(data) > 0):
            socketio.emit('sensors', {
                "humidity": data["humidity"],
                "temperature": data["temperature"],
                "earthquake": data["earthquake"],
                "flame": data["flame"],
                "smoke": data["smoke"],
                "gas": data["gas"],
                "time": data["time"]
            })

if __name__ == "__main__":
    main_threads.main()
    socketio.start_background_task(target=send_sensor_data)
    socketio.run(app)
