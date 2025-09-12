
import pickle
flight = {'flight_number': 'I1700', 'airline ' : 'Indigo','capacity ':225, 'price':4500, 'source ': 'Banglore',
          'destination':'Hyderabad'},

file_name = 'flight.dat'
print('Before file: ',flight)

with open(file_name,'wb') as writer:
    pickle.dump(flight,writer)
    print("Saved the Flight to file")

with open(file_name,'rb') as reader:
    flight_from_file = pickle.load(reader)
    print("Flight after read from file: ",flight_from_file)
