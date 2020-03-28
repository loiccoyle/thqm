#!/usr/bin/env python
import argparse
import os
from pathlib import Path

from .server import start_server
from .settings import CONF_DIR, CONF_FILE, CONF_FILE_HEADER


def main():
    """Main logic.
    """
    CONF_DIR.mkdir(exist_ok=True)
    if not CONF_FILE.is_file():
        with open(CONF_FILE, 'w') as fp:
            fp.write(CONF_FILE_HEADER)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        default=CONF_FILE,
                        help="Path to config file.")
    parser.add_argument("-p", "--port", type=int, default=8800,
                        help="Port number.")
    parser.add_argument('-q', '--qrcode', action='store_true',
                        default=False,
                        help='Show the qrcode.')
    parser.add_argument("-v", "--verbose", action='count', default=1,
                        help="Verbosity or the server. -v shows the print the keypresses. -vv show the server output.")
    args = parser.parse_args()

    if not Path(args.config).is_file():
        raise ValueError(f'File {args.config} does not exists.')

    start_server(args.config, port_number=args.port, qrcode=args.qrcode, verbosity=args.verbose)

if __name__ == '__main__':
    main()
