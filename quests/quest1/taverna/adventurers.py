import requests, json
from quests.utils import paths_util, get_config
from quests.quest1.utilities import divide_line


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


def user_interaction_ui(auth_header, response_json, user_url):
    divide_line()
    print('So we found this adventurer here ' + user_url)
    print('But what do we do with him?')
    print()
    print('1: Send a message.')
    print('2: Join group')
    print('3: Hire')
    print('4: Inspect group')
    print('5: Send assignment')
    print()
    return user_interaction_filter(input('Boss? \n> '), auth_header, response_json, user_url)

def user_interaction_filter(choice, auth_header, response_json, user_url):
    choice_filter = {
        '1': send_message_to_user,
        '2': join_group_of_user,
        '3': hire_user,
        '4': inspect_group,
        '5': send_assignment
    }
    if not choice_filter.get(choice):
        return False
    return choice_filter.get(choice)(auth_header, response_json, user_url), ''


def get_adventurer(auth_header, name):
    response = requests.get(paths_util.adventurer_uri_name(name), headers=auth_header)
    if response.status_code == 200 or response.status_code == 201:
        print('\nThe User: ' + str(response.json()))
        if not response.json()['object']['url'].startswith('http://'):
            user_url = 'http://' + response.json()['object']['url']
        else:
            user_url = response.json()['url'][0:response.json()['url'].find('/')]
            print(user_url)
        try:
            user_info = requests.get(user_url)
            print('User:           ' + str(user_info.json()['user']))
            print('Messages:       ' + str(user_info.json()['messages']))
            print('Idle:           ' + str(user_info.json()['idle']))
            print('Group:          ' + str(user_info.json()['group']))
            print('Hiring:         ' + str(user_info.json()['hirings']))
            print('Assignments:    ' + str(user_info.json()['assignments']))
            return user_interaction_ui(auth_header, user_info.json(), user_url)
        except ConnectionRefusedError:
            print('Connection Refused. Does not want to talk it seems :/')
    else:
        print('Could not connect to user')


def send_message_to_user(auth_header, response_json, user_url):
    divide_line()
    print('It is time to send a message!')
    message = input('Your message:\n> ')
    data = '{"message": "' + message + '"}'
    response = requests.post(user_url + response_json['messages'], data=data)
    if response.status_code == 200 or response.status_code == 201:
        print('The message has successfully been delivered.')
        print('\nAnwser:\n> ' + str(response.json()))
    else:
        print('Message could not be delivered')


def join_group_of_user(auth_header, response_json):
    pass


def hire_user(auth_header, response_json):
    pass


def inspect_group(auth_header, response_json):
    pass


def send_assignment(auth_header, response_json, user_url):
    data = json.dumps({
        "id": 9001,
        "task": '/blackboard/tasks/4' ,
        "resource": 'http://172.19.0.5:5000/stretcher/handle/back',
        "method": "POST",
        "data": '',
        "callback": get_config()['hero_url'],
        "message": "Do it nao xD"
    })
    response = requests.post(user_url + response_json.get('assignments'), data=data)
    if response.status_code == 200 or response.status_code == 201:
        print(response.json())
        print('Send assignment')
    else:
        print('Could not send the assignment. We are DOOOMED!')


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