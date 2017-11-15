from flask_restful import Resource,  reqparse
import requests, json


class HeroyPresident(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('algorithm', required=True, location='args')
        parser.add_argument('payload', required=True, location='args')
        parser.add_argument('user', required=True, location='args')
        parser.add_argument('job', required=True, location='args')
        parser.add_argument('message', required=True, location='args')
        '''
        {
            "algorithm": "<name of the algorithm used>",
            "payload": "<the payload for the current state of the algorithm>",
            "user": "<uri of the user sending this request>",
            "job": "<JSON description of the job to do>",
            "message": "<something you want to tell the other one>"
        }
        '''
        args = parser.parse_args()
        job_json = json.loads(args['job'])
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