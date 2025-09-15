
from db_setup import session, Employee 

#CRUD (Create, Read All | Read One, Update, Delete)
#Employee App - SQL DB - dict element
def create_employee(employee):
    employee_model = Employee(id = employee['id'],
        name = employee['name'],
        age = employee['age'],
        salary = employee['salary'],
        is_active = employee['is_active'] )
    session.add(employee_model) #INSERT stmt db 
    session.commit() 
def read_all_employee():
    employees = session.query(Employee).all()
    dict_employees = []
    for employee in employees:
        employee_dict = {'id':employee.id, 
            'name':employee.name,
            'age':employee.age, 'salary':employee.salary,'is_active':employee.is_active}
        dict_employees.append(employee_dict)
    return dict_employees 
def read_model_by_id(id):
    employee = session.query(Employee).filter_by(id = id).first()
    return employee

def read_by_id(id):
    employee = read_model_by_id(id)
    if not employee: #if employee == None:
        return None
    employee_dict = {'id':employee.id,
        'name':employee.name,
        'age':employee.age,'salary':employee.salary,'is_active':employee.is_active}    
    return employee_dict 

def update(id, new_employee):
    employee = read_model_by_id(id)
    if not employee:
        return 
    employee.salary = new_employee['salary']
    session.commit()
    
def delete_employee(id):
    employee = read_model_by_id(id)
    if not employee:
        return
    session.delete(employee)
    session.commit()
    
