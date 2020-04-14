import sys
import click
import socket
import pyqrcode
import logging

from pathlib import Path
from time import sleep
from flask import Flask, render_template, request
from waitress import serve

from .parser import Parser

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def start_server(config_path=None, port_number=8800, verbosity=2, qrcode=False):
    # get the ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # this sees if device is connected to internet
    ip = s.getsockname()[0]
    s.close()

    if port_number is None:
        port_number = randint(49152, 65535)

    config_path = Path(config_path)

    qr_path = Path(__file__).parent / 'static' / 'qr_code.svg'
    qr = pyqrcode.create(f'http://{ip}:{port_number}')
    qr.svg(qr_path, module_color="#000000", background='#ffffff')
    if qrcode:
        print(qr.terminal())

    events = Parser(config_path).parse()

    thqm = Flask(__name__.split('.')[0])

    @thqm.route("/")
    def index():
        return render_template("index.html", events=events.values())


    @thqm.route("/event")
    def do_event():
        # query is key and the default value is None
        key = request.args.get("key", "None")
        if verbosity >= 1:
            print(key, flush=True)

        # presses key as it receives via GET
        success = True
        if key == 'shutdown_rc_server':
            shutdown_server()

        try:
            events[key].run_exec_cmd()
            events[key].run_exec_hotkey()
            sleep(0.3)
        except Exception as e:
            print(e)
            success = False

        return {"press": success}

    serve(thqm, host="0.0.0.0", port=port_number, _quiet=verbosity <= 1)

