import yaml
import paramiko

from utils import (
    get_commands_to_run_for,
    get_upload_files_for,
    get_script_to_run_for
)
from sftp_utils import put_home_files


def run_command(session, cmd, nbytes=4096):
    # type: (paramiko.Channel, str, int) -> (list, list)
    stdout_data = []
    stderr_data = []

    session.exec_command(cmd)

    # print('exit status: ', session.recv_exit_status())
    while True:
        if session.recv_ready():
            stdout_data.append(session.recv(nbytes))
        if session.recv_stderr_ready():
            stderr_data.append(session.recv_stderr(nbytes))
        if session.exit_status_ready():
            break

    return stdout_data, stderr_data


def connect(username, hostname, port=22):
    # type: (str, str, int) -> paramiko.Transport
    # TODO password?
    with open('digitalocean_config.yml', 'r') as cfg:
        config = yaml.safe_load(cfg.read())

    key_filename = f"keys/{config.get('api_info').get('key_name')}"

    # Get private key and connect to Transport
    priv_key = paramiko.RSAKey(
        filename=key_filename)  # Non PPK

    # noinspection PyTypeChecker
    transp = paramiko.Transport((hostname, port))
    transp.connect(username=username, pkey=priv_key)

    return transp


def finalize_server_setup(config_definition_path, ssh_ip_address, **kwargs):
    # type: (str, str, dict) -> None
    transport = connect('root', ssh_ip_address)  # rename transport

    replacements = list(kwargs.keys())
    commands = get_commands_to_run_for(config_definition_path)
    reserved = locals()

    # Replace placeholders with actual values

    script = get_script_to_run_for(config_definition_path)
    uploads = get_upload_files_for(config_definition_path)

    if replacements:
        for cmd in commands:
            for rpl in replacements:
                if rpl not in reserved:  # TODO Note in docs
                    cmd = cmd.replace(f"{{{rpl}}}", kwargs.get(rpl, ""))

        for rpl in replacements:
            if rpl not in reserved:
                script = script.replace(f"{{{rpl}}}", kwargs.get(rpl, ""))

    put_home_files(transport, uploads)

    transport.set_keepalive(60)
    session = transport.open_channel(kind='session')

    one_liner = "; ".join(commands) if commands else ""
    print(one_liner)
    if one_liner:
        print("Running Pre Commands...")
        stdout_data, stderr_data = run_command(session, one_liner)
        print(''.join([i.decode('utf8') for i in stdout_data]))
        print(''.join([i.decode('utf8') for i in stderr_data]))

    session = transport.open_channel(kind='session')
    print(script)
    if script:
        print("Running Setup Script...")
        stdout_data, stderr_data = run_command(session, script)
        print(''.join([i.decode('utf8') for i in stdout_data]))
        print(''.join([i.decode('utf8') for i in stderr_data]))

    if transport:
        transport.close()
