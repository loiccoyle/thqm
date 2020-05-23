import sys
try:
    import pyqrcode
    PYQRCODE_IMPORT = True
except ImportError:
    PYQRCODE_IMPORT = False
from http.server import HTTPServer

from .utils import get_ip
from .settings import BASE_DIR
from .http_handler import handler_factory


def start_server(events:list=[],
                 port:int=8888,
                 qrcode:bool=False,
                 username:str='thqm',
                 password:str=None):

    if PYQRCODE_IMPORT:
        qr_path = BASE_DIR / 'static' / 'qr_code.svg'
        if password is not None:
            qr_url = f'http://{username}:{password}@{get_ip()}:{port}'
        else:
            qr_url = f'http://{get_ip()}:{port}'
        qr = pyqrcode.create(qr_url)
        qr.svg(qr_path, module_color="#000000", background='#ffffff')
    if qrcode:
        if PYQRCODE_IMPORT:
            print(qr.terminal())
        else:
            print("'pyqrcode' not installed.", file=sys.stderr)


    handler = handler_factory(events=events,
                              username=username,
                              password=password,
                              qrcode=PYQRCODE_IMPORT)

    server_address = ('', port)
    httpd = HTTPServer(server_address, handler)
    httpd.serve_forever()
