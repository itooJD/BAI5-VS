from cProfile import label

from flask import jsonify, request, abort
from flask_restful import Resource

from quests.utils import get_config, change_config


class TheFake(Resource):
    states = ['released', 'wanting', 'held']

    def get(self):
        response = {
            'state': 'released',
            'time': 0
        }
        return jsonify(response)

    def post(self):
        response = {
            'msg': 'reply-ok',
            'time': 0
        }
        return jsonify(response)
