import requests

from questing_resources import blackboard as bb
from utils import paths


def my_quest(auth_header, tokens_id, tokens, quest):
    bb.quest_infos(requests.get(paths.server_uri(quest['uri']), headers=auth_header))
    for key, task in quest['tasks'].items():
        bb.task_infos(requests.get(paths.server_uri(task['uri']), headers=auth_header))
        print('1: deliver')
        print('2: abandon')
        choice_quest = input('what do you want to do: ')
        if choice_quest == '1':
            deliveries_uri = quest['deliveries']
            tasks = quest['tasks']
            for id, value in tasks.items():
                print(id, value['name'])
            choice_task = input('which task do you want to deliver: ')
            if choice_task in tasks:
                task_uri = tasks[choice_task]['uri']
                print('\nTokens to deliver')
                for key, values in tokens_id.items():
                    print(key, ': ', values)
                choice_token = input('which token to deliver: ')
                if choice_token in tokens_id:
                    token = '{"' + task_uri + '":' + tokens[tokens_id[choice_token]] + '}'
                    data = '{"tokens":' + token + '}'
                    response = requests.post(paths.server_uri(deliveries_uri), headers=auth_header, data=data)
                    print(response.json())
            return quest
        elif choice_quest == '2':
            return {}
        else:
            return quest
