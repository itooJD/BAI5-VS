from flask_restful import Resource,  reqparse
from flask import request, abort
import requests, json


class HeroyPresident(Resource):
    def post(self):
        json_data = request.get_json(force=True)


        if not json_data['algorithm'] or not json_data['payload'] or not json_data['user'] or not json_data['job']:
            abort(400)

        print('Received the following message for election: ' + json_data['message'])
        if json_data['algorithm'].lower() == 'bully':
            payload = {'message': 'OK'}
            requests.post(json_data['user'], payload)
            # Send "OK" back
            payload = self.handle_quest(json_data['job'])
            '''
                {
                    "algorithm": "<name of the algorithm used>",
                    "payload": "<the payload for the current state of the algorithm>",
                    "user": "<uri of the user sending this request>",
                    "job": "<JSON description of the job to do>",
                    "message": "<something you want to tell the other one>"
                }
            '''
            requests.post(json_data['user'], payload)


    def handle_quest(self, job):
        pass


        '''
        {
            "id": "<some identity choosen by the initiator to identify this request>",
            "task": "<uri to the task to accomplish>",
            "resource": "<uri or url to resource where actions are required>",
            "method": "<method to take – if already known>",
            "data": "<data to use/post for the task>",
            "callback": "<an url where the initiator can be reached with the results/token>",
            "message": "<something you want to tell the other one>"
        }
        '''