#!/usr/bin/env python
import argparse
import json
import sys

from . import __version__
from .server import start_server
from .settings import CONF_DIR
from .utils import (
    PYQRCODE_IMPORT,
    ArgFormatter,
    echo,
    generate_qr,
    get_styles,
    get_url,
    init_conf_folder,
    style_base_dir,
)


def main():
    """thqm cli."""
    # init the configuration folder
    init_conf_folder()

    # argument parsing
    parser = argparse.ArgumentParser(
        prog="thqm",
        formatter_class=ArgFormatter,
        description=f"""\
Remote command execution made easy.

Custom styles should be added to {CONF_DIR}
""",
    )
    parser.add_argument("-p", "--port", type=int, default=8901, help="Port number.")
    parser.add_argument(
        "-u",
        "--username",
        default="thqm",
        type=str,
        help="Authentication username, only used if a PASSWORD is provided.",
    )
    parser.add_argument(
        "-pw", "--password", default=None, type=str, help="Authentication password."
    )
    parser.add_argument(
        "-s", "--seperator", default="\n", help="Entry seperator pattern.", type=str
    )
    parser.add_argument(
        "-t",
        "--title",
        default="thqm",
        help="Page title.",
        type=str,
    )
    parser.add_argument(
        "--style",
        default="default",
        choices=[style.name for style in get_styles()],
        type=str,
        help="Page style.",
    )
    parser.add_argument(
        "--extra-template-args",
        type=json.loads,
        help="Extra template arguments, json string.",
        default="{}",
        metavar="JSON",
    )
    parser.add_argument(
        "-q",
        "--show-qrcode",
        action="store_true",
        default=False,
        help='Show the qrcode in terminal, requires "pyqrcode".',
    )
    parser.add_argument(
        "-sq",
        "--save-qrcode",
        default=None,
        type=str,
        help='Save the qrcode png to the provided path, requires "pyqrcode".',
        metavar="PATH"
    )
    parser.add_argument(
        "-l",
        "--show-url",
        action="store_true",
        default=False,
        help="Show the page url.",
    )
    parser.add_argument(
        "-o",
        "--oneshot",
        action="store_true",
        default=False,
        help="Shutdown server after first click.",
    )
    parser.add_argument(
        "--no-shutdown",
        action="store_true",
        default=False,
        help="Remove server shutdown button.",
    )
    parser.add_argument(
        "--no-qrcode",
        action="store_true",
        default=not PYQRCODE_IMPORT,
        help="Remove qrcode button.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        default=False,
        help="Show version and exit.",
    )
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    # get the base dir of the style.
    base_dir = style_base_dir(args.style)

    # determine the page url (with login information)
    page_url = get_url(args.port, args.username, args.password)
    if args.show_url:
        echo(page_url)

    # if qrcode and pyqrcode not installed
    if not PYQRCODE_IMPORT and (
        args.show_qrcode or not args.no_qrcode or args.save_qrcode is not None
    ):
        print(
            "Can't create qrcode, 'pyqrcode' not installed. To install 'pip install pyqrcode'.",
            file=sys.stderr,
        )
        sys.exit(1)

    # if the qrcode is required
    if args.show_qrcode or not args.no_qrcode:
        # qr_path = base_dir / "static/qr_code.svg"
        qrcode, qrsvg = generate_qr(page_url)
        if args.show_qrcode:
            echo(qrcode.terminal())
        if args.save_qrcode is not None:
            qrcode.png(args.save_qrcode, scale=5)
    else:
        qrsvg = None

    # render page and start the server
    try:
        start_server(
            events=[e.strip() for e in sys.stdin.read().split(args.seperator) if e],
            port=args.port,
            username=args.username,
            password=args.password,
            qrsvg=qrsvg,
            oneshot=args.oneshot,
            base_dir=base_dir,
            qrcode_button=not args.no_qrcode,
            shutdown_button=not args.no_shutdown,
            title=args.title,
            **args.extra_template_args,
        )
    except KeyboardInterrupt:
        sys.exit(130)
    except BrokenPipeError:
        sys.exit(0)
    except Exception as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
