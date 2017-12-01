import requests
from quests.utils import paths_util, get_config, change_config
from quests.utils.paths_util import current_quest


def quests(auth_header, actual_quest):
    choice_quest, quests = quests_infos(requests.get(get_config()['quests'], headers=auth_header))
    if choice_quest in quests:
        quest = quests[choice_quest]
        # Quest Info
        quest_infos(requests.get(paths_util.server_uri(quest['uri']), headers=auth_header))
        tasks = dict()
        for i in range(len(quest['tasks'])):
            tasks.update(
                {str(i + 1): task_infos(requests.get(paths_util.server_uri(quest['tasks'][i]), headers=auth_header))})
        quest['tasks'] = tasks
        if not bool(actual_quest):
            if input('do you want to accept the quest (y/else): ') == 'y':
                change_config(current_quest, quest)
                return quest
        return actual_quest


# out: choice_quest, ids
def quests_infos(response):
    print('\nQuests')
    quests = {}
    objects = response.json()['objects']
    i = 1
    for obj in objects:
        quest = {
            'name': obj['name'],
            'uri': obj['_links']['self'],
            'tasks': obj['tasks'],
            'deliveries': obj['_links']['deliveries'],
            'id': 'no',
            'callback': 'no',
        }
        quests.update({str(i): quest})
        print('< id=', i, '>', end='')
        print(quest['name'])
        i = i + 1
    print('else to back')
    return input('more infos to: '), quests


def quest_infos(response):
    print('\nQuest')
    object = response.json()['object']
    print(object['name'])
    print(object['description'])


# OUT: task = (required_players, location_uri)
def task_infos(response):
    print('\nTask')
    obj = response.json()['object']
    task = {
        'name': obj['name'],
        'uri': obj['_links']['self'],
        'location': obj['location'],
        'resource': obj['resource'],
        'required_players': obj['required_players'],
        'data': 'no',
        'method': 'no'
    }
    print(obj['name'])
    print(obj['description'])
    print('required players: ', obj['required_players'])
    return task
