from flask_restful import Resource,  reqparse


class HeroysDiary(Resource):
    diary = []

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', required=True, location='args',
                            help='Please provide a message')
        args = parser.parse_args()
        print(args['message'])
        self.diary.append(args['message'])

    def get(self):
        return 200, str(self.diary)