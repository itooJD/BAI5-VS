import requests
from quests.utils import get_config


def logout(_):
    exit_check(True)


def exit_check(exit):
    if exit:
        raise Exception('Exiting')


def divide_line():
    print()
    print('#################################')