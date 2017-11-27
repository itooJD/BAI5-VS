import requests

from utils import paths, serializer as ser


def game_map(auth_header, quest, tokens_id, tokens):
    choice_map, locations = map(requests.get(paths.map, headers=auth_header))
    if choice_map in locations:
        questing = True
        while questing:
            location = locations[choice_map]
            destination = location[1]
            print('\nEntering ', location[0])
            if bool(quest):
                for key, task in quest['tasks'].items():
                    resources = {}
                    if task['location'] == '/map/' + location[0]:
                        resource = task['resource']
                        resources.update({key: resource})
                        print(key, ': ', resource)
                print('id for given resources')
                print('uri for new path')
                choice_resource = input('where do you want to go: ')
                if choice_resource in resources:
                    destination = destination + resources[choice_resource]
                else:
                    destination = destination + choice_resource
            choice_action = input('what do you want to do (GET/POST/else): ')
            if choice_action in ['GET', 'POST']:
                data = ''
                if input('any data (y/else): ') == 'y':
                    for key, value in tokens_id.items():
                        print(key, ': ', value)
                    id = input('which token to add: ')
                    tokens_temp = '['
                    while id in tokens_id:
                        tokens_temp = tokens_temp + '"' + tokens[tokens_id[id]] + '"'
                        id = input('which token to add (id/else): ')
                        if id in tokens_id:
                            tokens_temp = tokens_temp + ','
                        else:
                            tokens_temp = tokens_temp + ']'
                    data = '{"tokens":' + tokens_temp + '}'
                if choice_action == 'GET':
                    response = requests.get(paths.http(destination), headers=auth_header, data=data)
                elif choice_action == 'POST':
                    response = requests.post(paths.http(destination), headers=auth_header, data=data)
                print()
                if response.status_code in [200, 400]:
                    obj = response.json()
                    try:
                        token_name = obj['token_name']
                        if token_name == '<noname>':
                            token_name = choice_resource
                        if token_name not in tokens:
                            tokens.update({token_name: obj['token']})
                            tokens_id.update({str(len(tokens)): token_name})
                            ser.serialize([tokens_id, tokens], paths.tokens_file)
                    except Exception:
                        print('', end='')
                    for key, value in obj.items():
                        print(key, ': ', value)
                else:
                    print('something went wrong')
            else:
                questing = False
    return tokens_id, tokens


def map(response):
    print('\nMap')
    locations = {}
    objects = response.json()['objects']
    for i in range(len(objects)):
        location = (objects[i]['name'], objects[i]['host'])
        i = str(i + 1)
        locations.update({i: location})
        print('<', i, '> ', location[0])
    print('else to go back')
    return input('Where do you want to go: '), locations
