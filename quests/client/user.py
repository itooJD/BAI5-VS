import requests
from quests.client.utilities import divide_line
from quests.utils import paths_util, change_config, get_config
from quests.utils.paths_names import auth_token as token, util_user


def authentication_ui():
    print('1: Register')
    print('2: Login')
    print('Else: Exit')
    return input('> ')


def authentication():
    exit = False
    auth_header = ''

    choice = authentication_ui()
    if choice in ['1', '2']:
        username = input('Username \n> ')
        password = input('Password \n> ')
        if choice == '1':
            user_data = '{"name":"' + username + '","password":"' + password + '"}'
            response = requests.post(paths_util.server_uri(get_config()['user_url']), data=user_data)
            print()
            print(response.json()['message'])
            change_config(util_user, username)
        else:
            change_config(util_user, username)
        response = requests.get(paths_util.server_uri(get_config()['login_url']), auth=(username, password))
        if response.status_code == 200:
            print(response.json()['message'])
            auth_token = response.json()['token']
            auth_header = {'Authorization': 'Token ' + auth_token}
            change_config(token, auth_header)
    else:
        exit = True
    return exit, auth_header


def whoami(auth_header):
    divide_line()
    whoami_resp = requests.get(get_config()['server'] + get_config()['whoami_url'], headers=auth_header)
    if whoami_resp.json().get('user'):
        show = input('Show user info? [y/n] \n> ')
        if show == 'y' or show == 'yes':
            print('## WhoAmI ##\n' +
              'Name: ' + str(whoami_resp.json()['user']['name']) + '\n' +
              'Finished deliverables: ' + str(whoami_resp.json()['user']['deliverables_done']) + '\n' +
              'Delivered: ' + str(whoami_resp.json()['user']['delivered']))
            print(whoami_resp.json().get('message'))
            divide_line()
        else:
            print('Not showing user info')
        return True
    else:
        print('!!! You could not be authenticated. Please try again !!!')
        divide_line()
        return False