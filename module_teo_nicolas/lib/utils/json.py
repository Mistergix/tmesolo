import json

def encode_json(dico, fname):
    """
    fname : filename with no extension
    """
    with open("jsons/{}.json".format(fname), 'w') as f:
        json.dump(dico, f)

def decode_json(fname):
    """
    fname : filename with no extension
    """
    with open("jsons/{}.json".format(fname), 'r') as f:
        data = json.load(f)

    return data