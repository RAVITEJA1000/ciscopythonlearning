
employees = []

def create_employee(employee):
    global employees
    employees.append(employee)

def read_all_employee():
    return employees

def read_by_id(id):
    for employee in employees:
        if employee[0] == id:
            return employee
    return None

def update(id, new_employee):
    global employees
    i = 0
    for employee in employees:
        if employee[0] == id:
            employees[i] = new_employee
            break
        i += 1

def delete_employee(id):
    global employees
    index = -1
    i = 0
    for employee in employees:
        if employee[0] == id:
            index = i
            break
        i += 1
    if index != 1:
        employees.pop(index)
