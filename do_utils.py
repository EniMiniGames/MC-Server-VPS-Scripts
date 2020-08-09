import time

import yaml
import digitalocean


def get_manager(token=None):
    # type: (str) -> digitalocean.Manager

    # Load manager from
    manager = digitalocean.Manager(token=token)
    return manager


def get_droplet_info(drop):
    # type: (Droplet) -> dict
    info = dict(
        id=drop.id, name=drop.name, tags=drop.tags, status=drop.status,
        created_at=drop.created_at, disk=drop.disk, memory=drop.memory,
        monitoring=drop.monitoring, user_data=drop.user_data,
        ssh_keys=drop.ssh_keys, vcpus=drop.vcpus, volumes=drop.volumes,
        ip_address=drop.ip_address, ip_v6_address=drop.ip_v6_address, drop=drop
    )

    return info


# TODO decorator for (config_file=None, token=None) args?
def get_all_droplets(config_file=None, token=None):
    # type: (str, str) -> dict
    # Get token from config file if not given
    if not token:
        import yaml
        with open(config_file, 'r') as cfg:
            config = yaml.safe_load(cfg.read())
        token = config.get('api_info').get('token')

    manager = get_manager(token)
    my_droplets = manager.get_all_droplets()

    drops = dict()

    # Get droplet info
    for i in my_droplets:
        drops[i.id] = get_droplet_info(i)

    return drops


def create_new_droplet(name, def_path, attempts=1):
    # type: (str, str, int) -> dict
    # Get droplet info from config
    with open('digitalocean_config.yml', 'r') as cfg:
        config = yaml.safe_load(cfg.read())

    api_info = config.get('api_info')
    token = api_info.get('token')
    keys = api_info.get('key_name')

    droplet_config = config.get(def_path)

    droplet_name = f"{droplet_config.get('droplet_prefix')}---{name}"
    droplet_name = droplet_name.replace(" ", "")

    droplet_regions = droplet_config.get('droplet_regions')  # attempts+ ?
    droplet_image = droplet_config.get('droplet_image')
    droplet_size_slug = droplet_config.get('droplet_size_slug')
    droplet_tags = droplet_config.get('droplet_tags')  # list

    if droplet_config.get('droplet_custom_image_id'):
        droplet_image = droplet_config.get('custom_image_id')

    manager = get_manager(token)
    all_keys = manager.get_all_sshkeys()
    droplet_keys = [k.id for k in all_keys if k.name == keys]  # k.name in keys

    # Create droplet
    droplet = digitalocean.Droplet(
        token=manager.token,
        name=droplet_name,
        region=droplet_regions,
        image=droplet_image,
        size_slug=droplet_size_slug,
        backups=False,
        monitoring=True,
        ssh_keys=droplet_keys,
        tags=[droplet_tags]
    )

    droplet.create()
    return get_all_droplets('digitalocean_config.yml')[droplet.id]


def spin_up_new_server(name, def_path, sleep_time=60):
    # type: (str, str, int) -> dict
    sleep_time = int(sleep_time)
    new_drop = create_new_droplet(name, def_path)

    print(f"Droplet up, allowing it to load for {sleep_time}s...")
    # TODO errors when droplet deleted
    time.sleep(sleep_time)

    drop = get_all_droplets('digitalocean_config.yml')[new_drop['id']]

    print(drop)  # optional ?

    return drop
