employees = []

employee =('John', 21, 10000, True)
employees.append(employee)

employee =('Doe', 22, 20000, True)
employees.append(employee)

print(employees)

i = 0
search = 'John'
index = -1
for emp in employees:
    if emp[0] == search:
        index = i
        break
    i += 1

if index == -1:
    print("employee not found")
else:
    search_employee = employees[index]
    print(employees[index])
    salary = float(input('Salary'))
    employee = (search_employee[0], search_employee[1])
    employees[index] = employee
print('after search and update')

employee =('Doe', 22, 20000, True)
employees.append(employee)
print(employees)
employees.pop() 
print(employees)

position = 1
employees.pop(position)
print(employees)