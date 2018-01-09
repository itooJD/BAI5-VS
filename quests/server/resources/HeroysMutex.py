import requests
from flask import jsonify, request, abort, json
from flask_restful import Resource
from quests.utils import get_config, change_config, add_to


class HeroysMutex(Resource):
    states = ['released', 'wanting', 'held']

    def get(self):
        config = get_config()
        response = {
            'state': config['state'],
            'time': config['lamport_clock']
        }
        return jsonify(response)

    def post(self):
        print('Received mutex request')
        json_data = request.get_json(force=True)
        print('JsonData')
        config = get_config()
        state = config['state']
        lamport_clock = config['lamport_clock']
        stored_requests = config['stored_requests']
        waiting_answers = config['waiting_answers']
        print('Stored')
        try:
            if json_data['msg'].lower() == 'reply-ok' and len(json_data) == 4:
                print('Reply-OK')
                if json_data['user'] in waiting_answers:
                    waiting_answers.remove(json_data['user'])
                change_config('waiting_answers', waiting_answers)
                return 200
            elif json_data['msg'].lower() == 'request' and len(json_data) == 4:
                print('Received mutex request')
                if state == 'released' or (state == 'wanting' and json_data['lamport_clock'] >= lamport_clock):
                    message = 'reply-ok'
                else:
                    stored_requests.append(json_data['reply'])
                    message = 'request'
            else:
                print(str(json_data))
                return abort(400)

            if json_data['time'] > lamport_clock:
                lamport_clock = json_data['time']
            lamport_clock += 1

            response = {
                'msg': message,
                'time': lamport_clock,
                'user': 'http://' + config['own_address'] + ':5000/',
                'reply': 'http://' + config['own_address'] + ':5000' + config['mutex_url']
            }

            change_config('stored_requests', stored_requests)
            change_config('lamport_clock', lamport_clock)
            return jsonify(response)
        except KeyError or TypeError as e:
            print('Error working on Mutex post: ' + str(e))
            return abort(400)
