words_str = input("Words (space seperated): ")
words_list = words_str.split()
words_tuple = tuple(words_list)
print(words_str)
print(words_list)
print(words_tuple)

file_name = 'words.txt'
with open(file_name, 'w') as writer:
    writer.write(f'List: {words_list}\n')
    writer.write(f'Tuple: {words_tuple}')

with open(file_name,'r') as reader:
    line_list=reader.readline()
    line_tuple = reader.readline()
    print(line_list)
    print()
    print(line_tuple)