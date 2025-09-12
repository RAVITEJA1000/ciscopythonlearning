
import db_pickle as db

file_name = 'flights.pkl'
flights = db.read_from_file(file_name)

def create_flight(flight):
    global flights
    flights.append(flight)
    db.write_to_file(flights, file_name)

def read_all_flights():
    return flights

def read_flight_by_id(flight_id):
    return next((f for f in flights if f['id'] == flight_id), None)

def update_flight(flight_id, updated_flight):
    global flights
    for i, flight in enumerate(flights):
        if flight['id'] == flight_id:
            flights[i] = updated_flight
            db.write_to_file(flights, file_name)
            break

def delete_flight(flight_id):
    global flights
    flights = [f for f in flights if f['id'] != flight_id]
    db.write_to_file(flights, file_name)
