import os
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape


def get_conf_path() -> Path:
    """Platform agnostic config directory.

    Returns:
        config folder path.
    """
    if PLATFORM.startswith("win"):
        key = "LOCALAPPDATA"
        folder = os.environ.get(key)
        if folder is None:
            folder = Path.home()
        return folder / "thqm"
    if PLATFORM == "darwin":
        return Path("~/Library/Application Support").expanduser() / "thqm"
    return (
        Path(os.environ.get("XDG_CONFIG_HOME", Path("~/.config").expanduser())) / "thqm"
    )


PLATFORM = sys.platform
PKG_DIR = Path(__file__).absolute().parent
CONF_DIR = get_conf_path()
EXAMPLE_PURE_HTML = """\
{# thqm template
    Pure html, no bells or whistles.

    args:
        title (str): page title.
        qrcode_button (bool): show qrcode button.
        shutdown_button (bool): show shutdown button.
        events (list): list of strings.
#}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <!-- <meta name="viewport" content="width=device-width, initial-scale=1" /> -->
    <title>{{ title }}</title>
  </head>

  <body>
    <header>
      <div>
        <h2>{{ title }}</h1>
        {% if qrcode_button %}
          <a href='static/qr_code.svg'>qrcode</a>
        {% endif %}
        {% if shutdown_button %}
          <a href="./?shutdown")>shutdown</a>
        {% endif %}
      </div>
    </header>
    <hr/>
    {% for e in events %}
      <a href='./{{ e }}'>
        <pre><code>{{ e|safe }}</code></pre>
      </a>
    {% endfor %}
  </body>
</html>"""
