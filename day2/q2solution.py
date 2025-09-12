numbers_str = input("numbers :")
numbers_list = [int(num_str) for num_str in numbers_str.split()]
print(numbers_list)
num_sum = sum(numbers_list)
num_avg = num_sum / len(number)

file_name = 'words.text'
with open(file_name,'w') as writer:
    writer.write(f'List:{words_list}\n')
    writer.write(f'Tuple:{words_tuple}')
with open(file_name,'r') as reader:
    line_list = reader.readeline()
    line_tuple=reader.readline()
    print(line_list)
    print(line_tuple)