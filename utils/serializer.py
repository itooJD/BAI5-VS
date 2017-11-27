import pickle, os


def serialize(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb+') as file:
        pickle.dump(data, file)


def de_serialize(path):
    if os.path.exists(path):
        with open(path, 'rb') as file:
            return pickle.load(file)
    else:
        raise AttributeError
