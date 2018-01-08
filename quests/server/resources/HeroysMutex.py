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
        json_data = request.get_json(force=True)
        config = get_config()

        # get config informations
        lamport_clock = config['lamport_clock']
        state = config['state']
        stored_requests = config['stored_requests']
        remote_addr = request.remote_addr
        try:
            if bool(json_data) and len(json_data) == 2:
                if state == 'released':
                    message = 'reply-ok'
                elif state == 'wanting':
                    if json_data['time'] < lamport_clock:
                        if remote_addr not in stored_requests:
                            stored_requests.append(remote_addr)
                        message = 'request'
                    else:
                        message = 'reply-ok'
                elif state == 'held':
                    if remote_addr not in stored_requests:
                        stored_requests.append(remote_addr)
                    message = 'request'
                response = {
                    'msg': message,
                    'time': lamport_clock
                }
                return jsonify(response)
            else:
                return abort(400)
        except KeyError:
            return abort(400)

    def put(self):
        json_data = request.get_json(force=True)
        config = get_config()
        lamport_clock = config['lamport_clock']
        state = config['state']
        stored_requests = config['stored_requests']
        try:
            message = 'update unsuccessful, {state:' + str(state) + ',clock:' + str(lamport_clock) + '}'
            if bool(json_data) and len(json_data) == 2:
                if json_data['message'] == 'state' and json_data['state'] in self.states:
                    print('ich bin in der if')
                    if state != 'released' and json_data['state'] == 'released':
                        print('ich bin in der 2. if')
                        self.answer_stored_requests(stored_requests)
                        change_config('stored_reqeuests', list())
                    state = json_data['state']
                    change_config('state', state)
                    message = 'successfully update state to ' + str(state)
                if json_data['message'] == 'clock':
                    lamport_clock += 1
                    change_config('lamport_clock', lamport_clock)
                    message = 'sucessufully update clock to ' + str(lamport_clock)
            response = {'msg': message}
            return jsonify(response)
        except KeyError:
            return abort(400)

    def store_request(self):
        pass

    def answer_stored_requests(self, stored_requests):
        for request in stored_requests:
            print('Answer Request: ' + request)
            requests.post('http://' + request + ':5000/path', data='{"msg":"reply-ok","time":1}')
        pass
