import requests, json
from flask_restful import Resource
from flask import request, abort, jsonify
from quests.utils import change_config, get_config
from quests.utils.paths_names import util_assignments, auth_token as token
from quests.utils import paths_util
from quests.quest1.utilities import divide_line


# Post assignments
class HeroysMightyTasks(Resource):
    def get(self):
        # depending if we want to save the data locally or not

        json_data = request.get_json(force=True)
        try:
            if bool(json_data) and len(json_data) == 1 and json_data['heroy'] == 'user':
                return jsonify(get_config()[util_assignments])
            else:
                return jsonify({"message": "whaaat the hellllllll"})
        except KeyError:
            return abort(400)

    def post(self):
        try:
            json_data = request.get_json(force=True)
            if bool(json_data) and len(json_data) == 7:
                change_config(util_assignments, {
                    "id": json_data['id'],
                    "task": json_data['task'],
                    "resource": json_data['resource'],
                    "method": json_data['method'],
                    "data": json_data['data'],
                    "callback": json_data['callback'],
                    "message": json_data['message']
                })
                # auto completing assignment?
                divide_line()
                print('Received assignment: \n' + str(json_data['message']) + '\n' + str(json_data['method']) + '\n' + str(json_data['resource']))
                print()
                url = paths_util.make_http(json_data['resource'])
                if json_data['method'].lower() == 'get':
                    response = requests.get(url, headers=get_config()[token], data=json_data['data'])
                elif json_data['method'].lower() == 'post':
                    response = requests.post(url, headers=get_config()[token], data=json_data['data'])
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
            else:
                return abort(400)
        except KeyError or TypeError:
            return abort(400)