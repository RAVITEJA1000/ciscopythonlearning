
import db_pickle as db 
#CRUD (Create, Read All | Read One, Update, Delete)
#Employee App - Pickle Binary Persisten Storage (DB) - dict element
file_name = 'employees.dat' 
employees = db.read_from_file(file_name) #[] # [{'id':id,'name':name,'age':age,'salary':salary,'is_active':is_active}, ...]

def create_employee(employee):
    global employees 
    employees.append(employee)
    db.write_to_file(employees, file_name)

def read_all_employee():
    return employees 

def read_by_id(id):
    for employee in employees:
        if employee['id'] == id:
            return employee 
    return None 

def update(id, new_employee):#new_employee is update at id
    global employees
    I = 0
    for employee in employees:
        if employee['id'] == id:
            employees[I] = new_employee
            db.write_to_file(employees, file_name)
            break 
        I += 1
    
def delete_employee(id):
    global employees
    index = -1
    I = 0
    for employee in employees:
        if employee['id'] == id:
            index = I
            break 
        I += 1
    if index != -1:
        employees.pop(index)
        db.write_to_file(employees, file_name)
