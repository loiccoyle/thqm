import argparse
from io import BytesIO
from pathlib import Path
from typing import Optional

import netifaces
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .settings import CONF_DIR, EXAMPLE_PURE_HTML, PKG_DIR

try:
    import pyqrcode

    PYQRCODE_IMPORT = True
except ImportError:
    PYQRCODE_IMPORT = False


def get_url(
    port: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    interface: Optional[str] = None,
) -> str:
    """Construct the url string.

    Args:
        port: port number.
        username: basic auth username.
        password: basic auth password.
        interface: network interface to use to find the local ip.
    """
    ip = get_ip(interface)
    if password is not None and username is not None:
        return f"http://{username}:{password}@{ip}:{port}/"
    return f"http://{ip}:{port}/"


def generate_qr(data: str) -> tuple:
    """Generate the qrcode containing login credential if provided.
    Requires 'pyqrcode'.

    Args:
        data: data to encode in qrcode.

    Returns:
        tuple of pyqrcode.qr object and qrcode svg string.
    """
    qrcode = pyqrcode.create(data)
    qr_buf = BytesIO()
    qrcode.svg(
        qr_buf,
        module_color="#000000",
        background="#ffffff",
        scale=5,
        lineclass="qrcode-line",
        svgclass="qrcode",
        omithw=True,
    )
    return qrcode, qr_buf.getvalue().decode("utf8")


def get_ip(interface: Optional[str] = None) -> str:
    """Gets host local network ip.

    Args:
        interface: network interface to use to find the local ip.

    Returns:
        Local network ip.
    """
    if interface is None:
        gateways = netifaces.gateways()[netifaces.AF_INET]
        # skip over tun interfaces, usually for vpns
        interface = [iface for _, iface, _ in gateways if not "tun" in iface][0]

    ips = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
    return ips["addr"]


def echo(msg: str):
    """Print and flush."""
    print(msg, flush=True)


def check_base_dir(folder: Path) -> bool:
    """Check to make sure the minimum requirements are met.

    Return:
        True if template/index.html exists in folder, False otherwise.
    """
    return (folder / "template").is_dir() and (folder / "template/index.html").is_file()


def get_styles() -> list:
    """Get the available styles."""
    return [
        style
        for style in list((PKG_DIR / "styles").glob("*")) + list(CONF_DIR.glob("*"))
        if style.is_dir() and check_base_dir(style)
    ]


def style_base_dir(style: str) -> Path:
    """Get style path from name."""
    styles = {style_path.name: style_path for style_path in get_styles()}
    return styles[style]


def create_jinja_env(folder: Path) -> Environment:
    """Create a jinja environment for the path. folder should contain a
    template/index.html file.
    """
    if not check_base_dir(folder):
        raise FileNotFoundError(
            f"'{folder}' not valid, must contain 'template/index.html'."
        )
    env = Environment(
        loader=FileSystemLoader(folder / "template"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    return env


def init_conf_folder():
    """Initialize the config folder contents."""
    folders = [
        CONF_DIR,
        CONF_DIR / "pure_html",
        CONF_DIR / "pure_html/static",
        CONF_DIR / "pure_html/template",
    ]
    if not CONF_DIR.is_dir():
        for folder in folders:
            if not folder.is_dir():
                folder.mkdir()
        (CONF_DIR / "pure_html/template/index.html").write_text(EXAMPLE_PURE_HTML)


class ArgFormatter(argparse.RawTextHelpFormatter):
    def _get_help_string(self, action) -> str:
        """Small hack to use raw printing on default values."""
        help_str = action.help
        if "%(default)" not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help_str += " (default: %(default)r)"
        return help_str
