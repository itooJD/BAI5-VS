from flask import Flask
from flask_restful import Api
from quests.server.resources import *


def setup_flask():
    app = Flask(__name__)
    api = Api(app)
    return app, api


def add_api(paths, api):
    api.add_resource(Heroy, paths['hero_url'])
    api.add_resource(HeroysDiary, paths['diary_url'])
    api.add_resource(HeroysMightyTasks, paths['assignment_url'])
    api.add_resource(HeroyPresident, paths['election_url'])
    api.add_resource(HeroysCallMeMaybeBack, paths['callback_url'])
    #api.add_resource(HeroysMutex, '/path') # must do
    #api.add_resource(TheFake, '/mutex')
