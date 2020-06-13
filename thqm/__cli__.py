#!/usr/bin/env python
import argparse
import sys

from .server import start_server
from .utils import (
    PYQRCODE_IMPORT,
    echo,
    generate_qr,
    get_styles,
    init_conf_folder,
    style_base_dir,
)


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
        "-pw", "--password", default=None, type=str, help="Authentication password."
    )
    parser.add_argument(
        "-u",
        "--username",
        default="thqm",
        type=str,
        help="Authentication username, only used if a PASSWORD is provided.",
    )
    parser.add_argument(
        "-s", "--seperator", default="\n", help="Entry seperator pattern.", type=str
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
    parser.add_argument(
        "--style",
        default="default",
        choices=[style.name for style in get_styles()],
        type=str,
        help="Page style.",
    )
    args = parser.parse_args()

    # init the configuration folder
    init_conf_folder()

    # get the base dir of the style.
    base_dir = style_base_dir(args.style)

    # if qr code and pyqrcode not installed
    if not PYQRCODE_IMPORT and (args.show_qrcode or not args.no_qrcode):
        print(
            "'pyqrcode' not installed. To install 'pip install pyqrcode'.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.show_qrcode or not args.no_qrcode:
        qr_path = base_dir / "static/qr_code.svg"
        qr = generate_qr(
            username=args.username,
            password=args.password,
            port=args.port,
            qr_path=qr_path,
        )
        if args.show_qrcode:
            echo(qr.terminal())
    else:
        qr_path = None

    try:
        start_server(
            events=[e.strip() for e in sys.stdin.read().split(args.seperator) if e],
            port=args.port,
            username=args.username,
            password=args.password,
            oneshot=args.oneshot,
            base_dir=base_dir,
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
    finally:
        # cleanup the qr_code.svg once done
        if qr_path is not None and qr_path.is_file():
            qr_path.unlink()


if __name__ == "__main__":
    main()
