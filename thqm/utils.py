import socket
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

from .settings import CONF_DIR, EXAMPLE_PURE_HTML, PKG_DIR, PLATFORM

try:
    import pyqrcode

    PYQRCODE_IMPORT = True
except ImportError:
    PYQRCODE_IMPORT = False


def generate_qr(
    port: int = 8888,
    username: str = "thqm",
    password: str = None,
    qr_path: Path = PKG_DIR / "styles/default/static/qr_code.svg",
):
    """Generate the qrcode containing login credential if provided.
    Requires 'pyqrcode'.

    Args:
        port: port number.
        username: login username.
        password: login password.
        qr_path: path where to store the generated qr code svg.

    Returns:
        A pyqrcode.qr object containing the url and login credentials if
        provided.
    """

    if password is not None:
        qr_url = f"http://{username}:{password}@{get_ip()}:{port}/"
    else:
        qr_url = f"http://{get_ip()}:{port}/"
    qr = pyqrcode.create(qr_url)
    qr.svg(qr_path, module_color="#000000", background="#ffffff")
    return qr


def get_ip() -> str:
    """Gets host local ip.

    Returns:
        LAN ip.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # checks if device is connected to internet
    ip = s.getsockname()[0]
    s.close()
    return ip


def echo(msg: str):
    """Print and flush.
    """
    print(msg, flush=True)


def check_base_dir(custom_folder: Path) -> bool:
    """Check to make sure the minimum requirements are met.

    Return:
        True if templates/index.html exists in custom_folder, False otherwise.
    """
    return (
        (custom_folder / "static").is_dir()
        and (custom_folder / "templates").is_dir()
        and (custom_folder / "templates/index.html").is_file()
    )


def get_styles() -> list:
    """Get the available styles.
    """
    return [
        style
        for style in list((PKG_DIR / "styles").glob("*")) + list(CONF_DIR.glob("*"))
        if style.is_dir() and check_base_dir(style)
    ]


def style_base_dir(style: str) -> Path:
    """Get style path from name.
    """
    styles = {style_path.name: style_path for style_path in get_styles()}
    return styles[style]


def create_jinja_env(custom_folder: Path = None) -> Environment:
    """Create a jinja environment for the custom path. custom_folder should contain a
    templates/index.html file.
    """
    if custom_folder is not None:
        if not check_base_dir(custom_folder):
            raise FileNotFoundError(
                f"'{custom_folder}' not valid, must contain 'templates/index.html'."
            )
        else:
            env = Environment(
                loader=FileSystemLoader(custom_folder / "templates"),
                autoescape=select_autoescape(["html", "xml"]),
            )
    else:
        env = Environment(
            loader=PackageLoader("thqm", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )
    return env


def init_conf_folder():
    folders = [
        CONF_DIR,
        CONF_DIR / "pure_html",
        CONF_DIR / "pure_html/static",
        CONF_DIR / "pure_html/templates",
    ]
    if not CONF_DIR.is_dir():
        for folder in folders:
            if not folder.is_dir():
                folder.mkdir()
        (CONF_DIR / "pure_html/templates/index.html").write_text(EXAMPLE_PURE_HTML)
