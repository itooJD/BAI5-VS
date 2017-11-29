import requests
from quests.quest1.utilities import divide_line, logout
from quests.utils import paths_util, get_config

'''
"/taverna/adventurers": {"get": {
    "description": "<br/>Subscribe yourself with<br/>{<br/>  \"heroclass\":\"<class>\",<br/>  \"capabilities\":\"<your earned capabilities>\",<br/>  \"url\":\"<the full url where one might reach you>\"<br/>}",
    "responses": {}, "summary": "The list of adventurerer known to the local taverna", "tags": ["adventurer"]},
                         "post": {
                             "description": "<br/>Subscribe yourself with<br/>{<br/>  \"heroclass\":\"<class>\",<br/>  \"capabilities\":\"<your earned capabilities>\",<br/>  \"url\":\"<the full url where one might reach you>\"<br/>}",
                             "responses": {}, "summary": "The list of adventurerer known to the local taverna",
                             "tags": ["adventurer"]}}, 
"/taverna/adventurers/{name}": {
    "delete": {"description": "", "responses": {}, "summary": "Details about a single adventurer",
               "tags": ["adventurer"]},
    "get": {"description": "", "responses": {}, "summary": "Details about a single adventurer", "tags": ["adventurer"]},
    "put": {"description": "", "responses": {}, "summary": "Details about a single adventurer",
            "tags": ["adventurer"]}}, 
"/taverna/groups": {
    "get": {
    "description": "<br/>The guy creating a group is the owner of the group.<br/>He does NOT automatically join it!<br/>Only the owner can disband a group, but the member may leave individualy<br/><br/>Just do a post with empty data to create a new group (watch the Location header)",
    "responses": {}, "summary": "Groups formed out of adventurer which want to solve something together.",
    "tags": ["Group"]}, 
    "post": {
    "description": "<br/>The guy creating a group is the owner of the group.<br/>He does NOT automatically join it!<br/>Only the owner can disband a group, but the member may leave individualy<br/><br/>Just do a post with empty data to create a new group (watch the Location header)",
    "responses": {}, "summary": "Groups formed out of adventurer which want to solve something together.",
    "tags": ["Group"]}}, 
"/taverna/groups/{id}": {"delete": {
    "description": "<br/>The guy creating a group is the owner of the group.<br/>He does NOT automatically join it!<br/>Only the owner can disband a group, but the member may leave individualy<br/>",
    "responses": {}, "summary": "Information about a single group", "tags": ["Group"]}, "get": {
    "description": "<br/>The guy creating a group is the owner of the group.<br/>He does NOT automatically join it!<br/>Only the owner can disband a group, but the member may leave individualy<br/>",
    "responses": {}, "summary": "Information about a single group",
    "tags": ["Group"]}}, 
"/taverna/groups/{id}/members": {
    "get": {"description": "<br/>To join just post to join the group", "responses": {},
            "summary": "The members of a group", "tags": ["Group"]},
    "post": {"description": "<br/>To join just post to join the group", "responses": {},
             "summary": "The members of a group", "tags": ["Group"]}},
'''

def taverna_ui(auth_header):
    print('\nTaverna')
    print('1: Adventurers')
    print('2: Groups')
    print('else to go back')
    return taverna_filter(input('Which is more interesting do you think? \n> '), auth_header)


def taverna_filter(choice, auth_header):
    choice_filter = {
        '1': taverna,
        '2': show_groups
    }
    if not choice_filter.get(choice):
        logout('')
    return choice_filter.get(choice)(auth_header), ''


def adventurer_ui(auth_header):
    print('\nWelcome, this is the place of the adventurers!')
    print('1: Look at the list behind the bar')
    print('2: Searching for someone?')
    print('Else: Get outta here')
    return adventurer_filter(input('Which list do you want to see: \n> '), auth_header)


def adventurer_filter(choice, auth_header):
    choice_filter = {
        '1': show_adventurers,
        '2': search_for_adventurer
    }
    if not choice_filter.get(choice):
        logout('')
    return choice_filter.get(choice)(auth_header), ''


def taverna(auth_header):
    # Entering the Taverna
    divide_line()
    print('So you are a juggernaut huh? And I can reach you at 172.19.0.13:5000/heroyjenkins? Weird address, well have fun.')
    adventurer_data = '{"heroclass":"juggernaut","capabilities":"","url":"172.19.0.13:5000/heroyjenkins"}'
    requests.post(paths_util.adventurers_uri(), headers=auth_header, data=adventurer_data)
    print('\nYou enter the dusty taverna')
    in_taverna = True
    while in_taverna:
        in_taverna = adventurer_ui(auth_header)
    print('Leaving the taverna')


def search_ui(auth_header, name):
    print('And what do you want to do with ' + name + '?')
    print('1: Look real close! Get all the details.')
    print('2: I dont like, so I change!')
    print('3: Kill.')
    return search_adv_filter(input('Hm? Tell me. \n> '), auth_header, name)


def search_adv_filter(choice, auth_header, name):
    choice_filter = {
        '1': get_adventurer,
        '2': change_adventurer,
        '3': kill_adventurer
    }
    if not choice_filter.get(choice):
        logout('')
    return choice_filter.get(choice)(auth_header, name), ''


def show_adventurers(auth_header):
    response = requests.get(paths_util.adventurers_uri(), headers=auth_header)
    for adventurer in response.json()['objects']:
        print(adventurer['heroclass'] + ' | ' + adventurer['user'] + ' | ' + adventurer['capabilities'] + ' | ' + adventurer['url'])


def get_adventurer(auth_header, name):
    response = requests.get(paths_util.adventurer(name), headers=auth_header)
    print(response)


def change_adventurer(auth_header, name):
    response = requests.put(paths_util.adventurer(name), headers=auth_header)
    print(response)


def kill_adventurer(auth_header, name):
    response = requests.delete(paths_util.adventurer(name), headers=auth_header)
    print(response)


def search_for_adventurer(auth_header):
    name = input('So.. Whom then?')


def show_groups():
    pass