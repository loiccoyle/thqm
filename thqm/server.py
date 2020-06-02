import sys
import shutil
import threading

from io import BytesIO
from pathlib import Path
from base64 import b64encode
from urllib.parse import unquote
from http.server import BaseHTTPRequestHandler, HTTPServer

from .utils import PYQRCODE_IMPORT
from .settings import BASE_DIR, JINJA_ENV


def handler_factory(username:str='thqm',
                    password:str=None,
                    events:list=[],
                    qrcode:bool=True,
                    oneshot:bool=False):
    """Create a HTTPHandler class with the desired properties.

    Args:
        username: basic auth username.
        password: basic auth password.
        events: list of events with which to populate the page.
        qrcode: user qrcode in the template.
        oneshot: stop server after first click.

    Returns:
        HTTPHandler class.
    """

    class HTTPHandler(BaseHTTPRequestHandler):

        extensions_map = {'.html': 'text/html',
                          '': 'application/octet-stream',  # Default
                          '.css': 'text/css',
                          '.js': 'text/javascript',
                          '.png': 'image/png',
                          '.jpg': 'image/jpeg',
                          '.jpeg': 'image/jpeg',
                          '.svg': 'image/svg+xml'}

        def __init__(self, *args, **kwargs):
            self.qrcode = qrcode
            self.events = events
            self.require_login = password is not None
            self._auth = b64encode(f"{username}:{password}".encode()).decode()
            super().__init__(*args, **kwargs)

        def _do_GET(self):
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()

        def do_GET(self):
            """Serve a GET request.
            """
            if self.require_login:
                if self.headers.get("Authorization") == "Basic " + self._auth:
                    self._do_GET()
                else:
                    self.do_HEADAUTH()
            else:
                self._do_GET()

        def do_HEAD(self):
            """Serve a HEAD request.
            """
            f = self.send_head()
            if f:
                f.close()

        def do_HEADAUTH(self):
            """Handle the authentication in the header.
            """
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"thqm\"')
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def send_head(self):
            """Common code for GET and HEAD commands.

            This sends the response code and MIME headers.

            Return value is either a file object (which has to be copied
            to the outputfile by the caller unless the command was HEAD,
            and must be closed by the caller under all circumstances), or
            None, in which case the caller has nothing further to do.
            """
            path = self.translate_path(self.path)
            f = None
            ctype = None

            if self.get_query(self.path) == 'shutdown':
                # shutdown server
                self.shutdown()
                return
            elif path in (BASE_DIR / e for e in self.events):
                # If event
                print(path.relative_to(BASE_DIR), flush=True)
                if oneshot:
                    # shutdown after print
                    self.shutdown()
                    return
                self.send_response(302)
                self.send_header("Location", '/')
                self.end_headers()
                return
            elif path == BASE_DIR:
                # if control panel
                contents = JINJA_ENV.get_template('index.html').render(events=self.events,
                                                                       qrcode=self.qrcode)
                f = BytesIO(contents.encode('utf8'))
                ctype = 'text/html'
            elif (BASE_DIR / 'static') in path.parents:
                # if anything else
                try:
                    f = open(path, 'rb')
                except IOError:
                    return
            else:
                return
            if not ctype:
                ctype = self.guess_type(path)
            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.end_headers()
            return f

        def translate_path(self, path:str) -> Path:
            """Translate a /-separated PATH to the local filename syntax.
            """
            # abandon query parameters
            path = path.split('?',1)[0]
            path = path.split('#',1)[0]
            # remove first /
            return BASE_DIR / unquote(path)[1:]

        def get_query(self, path:str) -> Path:
            """Get the first query parameter.
            """
            path = path.split('?', 1)
            if len(path) > 1:
                return path[1]

        def shutdown(self):
            """Shutdown the server.
            """
            killer = threading.Thread(target=self.server.shutdown)
            killer.start()

        def copyfile(self, source, outputfile):
            """Copy all data between two file objects.

            The SOURCE argument is a file object open for reading
            (or anything with a read() method) and the DESTINATION
            argument is a file object open for writing (or
            anything with a write() method).

            The only reason for overriding this would be to change
            the block size or perhaps to replace newlines by CRLF
            -- note however that this the default server uses this
            to copy binary data as well.
            """
            shutil.copyfileobj(source, outputfile)

        def guess_type(self, path:Path) -> str:
            """Guess the type of a file.

            Argument is a PATH (a filename).

            Return value is a string of the form type/subtype,
            usable for a MIME Content-type header.

            The default implementation looks the file's extension
            up in the table self.extensions_map, using application/octet-stream
            as a default; however it would be permissible (if
            slow) to look inside the data to make a better guess.
            """
            ext = path.suffix.lower()
            return self.extensions_map.get(ext, self.extensions_map[''])

        def log_message(self, *args, **kwargs):
            """Disable all prints.
            """
            pass


    return HTTPHandler


def start_server(events:list=[],
                 port:int=8888,
                 username:str='thqm',
                 password:str=None,
                 qrcode=PYQRCODE_IMPORT,
                 oneshot=False):
    """Start the server.

    Args:
        events: list of events.
        port: port number on which to run the server.
        username: login username.
        password: login password.
        qrcode: control whether to use qrcode.
        oneshot: stop server after first click.
    """

    handler = handler_factory(events=events,
                              username=username,
                              password=password,
                              qrcode=qrcode,
                              oneshot=oneshot)

    server_address = ('', port)
    httpd = HTTPServer(server_address, handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        raise
