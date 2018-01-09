import requests
from quests.utils import get_config, change_config


def enter_critical_section():
    config = get_config()
    own_address = config['own_address']
    lamport_clock = config['lamport_clock']
    waiting_answers = config['waiting_answers']
    request = {
        "msg": "request",
        "time": lamport_clock,
    }
    requests.post('http://' + str(own_address) + ':' + str(5000), data=request)
    state = {
        "message": "state",
        "state": "wanting"
    }
    requests.put('http://' + str(own_address) + ':' + str(5000), data=state)

    # Adventurers list kriegen
    # nötigen Informationen ip addresse + mutex-uri

    adventurers = list()
    for adventurer in adventurers:
        # request an den adventurer/mutex senden
        # wenn der nicht mit reply-ok antwortet
        #   füge die ip addresse in waiting_answers
        lamport_clock += 1

    change_config('waiting_answers', waiting_answers)
    change_config('lamport_clock', lamport_clock)

    while len(waiting_answers) > 0:
        waiting_answers = get_config()['waiting_answers']
    state["state"] = "held"
    requests.put('http://' + str(own_address) + ':' + str(5000), data=state)
    # do something
    state["state"] = "released"
    requests.put('http://' + str(own_address) + ':' + str(5000), data=state)
