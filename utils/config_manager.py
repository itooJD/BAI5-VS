import yaml
from socket import *
from pathlib import Path
__location__ = Path().cwd()


def get_config():
    with (__location__ / 'utils' / 'paths.yaml').open('r') as stream:
        try:
            print('Config: Getting config data')
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def write_config(paths):
    with (__location__ / 'utils' / 'paths.yaml').open('w') as stream:
        try:
            print('Config: Writing config data')
            yaml.dump(paths, stream, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)


def get_server_url():
    s=socket(AF_INET, SOCK_DGRAM)
    s.bind(('',24000))
    udp_received = s.recvfrom(1024 )
    port_pre = udp_received[0]
    address_pre  = udp_received[1]
    port = port_pre.encode('utf-8')
    address = address_pre[0]
    print('Config: Received {0} as address and {1} as port'.format(address, port))
    return address


def set_server_url_via_udp():
    print('Config: Setting server_url')
    paths = get_config()
    server, port =  get_server_url()
    server_url = 'http://{0}:{1}'.format(server, port)
    paths['server'] =  server_url
    write_config(paths)
    return paths