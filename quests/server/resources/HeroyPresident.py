from flask_restful import Resource
from threading import Thread
from flask import request, abort, jsonify
from quests.utils import election_algorithm, get_config
from quests.utils.paths_names import util_user


class HeroyPresident(Resource):
    def post(self):
        json_data = request.get_json(force=True)

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
        thread = Thread(target=election_algorithm, args=(election_data,))
        thread.start()
        return jsonify({"message": "OK"})