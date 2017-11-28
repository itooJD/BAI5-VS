from flask import jsonify, request
from flask_restful import Resource, abort
from quests.utils import get_config


class Heroy(Resource):
    def __init__(self):
        self.idle = False

    def get(self):
        paths = get_config()
        return jsonify({
            "user": paths['hero_url'],
            "idle": self.idle,
            "group": paths['group_uri'],
            "hirings": paths['hero_url'],
            "assignments": paths['hero_url'] + paths['assignment_url'],
            "messages": paths['hero_url'] + paths['diary_url']
        })

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data['quest'] or not json_data['group'] or not json_data['message']:
            abort(400)

        take_quest = ''
        while take_quest != 'y' and take_quest != 'n':
            take_quest = input(
                "Do you want to take part in the quest: {0} of the group {1}. Message: {2}. Answer with [y,n]".format(
                    json_data['quest'], json_data['group'], json_data['message']))
        if take_quest == "y":
            get_config()['quests'].append((json_data['quest'], json_data['group'], json_data['message']))
            return 201
        else:
            return jsonify({'message': 'Mighty heroy jenkins does not take your pity quest'}), 400
