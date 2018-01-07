from cProfile import label

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
        lamport_clock = config['lamport_clock']
        state = config['state']
        addr = request.__getattribute__('connection')
        try:
            if bool(json_data) and len(json_data) == 2:
                if state == 'released':
                    message = 'reply-ok'
                elif state == 'wanting':
                    if json_data['time'] < lamport_clock:
                        self.store_request()

                        ####

                        message = 'request'
                        message = addr
                    else:
                        message = 'reply-ok'
                elif state == 'held':
                    self.store_request()
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
        try:
            message = 'update unsuccessful, {state:' + str(state) + ',clock:' + str(lamport_clock) + '}'
            if bool(json_data) and len(json_data) == 2:
                if json_data['message'] == 'state' and json_data['state'] in self.states:
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
