if __name__ == '__main__':
    answer = input('Do you want to start the flask server [1] or the ui [2]? \n > ')
    if answer == '1':
        from quests.quest2.server_setup import setup_flask, add_api
        from quests.utils import set_server_url_via_udp
        print('Setup: Setting server url')
        paths = set_server_url_via_udp()
        print('Setup: Configuring flask-server')
        app, api = setup_flask()
        print('Setup: Adding Rest-API')
        add_api(paths, api)
        print('Setup: Starting flask-server')
        app.run(host='0.0.0.0', debug=False)
    elif answer == '2':
        print('Setup: Starting UI')
        from quests.quest1 import quest1
    else:
        print('Exiting')