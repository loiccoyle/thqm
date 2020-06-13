#!/usr/bin/env python
import argparse
import sys

from .server import start_server
from .utils import PYQRCODE_IMPORT, echo, generate_qr


def main():
    """thqm cli.
    """
    parser = argparse.ArgumentParser(
        prog="thqm",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Remote command execution made easy.",
    )
    parser.add_argument("-p", "--port", type=int, default=8901, help="Port number.")
    parser.add_argument(
        "-q",
        "--show-qrcode",
        action="store_true",
        default=False,
        help='Show the qrcode in terminal, requires "pyqrcode".',
    )
    parser.add_argument(
        "-pw", "--password", default=None, help="Authentication password."
    )
    parser.add_argument(
        "-u",
        "--username",
        default="thqm",
        help="Authentication username, only used if a PASSWORD is provided.",
    )
    parser.add_argument(
        "-s", "--seperator", default="\n", help="Entry seperator pattern."
    )
    parser.add_argument(
        "-o",
        "--oneshot",
        action="store_true",
        default=False,
        help="Shutdown server after first click.",
    )
    parser.add_argument("-t", "--title", default="thqm", help="Page title.", type=str)
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
    args = parser.parse_args()

    if not PYQRCODE_IMPORT and (args.show_qrcode or not args.no_qrcode):
        print(
            "'pyqrcode' not installed. To install 'pip install pyqrcode'.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.show_qrcode or not args.no_qrcode:
        qr = generate_qr(username=args.username, password=args.password, port=args.port)
        if args.show_qrcode:
            echo(qr.terminal())

    try:
        start_server(
            events=[e.strip() for e in sys.stdin.read().split(args.seperator) if e],
            username=args.username,
            password=args.password,
            port=args.port,
            oneshot=args.oneshot,
            qrcode_button=not args.no_qrcode,
            shutdown_button=not args.no_shutdown,
            title=args.title,
        )
    except KeyboardInterrupt:
        sys.exit(130)
    except BrokenPipeError:
        sys.exit(0)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
