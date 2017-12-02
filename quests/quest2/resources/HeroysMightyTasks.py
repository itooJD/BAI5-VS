import requests, sys, logging
from flask_restful import Resource
from flask import request, abort, jsonify
from quests.utils import change_config, get_config
from quests.utils.paths_names import util_assignments, auth_token as token


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
        fh = logging.FileHandler('spam.log')
        fh.setLevel(logging.DEBUG)
        logger = logging.getLogger(__name__)
        try:
            json_data = request.get_json(force=True)
            logger.info(str(json_data))
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

                logger.info('Received Assignment')
                if json_data['method'].lower() == 'get':
                    response = requests.post(json_data['resource'], headers=get_config()[token], data=json_data['data'])
                elif json_data['method'].lower() == 'post':
                    response = requests.post(json_data['resource'], headers=get_config()[token], data=json_data['data'])
                else:
                    return abort(400)

                logger.info(str(response))
                if response.status_code == 200:
                    answer = {
                        'id': json_data['id'],
                        'task': json_data['task'],
                        'resource': json_data['resource'],
                        'method': json_data['method'],
                        'data': response,
                        'user': get_config()['username'],
                        'message': 'Swifty swooty as ever has Heroy done his job. Ez pz'
                    }
                    requests.post(json_data['callback'], data=answer)
                else:
                    return jsonify({"message": "That didnt go well duh"})
            else:
                logger.info('Nope Assignment')
                return abort(400)
        except KeyError or TypeError:
            logger.info('Ney Assignment')
            return abort(400)