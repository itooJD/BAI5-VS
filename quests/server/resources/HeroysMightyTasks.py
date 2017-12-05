import requests, json
from flask_restful import Resource
from flask import request, abort, jsonify
from quests.utils import change_config, get_config
from quests.utils.assignment_solver import solve_assignment
from quests.utils.paths_names import util_assignments
from quests.utils import paths_util


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
                solve_assignment(json_data, request.remote_addr)
            else:
                return abort(400)
        except KeyError or TypeError:
            return abort(400)
