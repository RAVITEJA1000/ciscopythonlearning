import repo_inmem_dict as repo

def menu():
    message = '''
Options are:
1 - Create Employee
2 - List All Employees
3 - Read Employee By Id
4 - Update Employee
5 - Delete Employee
6 - Exit 
Your Option:'''
    choice = int(input(message))
    if choice == 1:
        id = int(input('ID:'))
        name = input('Name:')
        age = int(input('Age:'))
        salary = float(input('Salary:'))
        is_active = (input('Active(y/n):').upper() == 'Y')

        employee = {'id':id, 'name':name, 'age':age, 
                    'salary':salary, 'is_active':is_active}

        repo.create_employee(employee)

        print('Employee Created Successfully.')
    elif choice == 2:
        print('List of Employees:')
        for employee in repo.read_all_employee():
            print(employee)
    elif choice == 3:
        id = int(input('ID:'))
        employee = repo.read_by_id(id)
        if employee == None:
            print('Employee not found.')
        else:
            print(employee)
    elif choice == 4:
        id = int(input('ID:'))
        employee = repo.read_by_id(id)
        if employee == None: 
            print('Employee Not Found')
        else:
            print(employee)
            salary = float(input('New Salary:'))
            new_employee = {'id':employee['id'], 
                'name':employee['name'], 
                'age':employee['age'], 
                'salary':salary, 
                'is_active':employee['is_active']}
            repo.update(id, new_employee)
            print('Employee updated successfully.')
    elif choice == 5:
        id = int(input('ID:'))
        employee = repo.read_by_id(id)
        if employee == None: 
            print('Employee Not Found')
        else:
            repo.delete_employee(id)
            print('Employee Deleted Succesfully.')
    elif choice == 6: 
        print('Thank you for using Application')

    return choice 

def menus():
    choice = menu()
    while choice != 6:
        choice = menu()
    
menus()