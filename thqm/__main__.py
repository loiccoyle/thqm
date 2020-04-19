#!/usr/bin/env python
import argparse
import os
from pathlib import Path

from .server import start_server
from .settings import CONF_DIR, CONF_FILE, CONF_FILE_DEFAULT


def main():
    """Main logic.
    """
    CONF_DIR.mkdir(exist_ok=True)
    if not CONF_FILE.is_file():
        with open(CONF_FILE, 'w') as fp:
            fp.write(CONF_FILE_DEFAULT)

    parser = argparse.ArgumentParser(prog='thqm',
                                     description='Remote command and hotkey execution server.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config',
                        default=CONF_FILE,
                        help="Path to config file.")
    parser.add_argument("-p", "--port", type=int, default=8800,
                        help="Port number.")
    parser.add_argument('-q', '--qrcode', action='store_true',
                        default=False,
                        help='Show the qrcode.')
    parser.add_argument("-v", "--verbosity", action='count', default=0,
                        help=("Verbosity of the waitress server. "
                              "-v will print events. "
                              "-vv will print server messages."))
    args = parser.parse_args()

    if not Path(args.config).is_file():
        raise ValueError(f'File {args.config} does not exists.')

    start_server(args.config, port_number=args.port, qrcode=args.qrcode, verbosity=args.verbosity)

if __name__ == '__main__':
    main()

