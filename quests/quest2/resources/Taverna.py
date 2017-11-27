import requests
from quests.utils import get_config


class Taverna():
    def register(self):
        payload = {
            'heroclass': 'Treasure Goblin',
            'capabilities': [],
            'url': get_config()['hero_url']
        }
        response = requests.post(get_config()['taverna_url'], data=payload)