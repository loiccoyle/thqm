import unittest
from pathlib import Path
from shutil import rmtree

from thqm import settings, utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_folder = Path("test_utils")
        self.test_folder.mkdir()

    def test_get_ip(self):
        utils.get_ip()

    def test_generate_qr(self):
        if utils.PYQRCODE_IMPORT:
            qr, qrsvg = utils.generate_qr(data="somedata")
            self.assertEqual(qr.data.decode("utf8"), "somedata")

    def test_get_url(self):
        url = utils.get_url(9809, "aaa", "hunter2")
        self.assertEqual(url, f"http://aaa:hunter2@{utils.get_ip()}:9809/")
        url = utils.get_url(9809, "aa", None)
        self.assertEqual(url, f"http://{utils.get_ip()}:9809/")

    def test_echo(self):
        utils.echo("test echo")

    def test_check_base_dir(self):
        self.assertFalse(utils.check_base_dir(self.test_folder))
        self.assertTrue(utils.check_base_dir(utils.style_base_dir("default")))

    def test_get_styles(self):
        self.assertTrue(
            set((settings.PKG_DIR / "styles").glob("*")) <= set(utils.get_styles())
        )

    def test_style_base_dir(self):
        self.assertEqual(
            utils.style_base_dir("default"), settings.PKG_DIR / "styles/default"
        )

    def test_create_jinja_env(self):
        env = utils.create_jinja_env(utils.style_base_dir("default"))
        self.assertTrue("index.html" in env.list_templates())
        with self.assertRaises(FileNotFoundError):
            utils.create_jinja_env(Path(__file__))

    def tearDown(self):
        rmtree(self.test_folder)
