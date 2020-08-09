#!/usr/bin/env python3
import yaml

from utils import validate_file_path


# Breaks yml file?
def set_bungee_mode(file_path: str):
    with open(file_path, 'r') as cfg:
        spig_yml = yaml.safe_load(cfg)
        # except yaml.YAMLError as exc:

    spig_yml['ip_forward'] = True

    with open(file_path, 'w') as cfg:
        yaml.dump(spig_yml, cfg)


if __name__ == '__main__':
    path = validate_file_path('config.yml')
    set_bungee_mode(path)
