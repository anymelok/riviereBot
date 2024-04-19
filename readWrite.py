import json

def writeJSON(file, object):
    with open(file, 'w') as f:
        f.writelines(json.dumps(object))


def readJSON(file):
    with open(file, 'r') as f:
        return json.load(f)

