from app.models import db, Employee 

def create_employee(employee):
    employee_model = Employee(id = employee['id'],
        name = employee['name'],
        age = employee['age'],
        salary = employee['salary'],
        is_active = employee['is_active'] )
    db.session.add(employee_model) 
    db.session.commit() 

def read_all_employee():
    employees = db.session.query(Employee).all()
    dict_employees = []
    for employee in employees:
        employee_dict = employee.to_dict()
        dict_employees.append(employee_dict)
    return dict_employees 

def read_model_by_id(id):
    employee = db.session.query(Employee).filter_by(id = id).first()
    return employee

def read_by_id(id):
    employee = read_model_by_id(id)
    if not employee: #if employee == None:
        return None
    employee_dict = employee.to_dict()   
    return employee_dict 

def update(id, new_employee):
    employee = read_model_by_id(id)
    if not employee:
        return 
    employee.salary = new_employee['salary']
    db.session.commit()

def delete_employee(id):
    employee = read_model_by_id(id)
    if not employee:
        return
    db.session.delete(employee)
    db.session.commit()
    