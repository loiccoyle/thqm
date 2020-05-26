import socket
from pathlib import Path
try:
    import pyqrcode
    PYQRCODE_IMPORT = True
except ImportError:
    PYQRCODE_IMPORT = False

from .settings import BASE_DIR

def generate_qr(port:int=8888, username:str='thqm', password:str=None,
                qr_path:Path=BASE_DIR / 'static' / 'qr_code.svg'):
    '''Generate the qrcode containing login credential if provided.
    '''

    if password is not None:
        qr_url = f'http://{username}:{password}@{get_ip()}:{port}/'
    else:
        qr_url = f'http://{get_ip()}:{port}/'
    qr = pyqrcode.create(qr_url)
    qr.svg(qr_path, module_color="#000000", background='#ffffff')
    return qr


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # checks if device is connected to internet
    ip = s.getsockname()[0]
    s.close()
    return ip
