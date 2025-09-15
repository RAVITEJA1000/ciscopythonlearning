names = input('Enter the names: ')
name_list = sorted(names.split())
name_tuple = tuple(name_list)
print(name_tuple)

filename = 'names_data.txt'
with open(filename, 'w') as writer:
    writer.write(f'List: {name_list}\n')
    writer.write(f'Tuple: {name_tuple}')

with open(filename, 'r') as reader:
    Sorted_List = reader.readline()
    Tuple = reader.readline()
    print(Sorted_List)
    print(Tuple)