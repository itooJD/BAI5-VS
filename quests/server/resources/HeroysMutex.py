import requests
from flask import jsonify, request, abort
from flask_restful import Resource

from quests.utils import get_config, change_config


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
        config = get_config()
        lamport_clock = config['lamport_clock']
        state = config['state']
        stored_requests = config['stored_requests']
        remote_addr = request.remote_addr
        try:
            if json_data['msg'] == 'reply-ok' and len(json_data) == 2:
                waiting_answers = config['waiting_answers']
                waiting_answers.remove(remote_addr)
                response = {
                    'msg': 'thanks',
                    'time': lamport_clock
                }
            elif json_data['msg'] == 'request' and len(json_data) == 2:
                waiting_answers = config['waiting_answers']
                if json_data['user'] in waiting_answers:
                    waiting_answers.remove(json_data['user'])
                print('Received mutex request')
                if state == 'released' or (state == 'wanting' and json_data['lamport_clock'] >= lamport_clock):
                    message = 'reply-ok'
                else:
                    if remote_addr not in stored_requests:
                        stored_requests.append(remote_addr)
                        change_config('stored_requests', stored_requests)
                    message = 'request'
                response = {
                    'msg': message,
                    'time': lamport_clock
                }
            else:
                return abort(400)

            if json_data['time'] > lamport_clock:
                lamport_clock = json_data['time']
            lamport_clock += 1
            change_config('lamport_clock', lamport_clock)
            return jsonify(response)
        except KeyError or TypeError as e:
            print('Error working on Mutex post: ' + str(e))
            return abort(400)

    # change status
    # {
    #   "message":"state",
    #   "state":"released" oder....
    # }
    #
    # update clock
    # {
    #   "message":"clock"
    # }
    def put(self):
        json_data = request.get_json(force=True)
        config = get_config()
        lamport_clock = config['lamport_clock']
        state = config['state']
        try:
            message = 'Update unsuccessful, {state:' + str(state) + ',clock:' + str(lamport_clock) + '}'
            if json_data['message'] == 'state' and json_data['state'] in self.states and len(json_data) == 2:
                if json_data['state'] == 'released':
                    if state != 'released':
                        self.answer_stored_requests()
                    change_config('stored_requests', list())
                state = json_data['state']
                change_config('state', state)
                message = 'successfully update state to ' + str(state)
            if json_data['message'] == 'clock' and len(json_data) == 1:
                lamport_clock += 1
                change_config('lamport_clock', lamport_clock)
                message = 'sucessufully update clock to ' + str(lamport_clock)
            response = {'msg': message}
            return jsonify(response)
        except KeyError or TypeError:
            return abort(400)

    def answer_stored_requests(self):
        config = get_config()
        lamport_clock = config['lamport_clock']
        stored_requests = config['stored_requests']
        # in stored_request are only the ip-addresses
        # get adventurer list
        for request in stored_requests:
            data = {
                "msg": "reply-ok",
                "time": lamport_clock
            }
            # get full URL of request from adventurer list
            # send POST to mutex with data
            lamport_clock += 1
        change_config('lamport_clock', lamport_clock)
