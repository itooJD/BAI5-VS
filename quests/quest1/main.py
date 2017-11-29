from quests.utils.config_manager import set_server_url_via_udp
from quests.quest1.ui import main_ui
from quests.quest1.user import authentication, whoami
from quests.quest1.utilities import exit_check, divide_line
from quests.utils import get_config
from quests.utils.paths_util import auth_token as token


def main():
    divide_line()
    if get_config()['server'] != '':
        research = input('Do you want to research for the blackboard host? [y] \n> ')
        if research == 'y':
            paths = set_server_url_via_udp()
        else:
            paths = get_config()
    else:
        paths = set_server_url_via_udp()

    # Authentication
    if get_config()[token] != '':
        print('You are already logged in!')
        auth_header = get_config()[token]
        whoami(paths, auth_header)
        divide_line()
    else:
        user_authenticated = False
        while not user_authenticated:
            exit, auth_header = authentication()
            exit_check(exit)
            user_authenticated = whoami(paths, auth_header)
        print()
    print('Authentication Token: ' + str(auth_header))
    divide_line()
    while True:
        main_ui(auth_header)


if __name__ == '__main__':
    main()