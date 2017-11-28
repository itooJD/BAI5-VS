from .config_manager import get_config

def http(uri):
    return 'http://' + uri


def server_uri(uri):
    return get_config()['server'] + uri


def group(id):
    return get_config()['group_url'] + '/' + id


def adventurer(name):
    return get_config()['adventurers_url'] + '/' + name

current_quest = 'current_quest'
auth_token = 'auth_token'
util_tokens = 'util_tokens'
util_group = 'group_uri'