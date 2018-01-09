import requests
from quests.client.utilities import divide_line, logout
from quests.utils import get_config, change_config
from quests.client.taverna.adventurers import get_all_adventureres

def mutex_ui(_):
    divide_line()
    print('Welcome to the Mutex UI.')
    print()
    print('1: Request Mutex')
    print('else to exit')
    return mutex_filter(input('\nWhat do you want to do?\n> '))

def mutex_filter(choice):
    choice_filter = {
        '1': request_mutex
    }
    if not choice_filter.get(choice):
        logout('')
    choice_filter.get(choice)()


def request_mutex():
    config = get_config()
    if config['state'] == 'wanting' or config['state'] == 'held':
        print('Already in a state of "wanting" or "held"')
        change_config('state', 'released')
    else:
        print('Sending requests to all adventureres')
        change_config('state','wanting')
        adventureres = get_all_adventureres()
        for adventurer in adventureres:
            try:
                response = requests.get(adventurer['url'])
                adventurer_mutex_endpoint = response.json()['mutex']
                data_json = {
                    "msg": "request",
                    "time": config['lamport_clock'],
                    "reply": config['mutex_url'],
                    "user": config['hero_url']
                }
                try:
                    requests.post(adventurer_mutex_endpoint, data=data_json)
                except Exception as e:
                    print('Something is wrong! Just wrong: \n' + str(e))
            except Exception as e:
                print('Adventurer with url ' + str(adventurer['url']) + ' could not be reached')
        print('All requests were sent, please work on the server')