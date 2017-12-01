import requests, json
from quests.utils import paths_util, get_config
from quests.quest1.utilities import divide_line


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


def send_message_to_user(auth_header, response_json, user_url):
    divide_line()
    print('It is time to send a message!')
    message = input('Your message:\n> ')
    data = '{"message": "' + message + '"}'
    print(user_url)
    print(response_json['messages'])
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