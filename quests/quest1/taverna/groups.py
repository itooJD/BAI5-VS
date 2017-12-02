import requests, json
from quests.utils import paths_util, get_config, change_config, add_to, rm_from
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
    print('8: Send assignment to own group')
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
        '7': show_all_groups,
        '8': send_assignment_to_group
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
        print(response.json()['message'] + ' ' + str(group_id))
        if response.status_code == 200 or response.status_code == 201:
            print('Joined Group!')
            group_get = requests.get(paths_util.group_url_id(group_id), headers=auth_header)
            if group_get.status_code == 200 or group_get.status_code == 201:
                group_url = group_get.json()['object']['_links']['self']
                change_config(util_group, paths_util.server_uri(group_url))
                add_to(util_req,util_group)
                adventurer_data = '{"heroclass":"juggernaut","capabilities":"' + str(
                    get_config()[util_req]) + '","url":"http://172.19.0.13:5000/"}'
                requests.post(paths_util.adventurers_uri(), headers=auth_header, data=adventurer_data)
            else:
                print('Could not find the group. Where did they hide?!')
        else:
            print('Seems they dont want you in this group. Could not join.')
    else:
        print('The group with this id does not exist')


def delete_your_group(auth_header, groups):
    response = requests.delete(paths_util.server_uri(get_config()[util_group]), headers=auth_header)
    if response.status_code == 200:
        change_config(util_group, '')
        rm_from(util_req,util_group)
        adventurer_data = '{"heroclass":"juggernaut","capabilities":"' + str(
            get_config()[util_req]) + '","url":"http://172.19.0.13:5000/"}'
        requests.post(paths_util.adventurers_uri(), headers=auth_header, data=adventurer_data)
        print('Deleted your group!')
    else:
        print('Could not delete the group :C')
        print(response.json())


def create_group(auth_header, groups):
    divide_line()
    create_new = False
    if get_config()[util_group] != '':
        print('You are already in a group! ' + str(get_config()[util_group]))
        create = input('Do you really want to create another one? [y]\n> ')
        if create == 'y':
            create_new = True
    else:
        create_new = True
    if create_new:
        response = requests.post(paths_util.group_url(), headers=auth_header)
        change_config(util_group,response.json()['object'][0]['_links']['self'])
        print(response.json()['message'])
    show_all_groups(auth_header, groups)
    divide_line()
    join = input('Well you founded it... You want in? [y]\n> ')
    if join == 'y':
        join_group(auth_header, groups)


def check_members(auth_header, groups):
    divide_line()
    group_id = input('So which groups members are ya lookin for? Your own? [a valid id / y (for own)]\n> ')
    if group_id == 'y':
        group_url = get_config()[util_group]
        if group_url != '':
            response = requests.get(group_url + get_config()['member_url'], headers=auth_header)
            print('Members: ')
            for member in response.json()['objects']:
                print_member(member)
        else:
            print('Well you aint in no group duh.')
    else:
        group_existant = False
        if group_id in groups.keys():
            group_existant = True
        if group_existant:
            response = requests.get(paths_util.group_url_id(group_id) + get_config()['member_url'], headers=auth_header)
            print('Members: ')
            for member in response.json()['objects']:
                print_member(member)
        else:
            print('The group with the given id does not exist')

def print_member(member_json):
    if member_json.get('heroclass'):
        print(member_json.get('heroclass') + ' | ', end='')
    if member_json.get('user', ''):
        print(member_json.get('user') + ' | ', end='')
    if member_json.get('capabilities'):
        print(member_json.get('capabilities') + ' | ', end='')
    if member_json.get('url'):
        print(member_json.get('url'), end='')
    print()


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
    if get_config()[util_group] != '':
        print('Our group: ' + str(get_config()[util_group]))
        response = requests.get(get_config()[util_group], headers=auth_header)
        print(str(response.json()))
    else:
        print('You are in no group!')


def send_assignment_to_group(auth_header, _, id=None, task=None, resource=None, method=None, task_data=None, message=None):
    if get_config()[util_group] != '':
        if not id:
            id = input('ID:         ')
        if not task:
            task = input('Tasknumber: ')
        if not resource:
            resource = input('Resource:   ')
        if not method:
            method = input('Method:     ')
        if not task_data:
            task_data = input('Data:       ')
            if not task_data:
                task_data = ''
        if not message:
            message = input('Message:    ')

        response = requests.get(get_config()[util_group] + get_config()['member_url'],
                                headers=auth_header)
        print(response.json())

        for member in response.json()['objects']:
            data = json.dumps({
                "id": str(id),
                "task": get_config()['blackboard_url'] + get_config()['task_url'] + task,
                "resource": str(resource),
                "method": str(method),
                "data": str(task_data),
                "callback": get_config()['callback_url'],
                "message": str(message)
            })
            try:
                member_data = requests.get(member['url'])
            except Exception:
                print('Member ' + str(member['user']) + ' could not be reached')
            if member_data and (member_data.status_code == 200 or member_data.status_code == 201):
                print(member_data.json())
                user_url = paths_util.make_http(member['url'])
                print(user_url + member_data.json()['assignments'])

                try:
                    response = requests.get(user_url)
                    print(response.json()['user'])
                    response = requests.post(user_url + member_data.json()['assignments'], data=data)
                    if response.status_code == 200:
                        print('Assignment sent to ' + str(member['user']))
                except Exception:
                    print('Member: ' + str(member['user']) + ' could not be reached')
            else:
                print('Member URL could not be reached!')
