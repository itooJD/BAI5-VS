from flask import request
from flask_restful import Resource


class HeroysDiary(Resource):
    diary = []

    def post(self):
        json_data = request.get_json(force=True)
        self.diary.append(json_data['message'])
        return "Send a message in a boooottle yeaah", 200

    def get(self):
        return "All messages: \n" + str(self.diary), 200