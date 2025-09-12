import flight_repo as repo

def menu():
    message = '''
Options:
1 - Create Flight
2 - List All Flights
3 - Read Flight By ID
4 - Update Flight
5 - Delete Flight
6 - Exit
Your Option: '''
    choice = int(input(message))

    if choice == 1:
        id = int(input('Flight ID: '))
        number = input('Flight Number: ')
        airline_name = input('Airline Name: ')
        seats = int(input('Total Seats: '))
        price = float(input('Ticket Price: '))
        source = input('Source: ')
        destination = input('Destination: ')

        flight = {
            'id': id,
            'number': number,
            'airline_name': airline_name,
            'seats': seats,
            'price': price,
            'source': source,
            'destination': destination
        }

        repo.create_flight(flight)
        print('Flight Created Successfully.')

    elif choice == 2:
        print('\nAll Flights:')
        for flight in repo.read_all_flights():
            print(flight)

    elif choice == 3:
        id = int(input('Flight ID: '))
        flight = repo.read_flight_by_id(id)
        if flight:
            print('Flight Details:', flight)
        else:
            print(' Flight not found.')

    elif choice == 4:
        id = int(input('Flight ID to Update: '))
        flight = repo.read_flight_by_id(id)
        if flight:
            print('Current Data:', flight)
            price = float(input('New Ticket Price: '))
            updated_flight = {
                'id': flight['id'],
                'number': flight['number'],
                'airline_name': flight['airline_name'],
                'seats': flight['seats'],
                'price': price,
                'source': flight['source'],
                'destination': flight['destination']
            }
            repo.update_flight(id, updated_flight)
            print('Flight Updated Successfully.')
        else:
            print('Flight not found.')

    elif choice == 5:
        id = int(input('Flight ID to Delete: '))
        flight = repo.read_flight_by_id(id)
        if flight:
            repo.delete_flight(id)
            print('✅ Flight Deleted Successfully.')
        else:
            print(' Flight not found.')

    elif choice == 6:
        print('👋Thank you for using Flight Management System!')

    return choice

def menus():
    while True:
        if menu() == 6:
            break

menus()