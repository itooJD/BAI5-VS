import requests

from questing_resources import taverna
from utils import paths, serializer as ser


def group(auth_header, group_uri, user_name, quest):
    in_group = True
    while in_group:
        obj = requests.get(paths.server_uri(group_uri), headers=auth_header).json()['object']
        print('\nGroup: ', obj['id'], '\t', obj['owner'])
        print('Members')
        members = dict()
        i = 1
        for member in obj['members']:
            members.update({str(i): member})
            print(i, ' ', member)
            i = i + 1
        print('\n1: leave the group')
        print('2: send a message')
        if bool(quest):
            print('3: send a assignment')
        print('else to go back')
        choice_group = input('what do you want to do: ')
        try:
            if choice_group == '1':
                if user_name == obj['owner']:
                    print(requests.delete(paths.server_uri(group_uri), headers=auth_header).json()['message'])
                else:
                    requests.delete(paths.adventurer(user_name), headers=auth_header)
                    print('You left the Group')
                group_uri = ''
                ser.serialize(group_uri, paths.group_link_file)
            elif choice_group == '2':
                choice_member = input('whom do you want to send the message to: ')
                if choice_member in members:
                    taverna.send_message_to_adventurer(auth_header, members[choice_member])
            elif choice_group == '3':
                choice_member = input('whom do you want to send the assignment to: ')
                for keys, values in quest['tasks'].items():
                    print(keys, ': ', values['name'])
                choice_task = input('which task to assign: ')
                if choice_member in members and choice_task in quest['tasks']:
                    taverna.send_assignment_to_adventurer(auth_header, members[choice_member],
                                                          quest['tasks'][choice_task])
            else:
                in_group = False
        except Exception:
            print('couldn\'t send')
