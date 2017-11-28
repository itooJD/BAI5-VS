from quests.quest2.server_setup import setup_flask, add_api
from quests.utils import set_server_url_via_udp
from threading import Thread

if __name__ == '__main__':
    print('Setup: Setting server url')
    paths = set_server_url_via_udp()
    app, api = setup_flask()
    add_api(paths, api)
    print('')
    thread = Thread(app.run(host='0.0.0.0', debug=True))
    thread.start()
    from quests.quest1 import quest1
    thread.join()
