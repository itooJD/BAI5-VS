server = 'http://172.19.0.3:5000'


def http(uri):
    return 'http://' + uri


def server_uri(uri):
    return server + uri


## blackboard
blackboard = server + '/blackboard'
quests = blackboard + '/quests'

## users
users = server + '/users'

## who am I
whoami = server + '/whoami'

## Taverna
taverna = server + '/taverna'
groups = taverna + '/groups'


def group(id):
    return groups + '/' + id


adventurers = taverna + '/adventurers'


def adventurer(name):
    return adventurers + '/' + name


login = server + '/login'
map = server + '/map'

## file paths
tokens_file = 'data/tokens'
auth_token_file = 'data/auth'
group_link_file = 'data/group'
messages_file = 'data/messages'
quest_file = 'data/quest'
