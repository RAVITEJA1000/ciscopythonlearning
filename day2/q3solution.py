sentence = input('Enter the sentence: ')
words_list = sentence.split()
print(words_list)
words_tuple = [words.upper() for words in words_list]
print(words_tuple)

filename = 'sentence_data.txt'
with open(filename, 'w') as writer:
    writer.write(f'List: {words_list}\n')
    writer.write(f'Tuple: {words_tuple}')

with open(filename, 'r') as reader:
    List = reader.readline()
    Tuple = reader.readline()
    print(List)
    print(Tuple)