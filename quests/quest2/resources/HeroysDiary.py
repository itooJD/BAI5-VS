from flask import request, abort
from flask_restful import Resource
from quests.utils import add_to
from quests.utils.paths_names import util_recv_messages


class HeroysDiary(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data['message']:
            abort(400)
        add_to(util_recv_messages,json_data['message'])
        print('Received: ' + str(json_data))
        return "Sent a message in a boooottle yeaah", 200