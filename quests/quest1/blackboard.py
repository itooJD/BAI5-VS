import requests
from quests.quest1.ui import divide_line, quest_ui
from quests.utils import paths_util, get_config, change_config
from quests.utils.paths_util import current_quest
from quests.quest1.questing import solve_quests


def choose_quest(auth_header):
    divide_line()
    quest_no, quest = quest_ui(auth_header)
    print(quest)
    quest_infos(requests.get(paths_util.server_uri(quest['uri']), headers=auth_header))
    change_config(current_quest, quest)
    return quest_starter(quest, quest_no, auth_header)


def quest_starter(quest, quest_no, auth_header):
    start = input('Should we go on a journey to solve this quest or go back to the main menu? [y/n]\n> ')
    if start == 'y':
        return solve_quests(quest, quest_no, auth_header)
    else:
        return ''


def show_available_quests(auth_header):
    response = requests.get(paths_util.quest_uri(), headers=auth_header)
    quest = {}
    quests = []
    available_quests = []
    print('Quest: Available quests: \n')
    for idx, quest in enumerate(response['objects']):
        divide_line()
        requirements_fullfilled = True
        if quest['requirements']:
            for req in quest['requirements']:
                if req not in get_config()['requirements']:
                    requirements_fullfilled = False
                    break
        if requirements_fullfilled:
            available_quests.append(idx)
            quests.append(quest)
            print('Quest with index: ' + str(idx))
            print_quest(quest)
        print()
    quest_no = -1
    divide_line()
    print('Available quests: ' + str(available_quests))
    while int(quest_no) not in available_quests:
        quest_no = input('Which quest do you want to tackle mighty Heroy? \n You can also go back to the main menu with [n] \n> ')
        if quest_no == 'n':
            quest_no = False
    if quest_no:
        quest = quests[int(quest_no)]
    return quest_no, quest


def show_all_quests(auth_header):
    response = requests.get(paths_util.quest_uri(), headers=auth_header)
    quest = {}
    available_quests = []
    for idx, quest in enumerate(response['objects']):
        divide_line()
        print_quest(quest)
    print('Available quests: ' + str(available_quests))
    quest_no = -1
    while int(quest_no) not in available_quests:
        quest_no = input('Which quest do you want to tackle mighty Heroy? \n You can also go back to the main menu with [n] \n> ')
        if quest_no == 'n':
            quest_no = False
    if quest_no:
        quest = available_quests[int(quest_no)]
    return quest_no, quest


def print_quest(quest):
    print('Name:        ' + quest['name'])
    print('Description: ' + quest['description'])
    print('URI:         ' + quest['_links']['self'])
    print('Tasks:       ' + quest['tasks'])
    print('Deliveries:  ' + quest['_links']['deliveries'])


def show_users(auth_header):
    response = requests.get(paths_util.users_uri(), headers=auth_header)
    print('\nAll Users')
    for user in response.json()['objects']:
        print(user['name'], end=', ')
    return ''


def look_at_map(auth_header):
    print()
    print('Quest: Lets look this up on the map')
    map_resp = requests.get(get_config()['server'] + get_config()['map_url'], headers=auth_header)
    print()
    print('Map: The map: \n' + str(map_resp.json()))
    print()
    return ''


def quest_infos(response):
    print('\nQuest')
    object = response.json()['object']
    print(object['name'])
    print(object['description'])