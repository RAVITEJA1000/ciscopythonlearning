
#1. testing the repo.py
#from repo import create_employee, read_all_employee, read_by_id
#from repo import update, delete_employee
import repo

employee =('John', 21, 10000, True)
repo.create_employee(employee)
print(f'Employee {employee[1]} created successfully')
print('After add:', repo.read_all_employee())

employee =('Doe', 22, 20000, True)
repo.create_employee(employee)
print(f'Employee {employee[1]} created successfully')
print('After add:', repo.read_all_employee())

employee = repo.read_by_id(103)
if employee == None:
    print('Employee not found')
else:
    print(employee)

employee = repo.read_by_id(103)
if employee == None:
    print('Employee not found')
else:
    id, name, age, salary, is_active = employee
    salary += 10000
    new_employee = (id, name, age, salary, is_active)
    repo.update(103, new_employee)
    print('After update:', repo.read_all_employee())

repo.delete_employee(102)
print('After delete:', repo.read_all_employee())


#2. make as app
