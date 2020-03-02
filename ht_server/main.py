import socket
import pyqrcode
# from random import randint

from time import sleep
from flask import Flask, render_template, request

from event import Event

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))  # this sees if device is connected to internet
ip = s.getsockname()[0]
s.close()

# port_num = randint(49152, 65535)  # generates a random port

port_num = 8000

# make this optional
qr = pyqrcode.create(f'http://{ip}:{port_num}')
print(qr.terminal())

test_events = [Event('test1', icon_path='../static/play.png', exec_cmd='notify-send "adad"', exec_hotkey=None),
               Event('media toggle', icon_path=None, exec_cmd=None, exec_hotkey='space')]

test_events = {e.event: e for e in test_events}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", events=test_events.values())


@app.route("/event")
def do_event():
    # query is key and the default value is None
    key = request.args.get("key", "None")

    # presses key as it receives via GET
    success = True
    try:
        print(key)
        test_events[key].run_exec_cmd()
        test_events[key].run_exec_hotkey()
        sleep(0.3)
    except Exception as e:
        print(e)
        success = False

    return {"press": success}


# change the port to any number 8000 to 65535
app.run(host="0.0.0.0", port=port_num)

