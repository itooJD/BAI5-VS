from flask import jsonify, request, abort
from flask_restful import Resource


class HeroysMutex(Resource):
    states = ['released', 'wanting', 'held']

    def __init__(self):
        self.lamport_clock = 0
        self.state = self.states[0]

    def get(self):
        response = {
            'state': self.state,
            'time': self.lamport_clock
        }
        return jsonify(response)

    def post(self):
        json_data = request.get_json(force=True)
        self.lamport_clock += 1
        try:
            if bool(json_data) and len(json_data) == 2:
                if self.state == 'released':
                    message = 'reply-ok'
                elif self.state == 'wanting':
                    if json_data['time'] < self.lamport_clock:
                        while self.state == 'wanting':
                            print('lulz')
                    message = 'reply-ok'
                elif self.state == 'held':
                    while self.state == 'held':
                        print('lulz')
                    message = 'reply-ok'
                response = {
                    'msg': message,
                    'time': self.lamport_clock
                }
                return jsonify(response)
            else:
                return abort(400)
        except KeyError:
            return abort(400)

    def put(self):
        json_data = request.get_json(force=True)
        try:
            message = 'update unsuccessful, {state:' + str(self.state) + ',clock:' + str(self.lamport_clock)
            if bool(json_data) and len(json_data) == 2:
                if json_data['message'] == 'state' and json_data['state'] in self.states:
                    self.state = json_data['state']
                    message = 'successfully update state to ' + str(self.state)
                if json_data['message'] == 'clock':
                    self.lamport_clock += 1
                    message = 'sucessufully update clock to ' + str(self.lamport_clock)
            response = {'msg': message}
            return jsonify(response)
        except KeyError:
            return abort(400)
