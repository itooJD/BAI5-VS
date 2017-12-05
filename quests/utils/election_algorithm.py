import requests
from threading import Thread
from multiprocessing.pool import ThreadPool
from .config_manager import get_config
from .paths_names import util_user
from .paths_util import make_http
'''
Election algorithm(election_data):
   coordinator = True
   each user > self:
        if(OK =  send(POST, /election, timeout=5) as thread?):
             coordinator = False
  [print("Coordinator") if coordinator else print("not Coordinator")
'''

def election_algorithm(data):
    coordinator = True
    pool = ThreadPool(processes=10)
    for user in data['members']:
        if user['name'] > get_config()[util_user]:
            async_result = pool.apply_async(recv_ok, (make_http(user['url']), data))
            if async_result.get():
                coordinator = False
                break
    if coordinator:
        print('Heroy for president')
    else:
        print('What?! We were not elected? Change our name to "AAAA" immediatly!')


def recv_ok(url, data):
    response = requests.post(url, data=data)
    if response.status_code == 200 or response.status_code == 201:
        if response.json()['message'].lower() == 'ok':
            return True
    return False