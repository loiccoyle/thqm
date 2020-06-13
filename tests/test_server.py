import unittest

from io import BytesIO
from base64 import b64decode
from thqm import server


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
    def _test(self, TestableHandler, request):
        handler = TestableHandler(MockRequest(request), (0, 0), None)
        return handler.wfile.getvalue()

    def test_handler_factory(self):
        Handler = server.handler_factory(
            username="lcoyle",
            password="hunter2",
            events=["event1", "event2"],
            qrcode=True,
            oneshot=False,
        )
        Handler = make_testable(Handler)
        handler = Handler(MockRequest(b"/"), (0, 0), None)
        self.assertEqual(handler.require_login, True)

    def test_Handler_unauthorized(self):
        Handler = server.handler_factory(
            username="lcoyle",
            password="hunter2",
            events=["event1", "event2"],
            qrcode=True,
            oneshot=False,
        )
        Handler = make_testable(Handler)
        self.assertTrue(
            self._test(Handler, b"/").startswith(b"HTTP/1.0 401 Unauthorized")
        )

    def test_Handler_authorized(self):
        Handler = server.handler_factory(
            username="lcoyle",
            password=None,
            events=["event1", "event2"],
            qrcode=True,
            oneshot=False,
        )
        Handler = make_testable(Handler)
        response = self._test(Handler, b"/")
        response = response.decode("utf8")
        self.assertTrue("HTTP/1.0 200 OK" in response)
        self.assertTrue("qrcode" in response)
        for event in ["event1", "event2"]:
            self.assertTrue(event in response)

        response = self._test(Handler, b"/event1").decode("utf8")
        self.assertTrue("302 Found" in response)
        self.assertTrue("Location: /" in response)

        response = self._test(Handler, b"/event2").decode("utf8")
        self.assertTrue("302 Found" in response)
        self.assertTrue("Location: /" in response)

    def test_Handler_noqr(self):
        Handler = server.handler_factory(
            username="lcoyle",
            password=None,
            events=["event1", "event2"],
            qrcode=False,
            oneshot=False,
        )
        Handler = make_testable(Handler)
        response = self._test(Handler, b"/")
        response = response.decode("utf8")
        self.assertTrue("HTTP/1.0 200 OK" in response)
        self.assertTrue("qrcode" not in response)
        for event in ["event1", "event2"]:
            self.assertTrue(event in response)

    def test_Handler_noshutdown(self):
        Handler = server.handler_factory(
            username="lcoyle",
            password=None,
            events=["event1", "event2"],
            qrcode=True,
            oneshot=False,
            shutdown_button=False,
        )
        Handler = make_testable(Handler)
        response = self._test(Handler, b"/")
        response = response.decode("utf8")
        self.assertTrue("HTTP/1.0 200 OK" in response)
        self.assertTrue("shutdown" not in response)
        for event in ["event1", "event2"]:
            self.assertTrue(event in response)

    def test_Handler_title(self):
        Handler = server.handler_factory(
            username="lcoyle",
            password=None,
            events=["event1", "event2"],
            qrcode=True,
            oneshot=False,
            shutdown_button=True,
            title="some awesome title",
        )
        Handler = make_testable(Handler)
        response = self._test(Handler, b"/")
        response = response.decode("utf8")
        self.assertTrue("HTTP/1.0 200 OK" in response)
        self.assertTrue("some awesome title" in response)
        for event in ["event1", "event2"]:
            self.assertTrue(event in response)
