import os
import sys
from pathlib import Path


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
        else:
            folder = Path(folder)
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
        qrcode (str): qrcode svg elements.
#}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>{{ title }}</title>
  </head>
  <body>
    <header>
      <div>
        <h2>{{ title }}</h1>
        {%- if qrcode_button -%}
          {{ qrcode|safe }}
        {%- endif -%}
        {%- if shutdown_button -%}
          <a href="./?shutdown")>shutdown</a>
        {%- endif -%}
      </div>
    </header>
    <hr/>
    {%- for e in events -%}
      <a href='./{{ e }}'>
        <pre><code>{{ e|safe }}</code></pre>
      </a>
    {%- endfor -%}
  </body>
</html>"""
