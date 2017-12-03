from flask_restful import Resource
from flask import request, abort
import requests, json


class HeroyPresident(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        try:
            print(json_data['algorithm'])
            print(json_data['payload'])
            print(json_data['user'])
            print(json_data['job'])
            print(json_data['message'])

            # start_thread:
            #   if group_members > self:
            #       send election

            return 200
        except Exception as ex:
            return abort(400)