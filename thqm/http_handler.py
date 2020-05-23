import shutil
from io import BytesIO
from pathlib import Path
from base64 import b64encode
from urllib.parse import unquote
from http.server import BaseHTTPRequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape

# from .settings import BASE_DIR
BASE_DIR = Path(__file__).absolute().parent


ENV = Environment(
    loader=PackageLoader('thqm', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def handler_factory(username:str='thqm', password:str=None, events:list=[], qrcode:bool=True):

    class HTTPHandler(BaseHTTPRequestHandler):

        extensions_map = {'.html': 'text/html',
                          '': 'application/octet-stream',  # Default
                          '.css': 'text/css',
                          '.png': 'image/png',
                          '.jpg': 'image/jpeg',
                          '.jpeg': 'image/jpeg'}

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
            """Serve a GET request."""
            if self.require_login:
                if self.headers.get("Authorization") == "Basic " + self._auth:
                    self._do_GET()
                else:
                    self.do_HEADAUTH()
            else:
                self._do_GET()

        def do_HEAD(self):
            """Serve a HEAD request."""
            f = self.send_head()
            if f:
                f.close()

        def do_HEADAUTH(self):
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
                if path == BASE_DIR or path in [BASE_DIR / e for e in self.events]:
                    if path != BASE_DIR:
                        print(path.name)
                        self.send_response(302)
                        self.send_header("Location", '/')
                        self.end_headers()
                        return None
                    contents = ENV.get_template('index.html').render(events=self.events,
                            qrcode=self.qrcode)
                    contents = contents.encode('utf8')
                    f = BytesIO(contents)
                    ctype = 'text/html'
                else:
                    try:
                        f = open(path, 'rb')
                    except IOError:
                        return None
                if not ctype:
                    ctype = self.guess_type(path)
                self.send_response(200)
                self.send_header("Content-type", ctype)
                self.end_headers()
                return f

        def translate_path(self, path:str) -> Path:
            """Translate a /-separated PATH to the local filename syntax.

            Components that mean special things to the local file system
            (e.g. drive or directory names) are ignored.  (XXX They should
            probably be diagnosed.)

            """
            # abandon query parameters
            path = path.split('?',1)[0]
            path = path.split('#',1)[0]
            # Don't forget explicit trailing slash when normalizing. Issue17324
            clean_path = unquote(path)[1:]
            path = BASE_DIR / clean_path
            return path

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

        def guess_type(self, path):
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
            if ext in self.extensions_map:
                return self.extensions_map.get(ext, self.extensions_map[''])

        def log_message(self, *args, **kwargs):
            '''Disable all prints.
            '''
            pass


    return HTTPHandler
