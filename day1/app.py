
import repo
def menu():
    message = '''
Options are:
1 - Create Employee
2 - List All Employee
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

        employee = (id, name, age, salary, is_active)

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
            print('Employee not found')
        else:
            print(employee)
        
    elif choice == 4:
        id = int(input('ID:'))
        employee = repo.read_by_id(id)
        if employee == None:
            print('Employee not found')
        else:
            print(employee)
            salary = float(input('Update New Salary:'))
            new_employee = (employee[0], employee[1], employee[2], salary, employee[4])
            repo.update(id, new_employee)
            print('Employee updated successfully')

    elif choice == 5:
        id = int(input('ID:'))
        employee = repo.read_by_id(id)
        if employee == None:
            print('Employee not found')
        else:
            repo.delete_employee(id)
            print('employee deleted successfully')

    elif choice == 6:
        print('Thank You for using Application')

    return choice

def menus():
    choice = menu()
    while choice != 6:
        choice = menu()

menus()
