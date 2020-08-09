import argparse
import yaml


def argparse_setup():
    # type: () -> (argparse.ArgumentParser, argparse.ArgumentParser)
    parser = argparse.ArgumentParser(description='Bungee Manager')

    parser.add_argument('name', help='Name you want to call the VPS')
    parser.add_argument('config_definition_path',
                        help='Path to the config set up in digitalocean_config.yml.'
                        'Check digitalocean_config.yml.example for examples')

    parser.add_argument('-s', '--sleep-time', type=int,
                        help="Amount of time between creating the droplet "
                             "and uploading the files "
                             "(Allows the droplet to start up)",
                             default=60)
    parser.add_argument('-b', '--bungee_name', type=str,
                        help="Name of the bungee connection as set up in "
                             "bungee_info.yml ")

    parser.add_argument('-t', '--token',
                        help="For commands that may only need a token. Unused")
    parser.add_argument('-y', '--yes', action='store_true',
                        help="Skips all checks in case of missing arguments")

    args, unknown = parser.parse_known_args()

    wild_parser = argparse.ArgumentParser(description='Bungee Manager/Placeholder arg viewer')
    for arg in unknown:
        if arg.startswith(("-", "--")):
            wild_parser.add_argument(arg)

    wild_args = wild_parser.parse_args(unknown)

    return args, wild_args


def missing(_arg, force=False):
    # type: (str, bool) -> None
    message = f"You are missing the argument {_arg}."
    if force:
        print(f"{message} This argument is required for this operation."
              " Use help for more info.")
        exit(1)

    consent = ''
    while consent.lower() not in ('y', 'yes'):
        consent = input(
            f"{message} Do you want to continue without setting it?\n(yes/no)")
        if consent.lower() in ('n', 'no'):
            exit(0)


def get_do_config():
    # type: ()  -> dict
    with open('digitalocean_config.yml', 'r') as cfg:
        config = yaml.safe_load(cfg) or {}
    return config


def update_do_config(new_cfg):
    # type: (dict) -> None
    with open('digitalocean_config.yml', 'w') as cfg:
        yaml.dump(new_cfg, cfg)


def get_upload_files_for(name):
    # type: (str) -> list
    config = get_do_config()
    server_config = config.get(name) or {}
    setup = server_config.get('setup') or {}
    upload_list = setup.get('uploads') or []

    return upload_list


def get_commands_to_run_for(name):
    # type: (str) -> list
    config = get_do_config()

    server_config = config.get(name) or {}
    setup = server_config.get('setup') or {}
    command_list = setup.get('pre_commands') or []

    return command_list


def get_script_to_run_for(name):
    # type: (str) -> str
    config = get_do_config()

    server_config = config.get(name) or {}
    setup = server_config.get('setup') or {}
    script = setup.get('script') or ""

    return script
