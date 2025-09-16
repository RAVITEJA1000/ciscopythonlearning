"""
    Consuming Employees Management APIs 
    - Consumer Employee App 
    - Employee Client / Frontend App 

    API REPO
"""

import requests # pip install requests  

BASE_URL = "http://127.0.0.1:5000"

def create_employee(employee):
    url = f'{BASE_URL}/employees'
    response = requests.post(url, json = employee)
    createdEmployee_dict = response.json()
    return createdEmployee_dict

def read_all_employee():
    url = f'{BASE_URL}/employees'
    response = requests.get(url)
    dict_employees = response.json()
    return dict_employees 

def read_by_id(id):
    url = f'{BASE_URL}/employees/{id}'
    response = requests.get(url)
    employee_dict = response.json() 
    return employee_dict 

def update(id, new_employee):
    url = f'{BASE_URL}/employees/{id}'
    response = requests.put(url, json=new_employee)
    updateEmployee_dict = response.json() 
    return updateEmployee_dict
    
def delete_employee(id):
    url = f'{BASE_URL}/employees/{id}'
    response = requests.delete(url)
    message_dict = response.json() 
    return message_dict
    