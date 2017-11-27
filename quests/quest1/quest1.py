import requests
from quests.utils.config_manager import set_server_url_via_udp


def register(paths):
    user_json = '{"name":"HeroyJenkins", "password":"pass"}'
    register_resp = requests.post(paths['server'] + paths['user_url'], data=user_json)
    print('Quest1: User registration: ' + register_resp.json()['message'])

def login(paths):
    login_resp = requests.get(paths['server'] + paths['login_url'], auth=('HeroyJenkins', 'pass'))
    print('Quest1: Login: ' + str(login_resp.json()['message']))
    return login_resp.json()['token']

def whoami(paths, headers):
    whoami_resp = requests.get(paths['server'] + paths['whoami_url'], headers=headers)
    print('Quest1: WhoAmI: ' + str(whoami_resp.json()['message']))

def quest(paths, headers):
    quest_resp = requests.get(paths['server'] + paths['blackboard_url'] + paths['quest_url'], headers=headers)
    quests = []
    available_quests = []
    print('Quest1: Available quests: \n')
    for idx, quest in enumerate(quest_resp.json()['objects']):
        print('#################################')
        print('Quest with index: ' + str(idx))
        print(quest['name'])
        print(quest['description'])
        requirements_fullfilled = True
        if quest['requirements']:
            for req in quest['requirements']:
                if req not in paths['requirements']:
                    requirements_fullfilled = False
                    print('\n!!! The requirements for this quest are not fullfilled by our hero :C !!!')
                    break
        if requirements_fullfilled:
            available_quests.append(idx)
            quests.append(quest)
        print()
    quest_no = -1
    print(available_quests)
    while quest_no not in available_quests:
        quest_no = input('Which quest do you want to tackle mighty Heroy? [Index starting from 0] ')
    quest = quests[available_quests.index(quest_no)]
    print('Quest1: Accepted quest ' + quest['name'])
    print('Quest1: This quest requires the tokens: ' + quest['requires_tokens'])

def map(paths, headers):
    map_resp = requests.get(paths['server'] + paths['map_url'], headers=headers)
    print('Quest1: Map: ' + str(map_resp.json()))
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