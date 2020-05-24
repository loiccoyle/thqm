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
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--port", type=int, default=8888,
                        help="Port number.")
    parser.add_argument('-q', '--qrcode', action='store_true',
                        default=False,
                        help='Show the qrcode, requires "pyqrcode".')
    parser.add_argument("-pw", '--password', default=None,
                        help="Authentication password.")
    parser.add_argument('-u', '--username', default='thqm',
                        help="Authentication username, only used if a password is provided.")
    parser.add_argument('-s', '--seperator', default='\n',
                        help="Entry seperator pattern.")
    args = parser.parse_args()

    qr = generate_qr(password=args.password, port=args.port)


    if args.qrcode:
        if PYQRCODE_IMPORT:
            print(qr.terminal())
            sys.exit(0)
        else:
            print("'pyqrcode' not installed.", file=sys.stderr)
            sys.exit(1)

    start_server(events=[e.strip() for e in sys.stdin.read().split(args.seperator) if e],
                 username=args.username,
                 password=args.password,
                 port=args.port,
                 qrcode=PYQRCODE_IMPORT,
                 )

if __name__ == '__main__':
    main()