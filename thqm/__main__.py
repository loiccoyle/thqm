#!/usr/bin/env python
import argparse
import os
from pathlib import Path

from .server import start_server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        default=Path(os.environ.get("XDG_CONFIG_HOME")) / 'thqm' / 'config',
                        help="Path to config file.")
    parser.add_argument("-p", "--port", type=int, default=8800,
                        help="Port number.")
    parser.add_argument("-q", "--quiet", action='store_true',
                        help="Don't show qr code.")
    args = parser.parse_args()

    if not args.config.is_file():
        raise ValueError(f'file {args.config} does not exists.')

    start_server(args.config, port_number=args.port, print_qr=not args.quiet)

if __name__ == '__main__':
    main()
