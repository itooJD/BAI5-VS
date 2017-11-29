import requests, json
from quests.quest1.utilities import divide_line
from quests.utils import paths_util, get_config, change_config
from quests.utils.paths_util import util_group, util_user


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


def adventurer_ui(auth_header):
    divide_line()
    print('\nWelcome, this is the place of the adventurers!')
    print()
    print('1: Look at the list behind the bar')
    print('2: Searching for someone?')
    print('Else: Get outta here')
    print()
    return adventurer_filter(input('Which list do you want to see: \n> '), auth_header)


def adventurer_filter(choice, auth_header):
    choice_filter = {
        '1': show_adventurers,
        '2': search_for_adventurer
    }
    if not choice_filter.get(choice):
        return False
    return choice_filter.get(choice)(auth_header), ''


def taverna(auth_header):
    # Entering the Taverna
    divide_line()
    print('So you are a juggernaut huh? And I can reach you at 172.19.0.13:5000/heroyjenkins? Weird address, well have fun.')
    adventurer_data = '{"heroclass":"juggernaut","capabilities":"","url":"172.19.0.13:5000/heroyjenkins"}'
    requests.post(paths_util.adventurers_uri(), headers=auth_header, data=adventurer_data)
    print('\nYou enter the dusty taverna')
    in_taverna = True
    while in_taverna:
        divide_line()
        in_taverna = taverna_ui(auth_header)
    print('Leaving the taverna')


def search_ui(auth_header, name):
    divide_line()
    print('And what do you want to do with ' + name + '?')
    print()
    print('1: Look real close! Get all the details.')
    print('2: I dont like, so I change!')
    print('3: Kill.')
    print('4: Hire him? This one? Hahaha, good luck')
    print()
    return search_adv_filter(input('Hm? Tell me. \n> '), auth_header, name)


def search_adv_filter(choice, auth_header, name):
    choice_filter = {
        '1': get_adventurer,
        '2': change_adventurer,
        '3': kill_adventurer,
        '4': hire_adventurer
    }
    if not choice_filter.get(choice):
        return False
    return choice_filter.get(choice)(auth_header, name), ''


def show_adventurers(auth_header):
    response = requests.get(paths_util.adventurers_uri(), headers=auth_header)
    adventurers = {}
    divide_line()
    for idx, adventurer in enumerate(response.json()['objects']):
        adventurers[str(idx)] = adventurer
        print(str(idx) + ': ', end='')
        if adventurer.get('heroclass'):
            print(adventurer.get('heroclass') + ' | ', end='')
        if adventurer.get('user',''):
            print(adventurer.get('user') + ' | ', end='')
        if adventurer.get('capabilities'):
            print(adventurer.get('capabilities') + ' | ', end='')
        if adventurer.get('url'):
            print(adventurer.get('url'), end='')
        print()
    divide_line()

    if get_config()['group_uri'] != '':
        recruit = input('Want to recruit one of these guys? [id,id,id]\n> ')
        to_hire = recruit.split(',')
        for id in to_hire:
            hire_adventurer(auth_header, adventurer=adventurers[id])


def get_adventurer(auth_header, name):
    response = requests.get(paths_util.adventurer_uri_name(name), headers=auth_header)
    if response.status_code == 200 or response.status_code == 201:
        print(response.json())

def change_adventurer(auth_header, name):
    response = requests.put(paths_util.adventurer_uri_name(name), headers=auth_header)
    print(response)
    divide_line()


def kill_adventurer(auth_header, name):
    response = requests.delete(paths_util.adventurer_uri_name(name), headers=auth_header)
    print(response)
    divide_line()


def hire_adventurer(auth_header, name=None, adventurer=None):
    if get_config()['group_uri'] == '':
        print('How do you want to hire, if you are in no group? First make one!')
        return
    else:
        group_uri = get_config()['group_uri']
    if adventurer:
        if adventurer['url']:
            hiring_uri = paths_util.http(adventurer['url'])
    elif name:
        pass
    message = input('An invite might not be enough. Write something: ')
    hirings_data = json.dumps({
        "group": group_uri,
        "quest": "quest",
        "message": message
    })
    try:
        response = requests.post(hiring_uri, data=hirings_data, timeout=50)
        print(response.status_code)
    except Exception:
        pass


def search_for_adventurer(auth_header):
    name = input('So.. Whom then? \n> ')
    search_ui(auth_header, name)


def group_ui(auth_header, groups):
    print('You can find a group to adventure with here... Want to?')
    print()
    print('1: Join a group')
    print('2: Delete your groups')
    print('3: Create your own group')
    print('4: Check the members of a group')
    print('5: Leave a group')
    print('6: Check your own group out')
    print('7: Show me all the groups')
    print()
    return group_filter(input('Sure about that? \n> '), auth_header, groups)


def group_filter(choice, auth_header, groups):
    choice_filter = {
        '1': join_group,
        '2': delete_your_group,
        '3': create_group,
        '4': check_members,
        '5': leave_group,
        '6': check_own_group,
        '7': show_all_groups
    }
    if not choice_filter.get(choice):
        return False
    return choice_filter.get(choice)(auth_header, groups), ''


def show_groups(auth_header):
    response = requests.get(paths_util.group_url(), headers=auth_header)
    groups = {}
    for group in response.json()['objects']:
        groups[str(group['id'])]=group
    return group_ui(auth_header, groups)


def show_all_groups(auth_header, groups)
    response = requests.get(paths_util.group_url(), headers=auth_header)
    for group in response.json()['objects']:
        groups[str(group['id'])]=group
        print(str(group['id']) + ': Owner - ' + group['owner'] + ' | ' + str(group['members']) + ' | ' + str(group['_links']))
    divide_line()


def join_group(auth_header, groups):
    divide_line()
    group_id = input('Which group do you want to join then? [a valid id]\n> ')
    group_existant = False
    print(type(groups))
    if group_id in groups:
        group_existant = True
    if group_existant:
        response = requests.post(paths_util.group_url_id(group_id) + get_config()['member_url'], headers=auth_header)
        print(response.json())
        print('Joined Group')
    else:
        print('The group with this id does not exist')


def delete_your_group(auth_header, groups):
    response = requests.delete(paths_util.server_uri(get_config()['group_uri']), headers=auth_header)
    if response.status_code == 200:
        change_config(util_group, '')
        print('Deleted your group!')


def create_group(auth_header, _):
    divide_line()
    create_new = False
    if get_config()['group_uri'] != '':
        print('You are already in a group! ' + str(get_config()['group_uri']))
        create = input('Do you really want to create another one? [y]\n> ')
        if create == 'y':
            create_new = True
    else:
        create_new = True
    if create_new:
        response = requests.post(paths_util.group_url(), headers=auth_header)
        change_config(util_group,response.json()['object'][0]['_links']['self'])
        print(response.json()['message'])


def check_members(auth_header, groups):
    divide_line()
    group_id = input('Which group do you want to join then? [a valid id]\n> ')
    group_existant = False
    if group_id in groups.keys():
        group_existant = True
    if group_existant:
        response = requests.get(paths_util.group_url_id(group_id) + get_config()['member_url'], headers=auth_header)
        print(response.json())


def leave_group(auth_header, groups):
    divide_line()
    print('The groups you are in:')
    groups_you_are_in = []
    for k,v in groups.items():
        if v['owner'] == get_config()[util_user]:
            groups_you_are_in.append(v)
    print(groups_you_are_in)
    divide_line()
    group_id = input('Which group do you want to leave then? [a valid id]\n> ')
    group_existant = False
    if group_id in groups:
        group_existant = True
    if group_existant:
        response = requests.post(paths_util.group_url_id(group_id) + get_config()['member_url'], headers=auth_header)
        print(response.json())
        print('Joined Group')
    else:
        print('The group with this id does not exist')


def check_own_group(auth_header, groups):
    divide_line()
    if get_config()['group_uri'] != '':
        print('Our group: ' + str(get_config()['group_uri']))
        response = requests.get(paths_util.server_uri(get_config()['group_uri']), headers=auth_header)
        print(response.json())
    else:
        print('You are in no group!')