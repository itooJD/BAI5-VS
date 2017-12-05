from flask_restful import Resource
from flask import request, abort, jsonify
from quests.utils import election_algorithm, get_config
from quests.utils.paths_names import util_user


class HeroyPresident(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        # try:
        config = get_config()
        print(json_data)

        election_data = {
            "algorithm": json_data['algorithm'],
            "payload": config[util_user],
            "user": "user_uri",
            "job": json_data['job'],
            "message": "hello you there?"
        }
        print(election_data)
        election_algorithm(election_data)

        return jsonify({"message": "OK"})
        # except Exception as ex:
        #    print(ex)
        #    return abort(400)
