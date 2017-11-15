from flask_restful import Resource


class HelloToHeroysWorld(Resource):
    def get(self):
        return {'Hey': 'There'}, 200