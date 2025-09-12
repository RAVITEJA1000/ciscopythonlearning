import pickle 
import os

def read_from_file(filename = 'db.dat'):
    if not os.path.exists(filename):
        employees = []
        return employees 
    
    with open(filename, 'rb') as reader:
        employees = pickle.load(reader)
        return employees 
    
def write_to_file(employees, filename = 'db.dat'):
    with open(filename, 'wb') as writer:
        pickle.dump(employees, writer) 