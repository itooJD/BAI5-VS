from quests.utils.config_manager import set_server_url_via_udp
from quests.quest1.ui import main_ui
from quests.quest1.user import authentication, whoami
from quests.quest1.utilities import exit_check, divide_line


def main():
    divide_line()
    paths = set_server_url_via_udp()

    # Authentication
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