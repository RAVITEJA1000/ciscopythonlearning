import pickle
import os

def read_from_file(filename='flights.pkl'):
    if not os.path.exists(filename):
        return []
    with open(filename, 'rb') as file:
        return pickle.load(file)

def write_to_file(data, filename='flights.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)