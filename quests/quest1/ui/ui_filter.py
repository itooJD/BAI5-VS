from quests.quest1.questing import search_location
from quests.quest1.blackboard import show_users, show_all_quests, show_available_quests, choose_quest
from quests.quest1.utilities import logout


def main_filter(choice, auth_header):
    choice_filter = {
        '1': choose_quest,
        '3': show_users,
        '4': search_location,
        '5': logout
    }
    return choice_filter.get(choice)(auth_header)


def quest_filter(choice, auth_header):
    choice_filter = {
        '1': show_available_quests,
        '2': show_all_quests
    }
    return choice_filter.get(choice)(auth_header)