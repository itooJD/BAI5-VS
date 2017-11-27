from flask import jsonify, request
from flask_restful import Resource, abort
from utils import serializer as ser, paths, get_config


class HeroyJenkins(Resource):
    def __init__(self):
        self.idle = False

    def get(self):
        try:
            group_uri = ser.de_serialize(paths.group_link_file)
        except AttributeError:
            group_uri = ''


        return jsonify({
            "user": get_config()['hero_url'],
            "idle": self.idle,
            "group": get_config()['group_uri'],
            "hirings": get_config()['hero_url'],
            "assignments": get_config()['hero_url'] + get_config()['assignment_url'],
            "messages": get_config()['hero_url'] + get_config()['diary_url']
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
