import requests
from quests.quest1.utilities import divide_line
from quests.utils import paths_util, get_config, change_config
from quests.utils.paths_util import current_quest
from quests.quest1.questing import solve_quests


def quest_ui(auth_header):
    print('1: The ones I fulfill the requirements of')
    print('2: All')
    print('Else: Exit')
    return quest_filter(input('> '), auth_header)


def quest_filter(choice, auth_header):
    choice_filter = {
        '1': show_available_quests,
        '2': show_all_quests
    }
    return choice_filter.get(choice)(auth_header)


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
    print('URI:         ' + str(quest['_links']['self']))
    print('Tasks:       ' + str(quest['tasks']))
    print('Deliveries:  ' + str(quest['_links']['deliveries']))


def show_users(auth_header):
    response = requests.get(paths_util.users_uri(), headers=auth_header)
    print('\nWhata bunch of people there are in here. How do we get through these hords?')
    divide_line()
    for user in response.json()['objects']:
        if user.get('name'):
            try:
                print(user['name'], end=', ')
            except UnicodeEncodeError:
                pass
    print()
    return ''


def look_at_map(auth_header):
    print()
    print('Lets look at our map')
    map_resp = requests.get(get_config()['server'] + get_config()['map_url'], headers=auth_header)
    print()
    if map_resp.json()['status'] == 'success':
        print('Map: \n')
        for location in map_resp.json().get('objects'):
            print('Name:     ' + location['name'])
            print('Host:     ' + location['host'])
            print('Tasks:    ' + str(location['tasks']))
            print('Visitors: ' + str(location['visitors']))
            divide_line()
    print()
    return ''


def quest_infos(response):
    print('\nQuest')
    object = response.json()['object']
    print(object['name'])
    print(object['description'])