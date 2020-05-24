import socket
try:
    import pyqrcode
    PYQRCODE_IMPORT = True
except ImportError:
    PYQRCODE_IMPORT = False

from .settings import BASE_DIR

def generate_qr(port=8888, password=None, qr_path=BASE_DIR / 'static' / 'qr_code.svg'):

    if PYQRCODE_IMPORT:
        if password is not None:
            qr_url = f'http://{username}:{password}@{get_ip()}:{port}'
        else:
            qr_url = f'http://{get_ip()}:{port}'
        qr = pyqrcode.create(qr_url)
        qr.svg(qr_path, module_color="#000000", background='#ffffff')
    return qr


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # this sees if device is connected to internet
    ip = s.getsockname()[0]
    s.close()
    return ip
