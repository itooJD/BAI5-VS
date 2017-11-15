import requests, json


blackboard_server_url = 'http://172.19.0.3:5000'
user_url = '/users'
login_url = '/login'
whoami_url = '/whoami'
blackboard_url = '/blackboard'
map_url = '/map'
visit_url = '/visits'
quest_url = 'quests'
last_url = '/deliveries'

headers = {'content-type': 'application/json'}
user_json=json.dumps({"user":"HeroyJenkins", "password":"pass"})
register_resp = requests.post(blackboard_server_url + user_url, headers=headers,  data=user_json)
print('User registered')
print(register_resp)

login_resp = requests.get(blackboard_server_url + login_url, auth=('HeroyJenkins', 'pass'))
print('Logged in')
print(login_resp)
auth_token = login_resp.json()['token']

whoami_resp = requests.get(blackboard_server_url +  whoami_url, headers=('Authorization:Token ' +  auth_token))
print(whoami_resp.json()['message'])
quest_resp = requests.get(blackboard_server_url + blackboard_url + quest_url)
print(quest_resp.json()['objects'])
map_resp = requests.get(blackboard_server_url + map_url)
quest1_host = map_resp.json()['objects'][2]['host']
print(map_resp.json()['objects'][2]['name'])
visit_resp = requests.post(quest1_host +  visit_url)
print(visit_resp.json()['message'] + ' with token: ' + visit_resp.json()['token_name'])
throneroom_token = visit_resp.json()['token']
last_resp = requests.post(blackboard_server_url +  blackboard_url + quest_url + '1' + last_url, json='{"tokens": {{0}: {1} } }'.format(blackboard_url + quest_url + '1', throneroom_token))
# print(last_resp.json()[''])
print("Quest successfully closed")