if __name__ == '__main__':
    from quests.quest2.server_setup import setup_flask, add_api
    from quests.utils import set_server_url_via_udp
    print('Setup: Setting server url')
    paths = set_server_url_via_udp()
    app, api = setup_flask()
    add_api(paths, api)
    print('')
    app.run(host='0.0.0.0', debug=True)
