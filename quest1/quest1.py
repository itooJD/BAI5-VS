import requests


blackboard_server_url = 'http://172.19.0.3:5000'
user_url = '/users'
login_url = '/login'
whoami_url = '/whoami'
blackboard_url = '/blackboard'
map_url = '/map'
visit_url = '/visits'
quest_url = '/quests'
last_url = '/deliveries'

# user_name = input('Please give your name, mighty hero!')
user_name = "HeroyJenkins"

user_json='{"user":{0}, "password":"pass"}'.format(user_name)
register_resp = requests.post(blackboard_server_url + user_url,  data=user_json)
print('User registered')
print(register_resp)

login_resp = requests.get(blackboard_server_url + login_url, auth=(user_name, 'pass'))
print('Logged in')
print(login_resp)
auth_token = login_resp.json()['token']
print('Token is: ' +  auth_token)

headers={'Authorization': 'Token ' +  str(auth_token)}
whoami_resp = requests.get(blackboard_server_url +  whoami_url, headers=headers)
print(whoami_resp.json()['message'])

quest_resp = requests.get(blackboard_server_url + blackboard_url + quest_url, headers=headers)
print(quest_resp)

map_resp = requests.get(blackboard_server_url + map_url, headers=headers)
print(map_resp)

quest1_host = map_resp.json()['objects'][2]['host']
print(map_resp.json()['objects'][2]['name'])

visit_resp = requests.post('http://' + quest1_host +  visit_url, headers=headers)
print(visit_resp.json()['message'] + ' with token: ' + visit_resp.json()['token_name'])
throneroom_token = visit_resp.json()['token']

deliver_data = '{{"tokens": {{ {0}: {1} }} }}'.format(blackboard_url + quest_url + '1', throneroom_token)
last_resp = requests.post(blackboard_server_url +  blackboard_url + quest_url + '1' + last_url, headers=headers, data=deliver_data)
# print(last_resp.json()[''])
print("Quest successfully closed")