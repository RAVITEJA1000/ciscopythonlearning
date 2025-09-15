
int_str = input("Integer (space separated):")
int_list = [int(i) for i in int_str.split()]

max_number = max(int_list)
min_number = min(int_list)

filename = 'minmax_data.txt'
with open(filename, 'w') as writer:
    writer.write(f'List: {int_list}\n')
    writer.write(f'Max: {max_number}\n')
    writer.write(f'Min: {min_number}')

with open(filename, 'r') as reader:
    integer_list = reader.readline()
    Maximum = reader.readline()
    Minimum = reader.readline()
    print(integer_list)
    print(Maximum)
    print(Minimum)
