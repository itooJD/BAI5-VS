import requests, json
from multiprocessing.pool import ThreadPool

from quests.quest1.utilities import divide_line
from quests.utils.assignment_solver import solve_assignment
from .config_manager import get_config
from .paths_names import util_user, util_group, auth_token, util_own_server
from .paths_util import make_http


def election_algorithm(election_data):
    data = json.dumps(election_data)
    response = requests.get(get_config()[util_group] + get_config()['member_url'], headers=get_config()[auth_token])
    coordinator = True
    pool = ThreadPool(processes=3)
    for member in response.json()['objects']:
        print(member['user'], ' > ', ('/users/' + get_config()[util_user]), ' = ',
              member['user'] > ('/users/' + get_config()[util_user]))
        if member['user'] > ('/users/' + get_config()[util_user]):
            print('will be tested')
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
