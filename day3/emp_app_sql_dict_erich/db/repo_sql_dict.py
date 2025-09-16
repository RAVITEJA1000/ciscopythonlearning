from .db_setup import session, Employee 
from .log import logging 
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .exc import EmployeeNotFoundError, EmployeeAlreadyExistError, DatabaseError
#CRUD (Create, Read All | Read One, Update, Delete)
#Employee App - SQL DB - dict element
def create_employee(employee):
    try:
        employee_model = Employee(id = employee['id'],
            name = employee['name'],
            age = employee['age'],
            salary = employee['salary'],
            is_active = employee['is_active'] )
        session.add(employee_model) #INSERT stmt db 
        session.commit() 
        logging.info("employee created.")
    except IntegrityError as ex:
        session.rollback()
        logging.error("Duplicate employee id:%s",ex)
        raise EmployeeAlreadyExistError(f"Employee id={employee['id']} exists already.")
    except SQLAlchemyError as ex:
        session.rollback()
        logging.error("Database error in creating employee:%s",ex)
        raise DatabaseError("Error in creating employee.")
def read_all_employee():
    employees = session.query(Employee).all()
    dict_employees = []
    for employee in employees:
        employee_dict = {'id':employee.id, 
            'name':employee.name,
            'age':employee.age, 'salary':employee.salary,'is_active':employee.is_active}
        dict_employees.append(employee_dict)
    logging.info("read all employees.")
    return dict_employees 
def read_model_by_id(id):
    employee = session.query(Employee).filter_by(id = id).first()
    logging.info("read employee model.")
    return employee

def read_by_id(id):
    employee = read_model_by_id(id)
    if not employee: #if employee == None:
        logging.info(f"employee not found {id}.")
        return None
    employee_dict = {'id':employee.id,
        'name':employee.name,
        'age':employee.age,'salary':employee.salary,'is_active':employee.is_active} 
    logging.info("read employee for given id.")
    return employee_dict 

def update(id, new_employee):
    employee = read_model_by_id(id)
    if not employee:
        logging.info(f"employee not found {id}.")
        return 
    employee.salary = new_employee['salary']
    session.commit()
    logging.info("employee salary updated.")
    
def delete_employee(id):
    employee = read_model_by_id(id)
    if not employee:
        logging.info(f"employee not found {id}.")
        return
    session.delete(employee)
    session.commit()
    logging.info("employee deleted.")
    