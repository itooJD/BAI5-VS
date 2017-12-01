import requests

from quests.utils import outputs, get_config


def users(auth_header):
    outputs.users(requests.get(get_config()['users_url'], headers=auth_header))
