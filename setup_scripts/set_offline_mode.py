#!/usr/bin/env python3
from io import StringIO
import configparser

from utils import validate_file_path


def set_offline_mode(file_path: str, localhost=False):
    placeholder = '[placeholder]\n'
    with open(file_path, 'r') as cfg:
        config_string = placeholder + cfg.read()  # dummy section needed bc Congigparser is dum

    config = configparser.ConfigParser()
    config.read_string(config_string)

    config['placeholder']['online-mode'] = 'false'
    if localhost:
        config['placeholder']['server-ip'] = "127.0.0.1"

    # Write contents to mock IO
    with StringIO("") as sIO:  # Trick into giving us config as string
        config.write(sIO, space_around_delimiters=False)
        sIO.seek(0)
        new_config_str = sIO.read()

    new_config_str = new_config_str[len(placeholder):]  # Remove placeholder

    with open(file_path, 'w') as cfg:
        cfg.write(new_config_str)


if __name__ == '__main__':
    import sys
    args = sys.argv
    localhost = False

    if len(args) >= 3 and str(args[2]).lower() == 'localhost':
        localhost = True

    path = validate_file_path('server.properties')
    set_offline_mode(path, localhost)
