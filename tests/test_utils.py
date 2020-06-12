import unittest
from pathlib import Path
from shutil import rmtree
from thqm import utils


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

    def tearDown(self):
        rmtree(self.test_folder)
