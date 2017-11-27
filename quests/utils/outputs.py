def authentication_ui():
    print('1: Register')
    print('2: Login')
    print('else to exit')
    return input('Choice: ')


def main_ui(quest, group_uri):
    print('\nNext Steps')
    print('1: Quests')
    print('2: Taverna')
    print('3: Users')
    print('4: Map')
    print('5: Logout')
    if bool(quest):
        print('6: Quest')
    if group_uri != '':
        print('7: Group')
    print('else to exit')
    return input('Where do you want to go: ')


def taverna_ui():
    print('\nTaverna')
    print('1: Adventurers')
    print('2: Groups')
    print('else to go back')
    return input('Which list do you want to see: ')


def group_ui(group_uri):
    print('\nid: to inspect group')
    if group_uri == '':
        print('new: to create new group')
    print('else to go back')
    return input('what do you want to do: ')


def invite_ui():
    print('id: invite to group')
    print('else to go back')
    return input('what to you want to do: ')


def groups(response):
    objects = response.json()['objects']
    print('\nGroups')
    print('\nID\tMembers\tOwner')
    ids = list()
    for group in objects:
        ids.append(str(group['id']))
        print(group['id'], '\t', len(group['members']), '\t', group['owner'])
    return ids


def group(response):
    group = response.json()['object']
    print('Group: ', group['id'], '\t', group['owner'])
    print('Members')
    for member in group['members']:
        print(member)
    return group['_links']['self']


def my_infos(response):
    print('\nMy Status\n')
    user = response.json()['user']
    user_name = user['name']
    print('Name: ', user['name'])
    print('Location: ', user['location'])
    print('Delivered: ', user['delivered'])
    print('Deliverables done: ', user['deliverables_done'])
    print('ip: ', user['ip'])
    return user_name


def users(response):
    print('\nAll Users')
    counter = 1
    for user in response.json()['objects']:
        [print() if ((counter % 10) == 0) else print('', end='')]
        try:
            print(user['name'], end=', ')
        except Exception:
            print('', end='')
        counter = counter + 1


def adventurers(response):
    print('\nAdventurers')
    return response.json()['objects']
