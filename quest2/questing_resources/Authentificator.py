import os, requests
from utils import paths, serializer as ser, outputs


class Authentificator():
    def authentification(self, auth_header):
        ## Authentification UI
        sleep = False
        choice = outputs.authentication_ui()
        if choice in ['1', '2']:
            username = input('Username: ')
            password = input('Password: ')
            if choice == '1':
                user_data = '{"name":"' + username + '","password":"' + password + '"}'
                response = requests.post(paths.users, data=user_data)
                print(response.json()['message'])
            response = requests.get(paths.login, auth=(username, password))
            if response.status_code == 200:
                print(response.json()['message'])
                auth_token = response.json()['token']
                auth_header = {'Authorization': 'Token ' + auth_token}
                ser.serialize(auth_token, paths.auth_token_file)
        else:
            sleep = True
        return sleep, auth_header


    def logout(self):
        os.remove(paths.auth_token_file)
        return {}