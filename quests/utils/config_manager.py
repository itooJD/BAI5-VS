import yaml, ast
from socket import *
from pathlib import Path
from .paths_util import util_req
__location__ = Path().cwd()


def get_config():
    with (__location__ / 'quests' / 'utils' / 'paths.yaml').open('r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def write_config(paths):
    with (__location__ / 'quests' / 'utils' / 'paths.yaml').open('w') as stream:
        try:
            yaml.dump(paths, stream, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)


def change_config(path, data):
    config = get_config()
    if data == util_req:
        config[path].append(data)
    else:
        config[path] = data
    write_config(config)


def get_server_url():
    s=socket(AF_INET, SOCK_DGRAM)
    s.bind(('',24000))
    udp_received = s.recvfrom(1024 )
    port_pre = udp_received[0]
    address_pre  = udp_received[1]
    port = ast.literal_eval(port_pre.decode('utf-8'))['blackboard_port']
    address = address_pre[0]
    print('Config: Received {0} as address and {1} as port'.format(address, port))
    return address, port


def set_server_url_via_udp():
    print('Config: Setting server_url')
    paths = get_config()
    server, port =  get_server_url()
    server_url = 'http://{0}:{1}'.format(server, port)
    paths['server'] =  server_url
    write_config(paths)
    return paths