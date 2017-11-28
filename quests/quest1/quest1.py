import requests
from quests.utils.config_manager import set_server_url_via_udp


def register(paths):
    from quests.quest2.questing_resources.authentification import authentification
    return authentification('')


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
    print('#################################')
    print('Available index values: ' + str(available_quests))
    while int(quest_no) not in available_quests:
        quest_no = input('Which quest do you want to tackle mighty Heroy? [Index starting from 0] \n > ')
    quest = quests[int(quest_no)]
    print('Quest1: Accepted quest ' + quest['name'])
    print('Quest1: This quest requires the tokens: ' + str(quest['requires_tokens']))
    print('and requires of you to open the task: ' + str(quest['tasks']))
    return str(int(quest_no) + 1), quest['tasks']


def task(paths, headers):
    print()
    task_no = input('Quest1: Which task are we looking for again? \n > ')
    task_resp = requests.get(paths['server'] + paths['blackboard_url'] + '/tasks/' + task_no, headers=headers)
    if task_resp.status_code == 200:
        print('### This task exists! You are making me proud Heroy! ###')
        print(task_resp.json()['object']['description'])
        print('It seems we have to go to: ' + str(task_resp.json()['object']['location']))
        print('And there to: ' + str(task_resp.json()['object']['resource']))
    return str(task_resp.json()['object']['resource']), task_no


def map(paths, headers, task):
    print()
    print('Quest1: Lets look this up on the map')
    map_resp = requests.get(paths['server'] + paths['map_url'], headers=headers)
    map = ''
    for map_item in map_resp.json()['objects']:
        if int(task) in map_item['tasks']:
            print('What do we have here...! The place we have to go: ' + str(map_item['host']))
            map = map_item['host']
            break
    return map


def visit(headers, quest_host, location_url):
    print()
    print('Quest1: Finally, we arrived at {0}{1}. Lets see what we can find at this place!'.format(quest_host,
                                                                                                   location_url))
    visit_resp = requests.post('http://' + quest_host + location_url, headers=headers)
    print(visit_resp.json()['message'] + ' with token: ' + visit_resp.json()['token_name'])
    throneroom_token = visit_resp.json()['token']
    print()
    print('You acquired the token! \n' + str(throneroom_token))
    return throneroom_token


def deliver(paths, headers, deliver_token, quest_no, task_uris):
    print()
    print('Quest1: Now let us deliver our token. Back to the blackboard!')
    print(deliver_token)
    for task_uri in task_uris:
        token = '{"' + task_uri + '":"' + deliver_token + '"}'
        data = '{"tokens":' + token + '}'
        print('Lets give our quest back to: ' + paths['server'] + paths['blackboard_url'] + paths['quest_url'] + '/' + quest_no + paths['deliver_url'] + '\n with token: ' + data)
        last_resp = requests.post(paths['server'] + paths['blackboard_url'] + paths['quest_url'] + '/' + quest_no + paths['deliver_url'],
                              headers=headers, data=data)
        print(last_resp.json())
    try:
        print(last_resp.json()['message'])
        if not last_resp.json()['error']:
            print("Quest successfully closed! Herrrrroooooooooy Jeeeeenkiiiiiins!!")
        else:
            print(last_resp.json()['error'])
    except Exception as ex:
        print(last_resp.status_code)
        print('', end='')
        print('Quest1: Could not be completed, caught exception - ' + str(ex))


if __name__ == '__main__':
    paths = set_server_url_via_udp()
    _, headers = register(paths)
    print('Quest1: Authentication Token: ' + str(headers))
    whoami(paths, headers)
    quest_no, task_uris = quest(paths, headers)
    location_url, task = task(paths, headers)
    quest_host = map(paths, headers, task)
    deliver_token = visit(headers, quest_host, location_url)
    deliver(paths, headers, deliver_token, quest_no, task_uris)
    # curl -H {'Authorization': 'Token eyJ1c2VybmFtZSI6ICJQZWFjb2NrIiwgImF1dGgiOiAiWjBGQlFVRkJRbUZJWkdZM2IzVkZZV3c1T1RaV1pXNVlhRGxuYUhOcWIzUnNRVmgzUlU1MFdsUkZSR2hWYkhWWlR6bDNaMUJJYVMxS2NIQnJkWE41WVZKRlZXZG5NMVYzVVVadWFsaFVlazF3UTFOTlpIYzRNM052YjNnMFJYQmxZbWxEUXpsVGVqRmxXbkZUZDFjMlJYcGpWVVJHVnpBelQydFhVVWg2T1hsNFdXbEVNVVpmU2pCUk4xSlhSelJaZW1wdldVTk1hMkZZZEdjemFsbFBPVUpCUFQwPSJ9'}  -X POST 172.19.0.7:5000/blackboard/tasks/2/deliveries -d {"tokens":{"task_uri":"Z0FBQUFBQmFIZGdBcFctNmlsajNneXF6d3pYeXdEdGxpZXhEZ0Fhc1dhNV9iUjE2TXNJbFpXd05NOG1JMmhNSmg5YmZwZS1GX3lwSkt4QWhMTEdnMUY5dlN3VlBiQUxzWGV4MFhVRjRPeEFOblNGd1prOEdnM0hiaHZWU1RVRmlHZFpBU3EtbXFRVGZzaWg0S3pCc2V1VlF6RC1PSlVQdms3TGtEMVR2b0Y4N2xlSTU5WkM0cTdpbnR4TVRSbjBuTWlSaWpJSF9QNVpNdmg0N19mTlRKNFkxdnlRM0dpRkh2alJzWkt1ZVBKcDZZOVNXRTc2cjRFX0NIdWVrNWJnQjdoaXVSTnhIaDVMNkpIWTVSY05fNThxLUFLblhoM0s2aUk0V2hIX1UtQzhWVFVEdDE3cVZ0QWhyRzY1UG9Ccm5EZHBhNDUyTHZiQ1M2RTdCVmxQamYwTHpadnFUQ1ByZ3VEQ0VibHdvYkY3eTJmdGtYWWxFbU5uZEZWWnVOUVdJRFd5dWt2VEtUaWNFMlppQzZDWFVIZUVsM1JWV2RCR0RkTnJ4aXFqWHAxSmhuX0w4dUg4N3Q1SWhyb19udEtHT1lIWGZiVVBXbVlQS19zSk1QdDUtOWt3a1kwczgtNHNVZC1Gd3BQaFlXbVpUajF6ZGU1c0I4bHZaR05GejFXZUQyeS1QWkRDUlBxT29wZ3drTldKeUZaelRkWlZIaUd3cFhIMng3SXpqdHZaeWhiWTBqSnhDMU1lUWV2Sms2MUFnaURpUS1KQmdtRzRZNi11NjdWMU1Ib09wVXY4eUxrZ255eTB2cy13MTdTZ1hFWjd6NW1pbGpQM2EzeEo2U3A4MzNkLXljQXdSbXJ2dg=="}}