from flask import jsonify, request
from flask_restful import Resource, abort
from quests.utils import get_config


class Heroy(Resource):
    def __init__(self):
        self.idle = False

    def get(self):
        config = get_config()
        data = {
            "user": config['hero_url'],
            "idle": True,
            "group": config['group'],
            "hirings": config['hero_url'],
            "assignments": config['assignment_url'],
            "messages": config['diary_url'],
            "election": config['election_url'],
            "mutex": config['mutex_url'],
            "mutexstate": config['mutex_url']
        }
        print(data)
        return jsonify(data)

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data['quest']:
            abort(400)

        take_quest = ''
        while take_quest != 'y' and take_quest != 'n':
            take_quest = input(
                "Do you want to take part in the quest: {0} of the group {1}. Message: {2}. Answer with [y,n]".format(
                    json_data['quest'], json_data['group'], json_data['message']))
        if take_quest == "y":
            quests.append((json_data['quest'], json_data['group'], json_data['message']))
            return 201
        else:
            return jsonify({'message': 'Mighty heroy jenkins does not take your pity quest'}), 400
