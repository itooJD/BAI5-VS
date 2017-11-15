from quest2.util import hero_url, taverna_url
import requests


class Taverna():
    def register(self):
        payload = {
            'heroclass': 'Treasure Goblin',
            'capabilities': [],
            'url': hero_url
        }
        response = requests.post(taverna_url, data=payload)