import json
import os

def read_from_file(filename='db.json'):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as reader:
        data = json.load(reader)
        return data

def write_to_file(data, filename='db.json'):
    with open(filename, 'w') as writer:
        json.dump(data, writer, indent=4)