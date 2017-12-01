import requests
from quests.utils import paths_util, get_config, change_config
from quests.quest1.utilities import divide_line
from quests.utils.paths_names import util_group, util_user, util_req


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


def show_all_groups(auth_header, groups):
    response = requests.get(paths_util.group_url(), headers=auth_header)
    for group in response.json()['objects']:
        groups[str(group['id'])]=group
        print(str(group['id']) + ': Owner - ' + group['owner'] + ' | ' + str(group['members']) + ' | ' + str(group['_links']))
    divide_line()


def join_group(auth_header, groups):
    divide_line()
    group_id = input('Which group do you want to join then? [a valid id]\n> ')
    group_existant = False
    if group_id in groups:
        group_existant = True
    if group_existant:
        response = requests.post(paths_util.group_url_id(group_id) + get_config()['member_url'], headers=auth_header)
        group_get = requests.post(paths_util.group_url_id(group_id), headers=auth_header)
        print(group_get.json())
        print(response.json())
        print('Joined Group')
        if response.status_code == 200 or response.status_code == 201:
            change_config(util_group, response.json()['url'])
            change_config(util_req,util_group)
    else:
        print('The group with this id does not exist')


def delete_your_group(auth_header, groups):
    response = requests.delete(paths_util.server_uri(get_config()['group_uri']), headers=auth_header)
    if response.status_code == 200:
        change_config(util_group, '')
        print('Deleted your group!')
    else:
        print(response.json())


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
        for member in response.json()['objects']:
            if member.get('heroclass'):
                print(member.get('heroclass') + ' | ', end='')
            if member.get('user', ''):
                print(member.get('user') + ' | ', end='')
            if member.get('capabilities'):
                print(member.get('capabilities') + ' | ', end='')
            if member.get('url'):
                print(member.get('url'), end='')
            print()
    else:
        print('The group with the given id does not exist')


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