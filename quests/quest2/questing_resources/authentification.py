import requests
from quests.utils import outputs, get_config, change_config
from quests.utils.paths_util import auth_token as token


def authentification(auth_header):
    ## Authentification UI
    sleep = False
    choice = outputs.authentication_ui()
    if choice in ['1', '2']:
        username = input('Username: ')
        password = input('Password: ')
        if choice == '1':
            user_data = '{"name":"' + username + '","password":"' + password + '"}'
            response = requests.post(get_config()['users'], data=user_data)
            print(response.json()['message'])
        response = requests.get(get_config()['login_url'], auth=(username, password))
        if response.status_code == 200:
            print(response.json()['message'])
            auth_token = response.json()['token']
            auth_header = {'Authorization': 'Token ' + auth_token}
            change_config(token, auth_token)
    else:
        sleep = True
    return sleep, auth_header


def logout():
    change_config(token, '')
    return {}
