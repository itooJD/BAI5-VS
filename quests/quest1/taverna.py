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
            "tags": ["adventurer"]}}, "/taverna/groups": {"get": {
    "description": "<br/>The guy creating a group is the owner of the group.<br/>He does NOT automatically join it!<br/>Only the owner can disband a group, but the member may leave individualy<br/><br/>Just do a post with empty data to create a new group (watch the Location header)",
    "responses": {}, "summary": "Groups formed out of adventurer which want to solve something together.",
    "tags": ["Group"]}, "post": {
    "description": "<br/>The guy creating a group is the owner of the group.<br/>He does NOT automatically join it!<br/>Only the owner can disband a group, but the member may leave individualy<br/><br/>Just do a post with empty data to create a new group (watch the Location header)",
    "responses": {}, "summary": "Groups formed out of adventurer which want to solve something together.",
    "tags": ["Group"]}}, "/taverna/groups/{id}": {"delete": {
    "description": "<br/>The guy creating a group is the owner of the group.<br/>He does NOT automatically join it!<br/>Only the owner can disband a group, but the member may leave individualy<br/>",
    "responses": {}, "summary": "Information about a single group", "tags": ["Group"]}, "get": {
    "description": "<br/>The guy creating a group is the owner of the group.<br/>He does NOT automatically join it!<br/>Only the owner can disband a group, but the member may leave individualy<br/>",
    "responses": {}, "summary": "Information about a single group",
    "tags": ["Group"]}}, "/taverna/groups/{id}/members": {
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
    return taverna_filter(input('Which list do you want to see: \n> '), auth_header)


def taverna_filter(choice, auth_header):
    choice_filter = {
        '1': show_adventurers,
        '2': show_groups
    }
    if not choice_filter.get(choice):
        logout('')
    return choice_filter.get(choice)(auth_header), ''


def taverna(auth_header):
    # Entering the Taverna
    adventurer_data = '{"heroclass":"juggernaut","capabilities":"None","url":"172.19.0.13:5000/heroyjenkins"}'
    requests.post(paths_util.adventurers, headers=auth_header, data=adventurer_data)
    print('\nEntering the Taverna')
    in_taverna = True
    while in_taverna:
        in_taverna = taverna_ui(auth_header)
    print('Leaving the taverna')


def show_adventurers(auth_header):
    response = requests.get(paths_util.adventurers(), headers=auth_header)
    print(response)
    for adventurer in response.json()['objects']:
        print(adventurer)

def show_groups():
    pass