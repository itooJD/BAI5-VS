import requests
from quests.utils.config_manager import set_server_url_via_udp


def register(paths):
    user_json = '{"name":"HeroyJenkins", "password":"pass"}'
    register_resp = requests.post(paths['server'] + paths['user_url'], data=user_json)
    print('User registered')
    print(register_resp.json()['message'])

def login(paths):
    login_resp = requests.get(paths['server'] + paths['login_url'], auth=('HeroyJenkins', 'pass'))
    print('Logged in')
    print(login_resp)
    return login_resp.json()['token']

def whoami(paths, headers):
    whoami_resp = requests.get(paths['server'] + paths['whoami_url'], headers=headers)
    print(whoami_resp.json()['message'])

def quest(paths, headers):
    quest_resp = requests.get(paths['server'] + paths['blackboard_url'] + paths['quest_url'], headers=headers)
    print(quest_resp)

def map(paths, headers):
    map_resp = requests.get(paths['server'] + paths['map_url'], headers=headers)
    print(map_resp)
    print(map_resp.json()['objects'][2]['name'])
    return  map_resp.json()['objects'][2]['host']

def visit(paths, headers, quest_host):
    visit_resp = requests.post('http://' + quest_host + paths['visit_url'], headers=headers)
    print(visit_resp.json()['message'] + ' with token: ' + visit_resp.json()['token_name'])
    throneroom_token =  visit_resp.json()['token']
    return {'tokens': {'/blackboard/tasks/2': throneroom_token}}

def deliver(paths, headers, deliver_token):
    last_resp = requests.post(paths['server'] + paths['blackboard_url'] + paths['quest_url'] + '/1' + paths['last_url'], headers=headers, data=deliver_token)
    print(last_resp.json()['message'])
    # print(last_resp.json()[''])
    print("Quest successfully closed")

if __name__ == '__main__':
    paths = set_server_url_via_udp()
    register(paths)
    auth_token = login(paths)
    headers = {'Authorization': 'Token ' + str(auth_token)}
    whoami(paths, headers)
    quest(paths, headers)
    quest_host = map(paths, headers)
    deliver_token = visit(paths, headers, quest_host)
    deliver(paths, headers, deliver_token)