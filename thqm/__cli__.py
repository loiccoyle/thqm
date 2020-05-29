#!/usr/bin/env python
import sys
import argparse

from .utils import PYQRCODE_IMPORT
from .server import start_server
from .utils import generate_qr


def main():
    """cli
    """
    parser = argparse.ArgumentParser(prog='thqm',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Remote command execution made easy.')
    parser.add_argument("-p", "--port", type=int, default=8888,
                        help="Port number.")
    parser.add_argument('-q', '--qrcode', action='store_true', default=False,
                        help='Show the qrcode and exits, requires "pyqrcode".')
    parser.add_argument("-pw", '--password', default=None,
                        help="Authentication password.")
    parser.add_argument('-u', '--username', default='thqm',
                        help="Authentication username, only used if a PASSWORD is provided.")
    parser.add_argument('-s', '--seperator', default='\n',
                        help="Entry seperator pattern.")
    parser.add_argument('-o', '--oneshot', action='store_true', default=False,
                        help="Shutdown server after first click.")
    args = parser.parse_args()

    if PYQRCODE_IMPORT:
        qr = generate_qr(username=args.username, password=args.password, port=args.port)

    if args.qrcode:
        if PYQRCODE_IMPORT:
            print(qr.terminal(), flush=True)
        else:
            print("'pyqrcode' not installed. To install 'pip install pyqrcode'.", file=sys.stderr)
            sys.exit(1)

    try:
        start_server(events=[e.strip() for e in sys.stdin.read().split(args.seperator) if e],
                     username=args.username,
                     password=args.password,
                     port=args.port,
                     qrcode=PYQRCODE_IMPORT,
                     oneshot=args.oneshot,
                     )
    except KeyboardInterrupt:
        sys.exit(130)
    except BrokenPipeError:
        sys.exit(0)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
