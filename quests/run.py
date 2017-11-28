
if __name__ == '__main__':
    from .quest2.server_setup import setup_flask, add_api
    from .utils import set_server_url_via_udp
    from threading import Thread
    print('Setup: Setting server url')
    paths = set_server_url_via_udp()
    print('Setup: Configuring flask-server')
    app, api = setup_flask()
    print('Setup: Adding Rest-API')
    add_api(paths, api)
    print('Setup: Starting flask-server')
    thread = Thread(app.run(host='0.0.0.0', debug=True))
    thread.start()
    print('Setup: Starting UI')
    from .quest1 import quest1
    thread.join()
