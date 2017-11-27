from flask_restful import Resource, reqparse
from utils.config_manager import get_config
import requests


# Post assignments
class HeroysMightyTasks(Resource):
    assignments = []

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, location='args')
        parser.add_argument('task', required=True, location='args')
        parser.add_argument('resource', required=True, location='args')
        parser.add_argument('method', required=True, location='args')
        parser.add_argument('data', required=True, location='args')
        parser.add_argument('callback', required=True, location='args')
        parser.add_argument('message', required=True, location='args')
        args = parser.parse_args()

        self.assignments.append(
            {
                'id': args['id'],
                'task': args['task']
            }
        )

        task = {
            "id": "<some identity chosen by the initiator to identify this request>",
            "task": "<uri to the task to accomplish>",
            "resource": "<uri or url to resource where actions are required>",
            "method": "<method to take – if already known>",
            "data": "<data to use/post for the task>",
            "callback": "<an url where the initiator can be reached with the results/token>",
            "message": "<something you want to tell the other one>"
        }
        response = requests.post(args['resource'], data=task)
        if response.status_code == 200:
            answer = {
                'id': args['id'],
                'task': args['task'],
                'resource': args['resource'],
                'method': '<method used to get this result>',
                'data': response.text,
                'user': get_config()['hero_url'],
                'message': 'Swifty swooty as ever has heroy done his job'
            }
            requests.post(args['callback'], data=answer)
            return '', 200
        else:
            return '', 400

    def get_mighty_tasks(self):
        return self.assignments
