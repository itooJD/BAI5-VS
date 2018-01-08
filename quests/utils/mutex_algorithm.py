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

    # get adventurers list
    adventurers = list()
    for adventurer in adventurers:
        # send post request to adventurer
        response = requests.post(adventurer, data=request, timeout=0.2)
        data = response.json()
        if data['msg'] != 'reply-ok' or response.status_code != 200:
            waiting_answers.append(adventurer)
        lamport_clock += 1

    change_config('waiting_answers', waiting_answers)
    change_config('lamport_clock', lamport_clock)

    while len(waiting_answers) > 0:
        waiting_answers = config['waiting_answers']
    state["state"] = "held"
    requests.put('http://' + str(own_address) + ':' + str(5000), data=state)
    # do something
    state["state"] = "released"
    requests.put('http://' + str(own_address) + ':' + str(5000), data=state)
