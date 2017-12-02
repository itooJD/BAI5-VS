import requests
from flask_restful import Resource, reqparse
from flask import request, abort, jsonify
from quests.utils import change_config, get_config, add_to
from quests.utils.paths_names import util_assignments, util_recv_tokens


# Post assignments
class HeroysCallMeMaybeBack(Resource):
    def get(self):
        # depending if we want to save the data locally or not

        json_data = request.get_json(force=True)
        try:
            if bool(json_data) and len(json_data) == 1 and json_data['heroy'] == 'user':
                return jsonify(get_config()[util_assignments])
            else:
                return jsonify({"message": "what do you want, unworthy scum"})
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
                    "user": json_data['user'],
                    "message": json_data['message']
                })
                add_to(util_recv_tokens, json_data['data'])
                print('Token received: ' +  json_data['data'])
                return jsonify({"message": "thats all?"}), 200
            else:
                return abort(400)
        except KeyError or TypeError:
            return abort(400)
