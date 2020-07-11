<h1 align="center">thqm</h1>
<h3 align="center"><img src="https://i.imgur.com/gVB270Z.png" width="150"></h3>
<h5 align="center">Remote command execution made easy.</h5>

<p align="center">
  <a href="https://github.com/loiccoyle/thqm/actions?query=workflow%3Atests"><img src="https://github.com/loiccoyle/thqm/workflows/tests/badge.svg"></a>
  <a href="https://pypi.org/project/thqm/"><img src="https://img.shields.io/pypi/v/thqm"></a>
  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-informational">
</p>

<img src="https://i.imgur.com/lYwkjzP.png" align="right" width='170px'>
<img src="https://i.imgur.com/ezJgbhX.png" align="right" width='170px'>


> `thqm` takes its name from the arabic تحكم, pronounced tahakum, meaning control.

`thqm` makes it very easy to setup a simple remote control interface on the host machine.

`thqm` is a nifty little HTTP server which reads from standard input. It dynamically generates a simple button menu based on the provided `stdin` and outputs any button the user presses to `stdout`.
In a sense its kind of like the [`dmenu`](https://tools.suckless.org/dmenu/)/[`rofi`](https://github.com/davatorium/rofi) of HTTP servers.

This makes it very flexible and script friendly. See the [examples](./examples) folder for some scripts.

&nbsp;

&nbsp;

# Installation
```shell
pip install thqm
```

or with `pyqrcode`

```shell
pip install 'thqm[qrcode]'
```

`thqm` should work on linux, MacOS and Windows.

It usually is a good idea to use a virtual environment, or maybe consider using [pipx](https://github.com/pipxproject/pipx).

# Dependencies
`thqm` requires the following to run:
  * `python3`
  * `jinja`

Optional:
  * `pyqrcode` for qrcode generation.

# Configuration
`thqm` will create a config folder:
  * Linux: `$XDG_CONFIG_HOME/thqm` (or `$HOME/.config/thqm` if `$XDG_CONFIG_HOME` is not set)
  * MacOS: `~/Library/Application Support/thqm`
  * Windows: `%LOCALAPPDATA%/thqm` (or `~/thqm`)

This folder holds `thqm`'s custom styles. A bare bone example, `pure_html`, will be created.

To add your own custom style, follow the folder structure of the provided example. Maybe have a look at the [`default`](https://github.com/loiccoyle/thqm/tree/master/thqm/styles/default) style.

**Note:** the base folder of the server will the style's folder. So to access files in the `static` folder from your `index.html`:

```html
<link rel="stylesheet" type="text/css" href="static/index.css">
```

# Usage
Check the [examples](./examples) folder for some usage examples.

```
$ thqm --help

usage: thqm [-h] [-p PORT] [-q] [-pw PASSWORD] [-u USERNAME] [-s SEPERATOR] [-o] [-t TITLE]
            [--no-shutdown] [--no-qrcode] [--style {default,pure_html}]

Remote command execution made easy.

Custom styles should be added to /home/lcoyle/.config/thqm

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port number. (default: 8901)
  -u USERNAME, --username USERNAME
                        Authentication username, only used if a PASSWORD is provided. (default: 'thqm')
  -pw PASSWORD, --password PASSWORD
                        Authentication password. (default: None)
  -s SEPERATOR, --seperator SEPERATOR
                        Entry seperator pattern. (default: '\n')
  -t TITLE, --title TITLE
                        Page title. (default: 'thqm')
  --style {default,pure_html}
                        Page style. (default: 'default')
  --extra-template-args JSON
                        Extra template arguments, json string. (default: '{}')
  -q, --show-qrcode     Show the qrcode in terminal, requires "pyqrcode". (default: False)
  -l, --show-url        Show the page url. (default: False)
  -o, --oneshot         Shutdown server after first click. (default: False)
  --no-shutdown         Remove server shutdown button. (default: False)
  --no-qrcode           Remove qrcode button. (default: False)
  --version             Show version and exit. (default: False)
```
Use the `-u` and `-pw` arguments to set a username and password to restrict access. The authentication is handled with [HTTP basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).

With the `-s` argument you can define the pattern on which to split `stdin`.

The `-o` flag will stop the server after the first button press.

The `-q` (requires `pyqrcode`) flag will print a qr-code in the terminal, this qr-code contains the credentials so it will bypass any authentication, the same is true for the in browser qr-code. This makes it particularly easy to share access with others.

Use `-t` to change the page title.

`--no-shutdown` removes the shutdown server button.

`--no-qrcode` removes the qrcode button.

Select the page style using the `--style` argument. You can add custom styles in `thqm`'s config folder.
