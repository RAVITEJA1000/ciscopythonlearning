
import db_json as db

file_name = 'flights.json'
flights = db.read_from_file(file_name)  # List of dicts: [{'id':id, 'number':number, 'airline_name':airline_name, 'seats':seats, 'price':price, 'source':source, 'destination':destination}, ...]

def create_flight(flight):
    global flights
    flights.append(flight)
    db.write_to_file(flights, file_name)

def read_all_flights():
    return flights

def read_by_id(id):
    for flight in flights:
        if flight['id'] == id:
            return flight
    return None

def update(id, new_flight):
    global flights
    index = 0
    for flight in flights:
        if flight['id'] == id:
            flights[index] = new_flight
            db.write_to_file(flights, file_name)
            break
        index += 1

def delete_flight(id):
    global flights
    index = -1
    i = 0
    for flight in flights:
        if flight['id'] == id:
            index = i
            break
        i += 1
    if index != -1:
        flights.pop(index)
        db.write_to_file(flights, file_name)
