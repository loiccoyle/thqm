<h1 align="center">thqm</h1>

<h3 align="center"><img src="./images/logo.svg" width="150"></h3>
<h5 align="center">Remote command execution made easy.</h5>
<p align="center">
  <a href="https://pypi.org/project/thqm/"><img src="https://img.shields.io/pypi/v/thqm"></a>
  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</p>

> `thqm` takes its name from the arabic تحكم, pronounced tahakum, meaning control.

`thqm` makes it very easy to setup a simple remote control interface on the host machine.

`thqm` is a nifty little HTTP server which reads from standard input. It dynamically generates a simple button menu based on the provided `stdin` and outputs any button the user presses to `stdout`.
In a sense its kind of like the [`dmenu`](https://tools.suckless.org/dmenu/)/[`rofi`](https://github.com/davatorium/rofi) of HTTP servers.

This makes it very flexible and script friendly. See the [examples](./examples) folder for some scripts.

# Installation
```shell
pip install thqm
```
`thqm` is compatible with linux & MacOS (maybe windows ?).

It usually is a good idea to use a virtual environment, or maybe consider using [pipx](https://github.com/pipxproject/pipx).

# Dependencies
`thqm` requires the following to run:
  * `python3`
  * `jinja`
  
Optional:
  * `pyqrcode` for qrcode generation.

# Usage
Check the [examples](./examples) folder for some usage examples.

```shell
$ thqm --help
usage: thqm [-h] [-p PORT] [-q] [-pw PASSWORD] [-u USERNAME] [-s SEPERATOR]
            [-o]

Start an interactive web page from standard input.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port number. (default: 8888)
  -q, --qrcode          Show the qrcode and exits, requires "pyqrcode".
                        (default: False)
  -pw PASSWORD, --password PASSWORD
                        Authentication password. (default: None)
  -u USERNAME, --username USERNAME
                        Authentication username, only used if a PASSWORD is
                        provided. (default: thqm)
  -s SEPERATOR, --seperator SEPERATOR
                        Entry seperator pattern. (default: )
  -o, --oneshot         Shutdown server after first click. (default: False)

```
Use the `-u` and `-pw` arguments to set a username and password to restrict access. The authentication is handled with [HTTP basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).

With the `-s` argument you can define the pattern on which to split `stdin`.

The `-o` flag will stop the server after the first button press.

The `-q` (requires `pyqrcode`) flag will print a qr-code in the terminal, this qr-code contains the credentials so it will bypass any authentication, the same is true for the in browser qr-code. This makes it particularly easy to share access with others.
<p align="center">
 <img src="./images/thqm_phone_portrait.png" width="200" />
</p>
