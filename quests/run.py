
def flask_run(app):
    app.run(host='0.0.0.0', debug=False)

if __name__ == '__main__':
    from quests.quest2.server_setup import setup_flask, add_api
    from quests.utils import set_server_url_via_udp
    from threading import Thread
    print('Setup: Setting server url')
    paths = set_server_url_via_udp()
    print('Setup: Configuring flask-server')
    app, api = setup_flask()
    print('Setup: Adding Rest-API')
    add_api(paths, api)
    print('Setup: Starting flask-server')
    thread = Thread(target=flask_run, args=(app,))
    thread.start()
    print('Setup: Starting UI')
    from quests.quest1 import quest1
    thread.join()
