import unittest
from pathlib import Path
from shutil import rmtree

from thqm import settings, utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_folder = Path("test_utils")
        self.test_folder.mkdir()

    def test_generate_qr(self):
        if utils.PYQRCODE_IMPORT:
            qr = utils.generate_qr(
                port=8888,
                username="thqm",
                password=None,
                qr_path=self.test_folder / "test_qr.svg",
            )
            self.assertTrue((self.test_folder / "test_qr.svg").is_file())
            self.assertEqual(qr.data.decode("utf8"), f"http://{utils.get_ip()}:8888/")

    def test_get_ip(self):
        utils.get_ip()

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

    def tearDown(self):
        rmtree(self.test_folder)
