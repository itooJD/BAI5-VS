import requests
from quests.utils import paths_util, get_config
from quests.utils.paths_names import util_req
from quests.quest1.utilities import divide_line
from .groups import group_ui
from .adventurers import adventurer_ui


def taverna(auth_header):
    # Entering the Taverna
    divide_line()
    print('So you are a juggernaut huh? And I can reach you at 172.19.0.13:5000/heroyjenkins? Weird address, well have fun.')
    adventurer_data = '{"heroclass":"juggernaut","capabilities":"'+ str(get_config()[util_req]) +'","url":"http://172.19.0.13:5000/heroyjenkins"}'
    requests.post(paths_util.adventurers_uri(), headers=auth_header, data=adventurer_data)
    print('\nYou enter the dusty taverna')
    in_taverna = True
    while in_taverna:
        divide_line()
        in_taverna = taverna_ui(auth_header)
    print('Leaving the taverna')


def taverna_ui(auth_header):
    print('\nTaverna')
    print()
    print('1: Be careful with the adventurers')
    print('2: To quest, you need groups! Go get one')
    print('Else to get out')
    print()
    return taverna_filter(input('What will you do? \n> '), auth_header)


def taverna_filter(choice, auth_header):
    choice_filter = {
        '1': adventurer_ui,
        '2': show_groups
    }
    if not choice_filter.get(choice):
        return False
    return choice_filter.get(choice)(auth_header), ''


def show_groups(auth_header):
    response = requests.get(paths_util.group_url(), headers=auth_header)
    groups = {}
    for group in response.json()['objects']:
        groups[str(group['id'])]=group
    return group_ui(auth_header, groups)