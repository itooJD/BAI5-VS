from flask import jsonify, request
from flask_restful import Resource, abort
from quests.quest2.util import hero_url, assignment_url, diary_url, quests, election_url
from quests.utils.paths_names import util_group
from quests.utils import get_config


class HeroyJenkins(Resource):
    def __init__(self):
        self.idle = False

    def get(self):
        return jsonify({
            "user": hero_url,
            "idle": self.idle,
            "group": get_config()[util_group],
            "hirings": hero_url,
            "assignments": assignment_url,
            "messages": diary_url,
            "election": election_url
        })

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
