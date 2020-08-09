#!/usr/bin/env python3
import yaml

from utils import argparse_setup
from do_utils import spin_up_new_server
from ssh_utils import finalize_server_setup


def find_bungee_name(name):
    # type: (str) -> bool
    with open('bungee_info.yml', 'r') as bgf:
        cfg = yaml.safe_load(bgf) or {}
        if cfg.get(name):
            return True

    return False


def add_to_bungee_config(name, server_info):
    # type: (str, dict) -> None
    with open('bungee_info.yml', 'r') as bgf:
        cfg = yaml.safe_load(bgf) or {}

    cfg[name] = {}
    cfg[name]['servers'] = {}
    cfg[name]['ip'] = server_info.get('ip_address')

    with open('bungee_info.yml', 'w') as bgf:
        yaml.safe_dump(cfg, bgf)


if __name__ == "__main__":
    args, wildcards = argparse_setup()

    placeholders = vars(wildcards)

    if find_bungee_name(args.name):
        print(f"{args.name} already exists in bungee_info.yml! "
              "Choose a different name.")
        exit(1)

    new_server = spin_up_new_server(args.name, args.config_definition_path,
                                    sleep_time=args.sleep_time)
    add_to_bungee_config(args.name, new_server)

    finalize_server_setup(args.config_definition_path, new_server.get('ip_address'), **placeholders)

    print("Done! Exiting...")
