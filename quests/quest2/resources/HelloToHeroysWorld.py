from flask_restful import Resource
import logging, sys


class HelloToHeroysWorld(Resource):
    logger = ''

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        hdlr = logging.FileHandler('/root/BAI5-VS/logfile.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def get(self):
        print('oh', file=sys.stdout)
        self.logger.info('Received a message')
        return {'Hello': ' there *twinkle'}, 200
