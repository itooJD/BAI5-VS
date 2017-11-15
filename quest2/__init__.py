from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from quest2.resources import HelloToHeroysWorld, HeroyJenkins, HeroysDiary, HeroysMightyTasks, HeroyPresident
from quest2.util import hero_url, assignment_url, diary_url, election_url

api.add_resource(HelloToHeroysWorld, '/')
api.add_resource(HeroyJenkins, hero_url)
api.add_resource(HeroysDiary, hero_url + diary_url)
api.add_resource(HeroysMightyTasks, hero_url + assignment_url)
api.add_resource(HeroyPresident, hero_url + election_url)