import requests

from .questing_resources import blackboard as bb
from .questing_resources import users, game_map, taverna, group
from .questing_resources.authentification import authentification as auth, logout
from .questing_resources.quest import my_quest
from ..utils import paths_util, serializer as ser, outputs


try:
    auth_token = ser.de_serialize(paths_util.auth_token_file)
    auth_header = {'Authorization': 'Token ' + auth_token}
except Exception:
    auth_header = {}

try:
    group_uri = ser.de_serialize(paths_util.group_link_file)
except Exception:
    group_uri = ''

try:
    quest = ser.de_serialize(paths_util.quest_file)
except Exception:
    quest = {}

try:
    tokens_id, tokens = ser.de_serialize(paths_util.tokens_file)
except Exception:
    tokens_id = {}
    tokens = {}

print(tokens)
sleep = False
while not sleep:
    if not bool(auth_header):
        ## Authetification UI
        sleep, auth_header = auth(auth_header)
    else:
        # My Infos
        user_name = outputs.my_infos(requests.get(paths_util.whoami, headers=auth_header))
        # MAIN UI
        choice_main = outputs.main_ui(quest, group_uri)
        if choice_main == '1':
            # Quests
            quest = bb.quests(auth_header, quest)
        elif choice_main == '2':
            # Entering the Taverna
            adventurer_data = '{"heroclass":"juggernaut","capabilities":"None","url":"172.19.0.68:5000/heroyjenkins"}'
            requests.post(paths_util.adventurers, headers=auth_header, data=adventurer_data)
            print('\nEntering the Taverna')
            in_taverna = True
            while in_taverna:
                # Taverna UI
                choice_taverna = outputs.taverna_ui()
                if choice_taverna == '1':
                    taverna.adventurers(auth_header, group_uri)
                elif choice_taverna == '2':
                    # Group UI
                    ids_groups = outputs.groups(requests.get(paths_util.groups, headers=auth_header))
                    choice_group = outputs.group_ui(group_uri)
                    if choice_group in ids_groups:
                        group_uri_tmp = outputs.group(requests.get(paths_util.group(choice_group), headers=auth_header))
                        if group_uri == '':
                            if input('do you want to join(y/else): ') == 'y':
                                response = requests.post(paths_util.group(choice_group) + '/members', headers=auth_header)
                                print(response.json()['message'])
                                if response.json()['message'] == 'Welcome to the group':
                                    group_uri = group_uri_tmp
                    elif choice_group == 'new' and group_uri == '':
                        response = requests.post(paths_util.groups, headers=auth_header)
                        group_uri = response.json()['object'][0]['_links']['self']
                        response = requests.post(paths_util.server_uri(group_uri) + '/members', headers=auth_header)
                        print(response.json())
                    ser.serialize(group_uri, paths_util.group_link_file)
                else:
                    # Leaving the Taverna
                    print('Leaving the Taverna')
                    in_taverna = False
        elif choice_main == '3':
            # Users
            users(auth_header)
        elif choice_main == '4':
            # Map
            tokens_id, tokens = game_map(auth_header, quest, tokens_id, tokens)
        elif choice_main == '5':
            # Logout
            auth_header = logout()
        elif choice_main == '6' and bool(quest):
            # Quest
            quest = my_quest(auth_header, tokens_id, tokens, quest)
        elif choice_main == '7' and group_uri != '':  # Group
            group(auth_header, group_uri, user_name, quest)
        else:
            sleep = True
