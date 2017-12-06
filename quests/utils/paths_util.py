from .config_manager import get_config


def http(uri):
    return 'http://' + uri


def make_http(url):
    if not url.startswith('http://'):
        new_url = 'http://' + url
    else:
        new_url = url

    if new_url[-1] == '/':
        http_url = new_url[:-1]
    else:
        http_url = new_url
    return http_url


def port_check(url):
    if url.endswith(':5000') or url.endswith(':5000/'):
        return url
    else:
        return url + ':5000'


def server_uri(uri):
    return get_config()['server'] + uri


def quest_uri():
    return server_uri(get_config()['blackboard_url'] + get_config()['quest_url'])


def users_uri():
    return server_uri(get_config()['user_url'])


def group_url_id(id):
    return group_url() + '/' + id


def group_url():
    return server_uri(get_config()['taverna_url'] + get_config()['group_url'])


def adventurers_uri():
    return server_uri(get_config()['taverna_url'] + get_config()['adventurers_url'])


def adventurer_uri_name(name):
    return adventurers_uri() + '/' + name