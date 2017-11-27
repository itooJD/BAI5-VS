import json, requests

from .utils import paths, serializer as ser, outputs


def adventurers(auth_header, group_uri):
    # Adventurers
    adventurers_dict = {}
    adventurers = outputs.adventurers(requests.get(paths.adventurers, headers=auth_header))
    for i in range(len(adventurers)):
        adventurer = (adventurers[i]['user'], adventurers[i]['heroclass'])
        i = str(i + 1)
        adventurers_dict.update({i: adventurer})
        name = requests.get(paths.server_uri(adventurer[0]), headers=auth_header).json()['object']['name']
        adventurers_dict.update({i: name})
        print('<', i, '> ', end='')
        print(name, end='\t')
        print(adventurer[1])
    if group_uri != '':
        # invite player to group
        choice_invite = outputs.invite_ui()
        if choice_invite in adventurers_dict:
            try:
                if send_hiring_to_adventurer(auth_header, adventurers_dict[choice_invite], group_uri) == 200:
                    print('hired')
                else:
                    print('NO')
            except Exception:
                print('Can\'t create a connection!')


def group(auth_header, group_uri):
    # Group UI
    ids_groups = outputs.groups(requests.get(paths.groups, headers=auth_header))
    choice_group = outputs.group_ui(group_uri)
    if choice_group in ids_groups:
        group_uri_tmp = outputs.group(requests.get(paths.group(choice_group), headers=auth_header))
        if group_uri == '':
            if input('do you want to join(y/else): ') == 'y':
                response = requests.post(paths.group(choice_group) + '/members', headers=auth_header)
                print(response.json()['message'])
                if response.json()['message'] == 'Welcome to the group':
                    group_uri = group_uri_tmp
    elif choice_group == 'new' and group_uri == '':
        response = requests.post(paths.groups, headers=auth_header)
        group_uri = response.json()['object'][0]['_links']['self']
        response = requests.post(paths.server_uri(group_uri) + '/members', headers=auth_header)
        print(response.json())
    ser.serialize(group_uri, paths.group_link_file)


def send_message_to_adventurer(auth_header, name):
    message = json.dumps({"message": input('enter the message: ')})
    uri, adventurer_uris = adventurer(auth_header, name)
    messages_uri = uri + adventurer_uris['messages']
    response = requests.post(paths.http(messages_uri), data=message)
    try:
        print(response.json()['message'])
    except Exception:
        print('sent message!')


def send_assignment_to_adventurer(auth_header, name, task):
    uri, adventurer_uris = adventurer(auth_header, name)
    assignment_uri = uri + adventurer_uris['assignments']
    id = input('give the assignment an id: ')
    message = input('additional message: ')
    assignment_data = json.dumps({
        "id": id,
        "task": task['uri'],
        "resource": task['resource'],
        "method": "<GET/POST/...>",
        "data": "<data to use>",
        "callback": "initiator_url",
        "message": message
    })
    response = requests.post(paths.http(assignment_uri), data=assignment_data)
    try:
        print(response.json()['message'])
    except Exception:
        print('sent message!')


def send_hiring_to_adventurer(auth_header, name, group_uri):
    uri, adventurer_uris = adventurer(auth_header, name)
    hiring_uri = uri + adventurer_uris['hirings']
    message = input('additional message: ')
    hirings_data = json.dumps({
        "group": group_uri,
        "quest": "quest",
        "message": message
    })
    response = requests.post(paths.http(hiring_uri), data=hirings_data, timeout=50)


def adventurer(auth_header, name):
    adventurer = requests.get(paths.adventurer(name), headers=auth_header).json()['object']
    url = adventurer['url'][0:adventurer['url'].find('/')]
    return url, requests.get(paths.http(adventurer['url'])).json()
