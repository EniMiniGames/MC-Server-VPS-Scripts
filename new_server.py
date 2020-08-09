#!/usr/bin/env python3
import yaml

from utils import argparse_setup, missing
from new_bungee import find_bungee_name
from do_utils import spin_up_new_server
from ssh_utils import finalize_server_setup


def find_server_name(name, bungee_name):
    # type: (str, str) -> bool
    with open('bungee_info.yml', 'r') as bgf:
        cfg = yaml.safe_load(bgf) or {}
        if not cfg.get(bungee_name):
            return False

    servers = cfg.get(bungee_name).get('servers', {})
    if name not in servers:
        return False

    return True


def get_bungee_info(name):
    # type: (str) -> dict
    with open('bungee_info.yml', 'r') as bgf:
        cfg = yaml.safe_load(bgf) or {}

    bg_info = cfg.get(name) or {}
    return bg_info


def add_server_to_bungee_config(bungee_name, server_name, server_ip, server_port=0000):
    # type: (str, str, str, int) -> None
    with open('bungee_info.yml', 'r') as bgf:
        cfg = yaml.safe_load(bgf) or {}

    server_info = dict(ip=server_ip, port=server_port)
    cfg[bungee_name]['servers'][server_name] = server_info

    with open('bungee_info.yml', 'w') as bgf:
        yaml.safe_dump(cfg, bgf)


if __name__ == "__main__":
    args, wildcards = argparse_setup()

    placeholders = vars(wildcards)

    if not args.bungee_name:
        missing("--bungee_name", force=True)

    if not find_bungee_name(args.bungee_name):
        print(f"No bungee config by the name {args.bungee_name} was found! "
              "Choose a different name or create one with new_bungee.py.")
        exit(1)
    if find_server_name(args.name, args.bungee_name):
        print(f"A server by name {args.name} already exists under {args.bungee_name}!")
        print("Choose a different name")
        exit(1)

    new_server = spin_up_new_server(args.name, args.config_definition_path,
                                    sleep_time=args.sleep_time)

    # TODO add port to args, required
    add_server_to_bungee_config(args.bungee_name, args.name, new_server.get('ip_address'))
    bungee_info = get_bungee_info(args.bungee_name)

    finalize_server_setup(args.config_definition_path, new_server.get('ip_address'), **placeholders)
