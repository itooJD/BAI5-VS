import requests
from multiprocessing.pool import ThreadPool

from quests.utils.assignment_solver import solve_assignment
from .config_manager import get_config
from .paths_names import util_user, util_group, auth_token, util_own_server
from .paths_util import make_http


def election_algorithm(data):
    response = requests.get(get_config()[util_group] + get_config()['member_url'], headers=get_config()[auth_token])
    coordinator = True
    pool = ThreadPool(processes=3)
    for member in response.json()['objects']:
        if member['user'] > ('/users/' + get_config()[util_user]):
            if make_http(member['url']) != get_config()[util_own_server]:
                print(member)
                async_result = pool.apply_async(recv_ok, (make_http(member['url']), data))
                if async_result.get():
                    coordinator = False
                    break
    if coordinator:
        print('Heroy is president!')
        solve_assignment(data['job'])
    else:
        print('What?! We were not elected? Change our name to "AAAA" immediatly!')


def recv_ok(url, data):
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200 or response.status_code == 201:
            if response.json()['message'].lower() == 'ok':
                return True
        return False
    except Exception as ex:
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