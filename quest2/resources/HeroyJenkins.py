from flask import jsonify
from flask_restful import Resource,  reqparse
from quest2.util import hero_url, assignment_url, diary_url, quests


class HeroyJenkins(Resource):
    def get(self):
        return jsonify({
            "user": hero_url,
            "idle": False,
            "group": "<url to the group you are in>",
            "hirings": hero_url,
            "assignments": hero_url + assignment_url,
            "messages":  hero_url + diary_url
        })

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('group', required=True, location='args',
                            help='Please provide a message')
        parser.add_argument('quest', required=True, location='args')
        parser.add_argument('message', required=True, location='args')
        args = parser.parse_args()
        take_quest = ''
        while take_quest != 'y' and take_quest != 'n':
            take_quest = input("Do you want to take part in the quest: {0} of the group {1}. Message: {2}. Answer with [y,n]".format(args['quest'], args['group'], args['message']))
        if take_quest == "y":
            quests.append((args['quest'], args['group'], args['message']))
            return 201
        else:
            return jsonify({'message':'Mighty heroy jenkins does not take your pity quest'}), 400