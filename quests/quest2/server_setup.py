from flask import Flask
from flask_restful import Api

from quests.quest2.resources import *


def setup_flask():
    app = Flask(__name__)
    api = Api(app)
    return app, api


def add_api(paths, api):
    api.add_resource(HelloToHeroysWorld, '/')
    api.add_resource(Heroy, paths['hero_url'])
    api.add_resource(HeroysDiary, paths['hero_url'] + paths['diary_url'])
    api.add_resource(HeroysMightyTasks, paths['hero_url'] + paths['assignment_url'])
    api.add_resource(HeroyPresident, paths['hero_url'] + paths['election_url'])
