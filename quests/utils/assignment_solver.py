import requests
from flask import request, json, abort, jsonify

from quests.quest1.utilities import divide_line
from quests.utils import paths_util, get_config, change_config
from quests.utils.paths_names import auth_token, util_assignments


def solve_assignment(json_data):
    change_config(util_assignments, json_data)

    divide_line()
    print('Received assignment: \n' + str(json_data['message']) + '\n' + str(
        json_data['method']) + '\n' + str(json_data['resource']))
    print()
    url = paths_util.make_http(json_data['resource'])
    print(url)
    if json_data['method'].lower() == 'get':
        response = requests.get(url, headers=get_config()[auth_token], data=json_data['data'])
    elif json_data['method'].lower() == 'post':
        response = requests.post(url, headers=get_config()[auth_token], data=json_data['data'])
    else:
        return abort(400)

    if response.status_code == 200:
        answer = json.dumps({
            'id': json_data['id'],
            'task': json_data['task'],
            'resource': json_data['resource'],
            'method': json_data['method'],
            'data': response.json(),
            'user': get_config()['username'],
            'message': 'Swifty swooty as ever has Heroy done his job.'
        })

        requests.post(paths_util.make_http(request.remote_addr + json_data['callback']), data=answer)
        callback_address = paths_util.make_http(request.remote_addr + json_data['callback'])
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
        return jsonify({"message": "That didnt go well duh"})