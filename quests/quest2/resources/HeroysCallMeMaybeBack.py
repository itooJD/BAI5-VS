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
                return jsonify({"message": "what do you want, unworthy scum?"})
        except KeyError:
            return abort(400)

    def post(self):
        try:
            json_data = request.get_json(force=True)
            if bool(json_data) and len(json_data) == 7:
                assignment_data ={
                    "id": str(json_data['id']),
                    "task": str(json_data['task']),
                    "resource": str(json_data['resource']),
                    "method": str(json_data['method']),
                    "data": str(json_data['data']),
                    "user": str(json_data['user']),
                    "message": str(json_data['message'])
                }
                change_config(util_assignments, assignment_data)
                print('Received finished assignment: ' + str(assignment_data))
                add_to(util_recv_tokens, json_data['data'])
                print('Token received: ' +  json_data['data'])
                return jsonify({"message": "thats all?"}), 200
            else:
                return abort(400)
        except KeyError or TypeError:
            return abort(400)
