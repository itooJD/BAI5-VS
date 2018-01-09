if __name__ == '__main__':
    answer = input('Do you want to start the flask server [1] or the ui [2]? \n > ')
    if answer == '1':
        from quests.server.server_setup import setup_flask, add_api
        from quests.utils import set_server_url_via_udp
        print('Setup: Setting server url')
        paths = set_server_url_via_udp()
        print('Setup: Configuring flask-server')
        app, api = setup_flask()
        print('Setup: Adding Rest-API')
        add_api(paths, api)
        print('Setup: Starting flask-server')
        app.run(host='172.19.0.78', debug=False)
    elif answer == '2':
        print('Setup: Starting UI')
        from quests.client import main
        main.main()
    else:
        print('Exiting')