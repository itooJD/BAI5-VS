from flask import Flask
from flask_restful import Api


def setup_flask():
    app = Flask(__name__)
    api = Api(app)
    return app, api

from quests.quest2.resources import HelloToHeroysWorld, HeroyJenkins, HeroysDiary, HeroysMightyTasks, HeroyPresident

def add_api(paths, api):
    api.add_resource(HeroyJenkins, paths['hero_url'])
    api.add_resource(HeroysDiary, paths['diary_url'])
    api.add_resource(HeroysMightyTasks, paths['assignment_url'])
    api.add_resource(HeroyPresident, paths['election_url'])
