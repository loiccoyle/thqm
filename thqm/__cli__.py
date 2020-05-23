#!/usr/bin/env python
import sys
import argparse

from .server import start_server


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


    # print(sys.stdin.read().split())
    # print([e.strip() for e in sys.stdin.read().split(args.seperator) if e])
    start_server(events=[e.strip() for e in sys.stdin.read().split(args.seperator) if e],
                 username=args.username,
                 password=args.password,
                 port=args.port,
                 qrcode=args.qrcode,
                 )

if __name__ == '__main__':
    main()
