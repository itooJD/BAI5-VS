import requests
from flask_restful import Resource, reqparse
from quests.utils import get_config
from flask import request, abort, jsonify
from quests.utils.config_manager import write_assignment, get_assignment


# Post assignments
class HeroysMightyTasks(Resource):
    def get(self):
        # depending if we want to save the data locally or not

        json_data = request.get_json(force=True)
        try:
            if bool(json_data) and len(json_data) == 1 and json_data['heroy'] == 'user':
                return jsonify(get_assignment())
            else:
                return jsonify({"message": "whaaat the hellllllll"})
        except KeyError:
            return abort(400)

    def post(self):
        try:
            json_data = request.get_json(force=True)
            if bool(json_data) and len(json_data) == 7:
                write_assignment({
                    "id": '"' + json_data['id'] + '"',
                    "task": '"' + json_data['task'] + '"',
                    "resource": '"' + json_data['resource'] + '"',
                    "method": '"' + json_data['method'] + '"',
                    "data": '"' + json_data['data'] + '"',
                    "callback": '"' + json_data['callback'] + '"',
                    "message": '"' + json_data['message'] + '"'
                })
                return jsonify({"message": "assignment received"})
                # auto completing assignment?
                '''
                if json_data['method'] == 'GET':
                    response = requests.post(json_data['resource'], headers=auth_header, data=json_data['data'])
                elif json_data['method'] == 'POST':
                    response = requests.post(json_data['resource'], headers=auth_header, data=json_data['data'])
                else:
                    return abort(400)

                if response.status_code == 200:
                    answer = {
                        'id': json_data['id'],
                        'task': json_data['task'],
                        'resource': json_data['resource'],
                        'method': json_data['method'],
                        'data': response,
                        'user': hero_url,
                        'message': 'Swifty swooty as ever has heroy done his job'
                    }
                    requests.post(json_data['callback'], data=answer)
                    '''
            else:
                return abort(400)
        except KeyError or TypeError:
            return abort(400)
