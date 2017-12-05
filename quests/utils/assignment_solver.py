import requests
from flask import json, abort

from quests.quest1.taverna.groups import start_election
from quests.quest1.utilities import divide_line
from quests.utils import paths_util, get_config, change_config
from quests.utils.paths_names import auth_token, util_assignments, util_group


def solve_assignment(json_data, sender_uri):
    change_config(util_assignments, json_data)

    divide_line()
    print('Received assignment: \n' + str(json_data['message']) + '\n' + str(
        json_data['method']) + '\n' + str(json_data['resource']))
    print()
    url = paths_util.make_http(json_data['resource'])
    if json_data['method'].lower() == 'get':
        response = requests.get(url, headers=get_config()[auth_token], data=json_data['data'])
    elif json_data['method'].lower() == 'post':
        response = requests.post(url, headers=get_config()[auth_token], data=json_data['data'])
    else:
        return False

    if response.status_code == 200:
        print(response.json()['message'])
        print()
        print(response.json())
        if response.json().get('hint'):
            print(response.json()['hint'])
            divide_line()
            print('Starting new election')
            new_assignment = json_data
            new_assignment['job'] = {
                "id": json_data['id'],
                "task": json_data['task'],
                "resource": json_data['resource'],
                "method": json_data['method'],
                "data": str(json.dumps({
                    "group": get_config()[util_group],
                    "token": response.json()['token']
                })),
                "callback": json_data['callback'],
                "message" : "Oh no, i am unconcious, take over please!"
            }
            start_election(election_data=new_assignment)

        answer = json.dumps({
            'id': json_data['id'],
            'task': json_data['task'],
            'resource': json_data['resource'],
            'method': json_data['method'],
            'data': response.json(),
            'user': get_config()['username'],
            'message': 'Swifty swooty as ever has Heroy done his job.'
        })

        requests.post(paths_util.make_http(sender_uri + json_data['callback']), data=answer)
        callback_address = paths_util.make_http(sender_uri + json_data['callback'])
        print('That went well, answering to Callback! ' + str(callback_address))
        try:
            callback_resp = requests.post(callback_address, data=answer)
            if callback_resp.status_code == 200 or callback_resp.status_code == 201:
                divide_line()
                print('Callback sent successfully')
            else:
                print('Could not reach callback url')
                divide_line()
        except Exception as cre:
            print('Could not reach callback, Connection Refused!')
            print(cre)
    else:
        divide_line()
        return False