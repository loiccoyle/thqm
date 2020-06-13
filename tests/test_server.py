import unittest
from base64 import b64decode
from io import BytesIO

from thqm import server, utils


def make_testable(Handler):
    class TestableHandler(Handler):
        # On Python3, in socketserver.StreamRequestHandler, if this is
        # set it will use makefile() to produce the output stream. Otherwise,
        # it will use socketserver._SocketWriter, and we won't be able to get
        # to the data
        wbufsize = 1

        def finish(self):
            # Do not close self.wfile, so we can read its value
            self.wfile.flush()
            self.rfile.close()

        def date_time_string(self, timestamp=None):
            """Mocked date time string.
            """
            return "DATETIME"

        def version_string(self):
            """Mock the server id.
            """
            return "BaseHTTP/x.x Python/x.x.x"

    return TestableHandler


class MockSocket:
    def getsockname(self):
        return ("sockname",)


class MockRequest:
    _sock = MockSocket()

    def __init__(self, path):
        self._path = path

    def makefile(self, *args, **kwargs):
        if args[0] == "rb":
            return BytesIO(b"GET %s HTTP/1.0" % self._path)
        elif args[0] == "wb":
            return BytesIO(b"")
        else:
            raise ValueError("Unknown file type to make", args, kwargs)


class TestHandler(unittest.TestCase):
    def _render_template(self, **kwargs):
        base_dir = utils.style_base_dir("default")
        jinja_env = utils.create_jinja_env(base_dir)
        template = jinja_env.get_template("index.html")
        return BytesIO(template.render(**kwargs).encode("utf8"))

    def _get_base_dir(self):
        return utils.style_base_dir("default")

    def _test(self, TestableHandler, request):
        handler = TestableHandler(MockRequest(request), (0, 0), None)
        return handler.wfile.getvalue()

    def test_handler_factory(self):
        Handler = server.handler_factory(
            base_dir=self._get_base_dir(),
            username="lcoyle",
            password="hunter2",
            oneshot=False,
            jinja_template_rendered=self._render_template(
                events=["event1", "event2"], qrcode_button=True, shutdown_button=True
            ),
        )

        Handler = make_testable(Handler)
        handler = Handler(MockRequest(b"/"), (0, 0), None)
        self.assertEqual(handler.require_login, True)

    def test_Handler_unauthorized(self):
        Handler = server.handler_factory(
            base_dir=self._get_base_dir(),
            username="lcoyle",
            password="hunter2",
            oneshot=False,
            jinja_template_rendered=self._render_template(
                events=["event1", "event2"], qrcode_button=True, shutdown_button=True
            ),
        )
        Handler = make_testable(Handler)
        self.assertTrue(
            self._test(Handler, b"/").startswith(b"HTTP/1.0 401 Unauthorized")
        )

    def test_Handler_authorized(self):
        Handler = server.handler_factory(
            base_dir=self._get_base_dir(),
            username="lcoyle",
            password=None,
            oneshot=False,
            jinja_template_rendered=self._render_template(
                events=["event1", "event2"], qrcode_button=True, shutdown_button=True
            ),
        )
        Handler = make_testable(Handler)
        response = self._test(Handler, b"/")
        response = response.decode("utf8")
        self.assertTrue("HTTP/1.0 200 OK" in response)
        self.assertTrue("qrcode-btn" in response)
        self.assertTrue("shutdown-btn" in response)
        for event in ["event1", "event2"]:
            self.assertTrue(event in response)

    def test_Handler_noqr(self):
        Handler = server.handler_factory(
            base_dir=self._get_base_dir(),
            username="lcoyle",
            password=None,
            oneshot=False,
            jinja_template_rendered=self._render_template(
                events=["event1", "event2"], qrcode_button=False, shutdown_button=True
            ),
        )
        Handler = make_testable(Handler)
        response = self._test(Handler, b"/")
        response = response.decode("utf8")
        self.assertTrue("HTTP/1.0 200 OK" in response)
        self.assertTrue("qrcode-btn" not in response)
        self.assertTrue("shutdown-btn" in response)
        for event in ["event1", "event2"]:
            self.assertTrue(event in response)

    def test_Handler_noshutdown(self):
        Handler = server.handler_factory(
            base_dir=self._get_base_dir(),
            username="lcoyle",
            password=None,
            oneshot=False,
            jinja_template_rendered=self._render_template(
                events=["event1", "event2"], qrcode_button=True, shutdown_button=False
            ),
        )
        Handler = make_testable(Handler)
        response = self._test(Handler, b"/")
        response = response.decode("utf8")
        self.assertTrue("HTTP/1.0 200 OK" in response)
        self.assertTrue("qrcode-btn" in response)
        self.assertTrue("shutdown-btn" not in response)
        for event in ["event1", "event2"]:
            self.assertTrue(event in response)

    def test_Handler_title(self):
        Handler = server.handler_factory(
            base_dir=self._get_base_dir(),
            username="lcoyle",
            password=None,
            oneshot=False,
            jinja_template_rendered=self._render_template(
                events=["event1", "event2"],
                qrcode_button=True,
                shutdown_button=True,
                title="some awesome title",
            ),
        )
        Handler = make_testable(Handler)
        response = self._test(Handler, b"/")
        response = response.decode("utf8")
        self.assertTrue("HTTP/1.0 200 OK" in response)
        self.assertTrue("some awesome title" in response)
        self.assertTrue("qrcode-btn" in response)
        self.assertTrue("shutdown-btn" in response)
        for event in ["event1", "event2"]:
            self.assertTrue(event in response)
