import requests, json
from multiprocessing.pool import ThreadPool
from .paths_names import util_user, util_own_server
from .paths_util import make_http
from quests.quest1.taverna.groups import start_election
from quests.quest1.utilities import divide_line
from quests.utils import paths_util, get_config, change_config
from quests.utils.paths_names import auth_token, util_assignments, util_group


def election_algorithm(election_data):
    data = json.dumps(election_data)
    response = requests.get(get_config()[util_group] + get_config()['member_url'], headers=get_config()[auth_token])
    coordinator = True
    pool = ThreadPool(processes=3)
    for member in response.json()['objects']:
        if member['user'] > ('/users/' + get_config()[util_user]):
            if make_http(member['url']) != get_config()[util_own_server]:
                try:
                    user = requests.get(make_http(member['url']))
                    async_result = pool.apply_async(recv_ok, (make_http(member['url']) + user.json()['election'], data))
                    if async_result.get():
                        coordinator = False
                except Exception as ex:
                    print('Could not reach - ' + str(member['user']))
                    print(ex)
    if coordinator:
        divide_line()
        print('Heroy is president!')
        if input('solve the assginment? ') == 'y':
            ok = solve_assignment(election_data['job'], election_data['job']['callback'])
            if not ok:
                print('Could not finish our assignment!')
        else:
            election_algorithm(election_data)

    else:
        divide_line()
        print('What?! We were not elected? Change our name to "zzzz" immediatly!')


def recv_ok(url, data):
    try:
        response = requests.post(url, data=data)
        print('Reached user ' + url)
        if response.status_code == 200 or response.status_code == 201:
            if response.json()['message'].lower() == 'ok':
                return True
        return False
    except Exception as ex:
        divide_line()
        print('Could not reach ' + url)
        print(ex)


'''
{
"algorithm":"<name of the algorithm used>",
"payload":"<the payload for the current state of the algorithm>",
"user":"<uri of the user sending this request>",
"job":"<JSON description of the job to do>",
"message": "<something you want to tell the other one>"
}
{
"id":"<some identity choosen by the initiator to identify this request>",
"task":"<uri to the task to accomplish>",
"resource":"<uri or url to resource where actions are required>",
"method":"<method to take – if already known>",
"data":"<data to use/post for the task>",
"callback": "<an url where the initiator can be reached with the results/token>",
"message": "<something you want to tell the other one>"

'''

def solve_assignment(json_data, sender_uri):
    change_config(util_assignments, json_data)

    divide_line()
    print('Received assignment: \n' + str(json_data['message']) + '\n' + str(
        json_data['method']) + '\n' + str(json_data['resource']))
    print()
    url = paths_util.make_http(json_data['resource'])
    if json_data['method'].lower() == 'get':
        response = requests.get(url, headers=get_config()[auth_token], data=json_data['data'])
    elif json_data['method'].lower() == 'post':
        response = requests.post(url, headers=get_config()[auth_token], data=json_data['data'])
    else:
        return False

    if response.status_code == 200:
        print(response.json()['message'])
        print()
        print(response.json())
        if response.json().get('hint'):
            print(response.json()['hint'])
            divide_line()
            print('Starting new election')
            new_assignment = json_data
            new_assignment['job'] = {
                "id": json_data['id'],
                "task": json_data['task'],
                "resource": json_data['resource'],
                "method": json_data['method'],
                "data": str(json.dumps({
                    "group": get_config()[util_group],
                    "token": response.json()['token']
                })),
                "callback": json_data['callback'],
                "message" : "Oh no, i am unconcious, take over please!"
            }
            start_election(election_data=new_assignment)

        answer = json.dumps({
            'id': json_data['id'],
            'task': json_data['task'],
            'resource': json_data['resource'],
            'method': json_data['method'],
            'data': response.json(),
            'user': get_config()['username'],
            'message': 'Swifty swooty as ever has Heroy done his job.'
        })

        requests.post(paths_util.make_http(sender_uri + json_data['callback']), data=answer)
        callback_address = paths_util.make_http(sender_uri + json_data['callback'])
        print('That went well, answering to Callback! ' + str(callback_address))
        try:
            callback_resp = requests.post(callback_address, data=answer)
            if callback_resp.status_code == 200 or callback_resp.status_code == 201:
                divide_line()
                print('Callback sent successfully')
            else:
                print('Could not reach callback url')
                divide_line()
        except Exception as cre:
            print('Could not reach callback, Connection Refused!')
            print(cre)
    else:
        divide_line()
        return False
