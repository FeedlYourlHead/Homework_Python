
stop_words = ['и', 'в', 'на', 'с']

def word_count(filename):
    with open(f"{filename}", "r", encoding='utf-8') as f:
        return len(f.read().split(' '))

def find_word(filename, word):
    count = 0
    with open(f"{filename}", 'r', encoding='utf-8') as f:
        for i in f.read().split(' '):
            if i == word:
                count += 1
        return count


def save_statistics(filename):
    pass

print(word_count('book.txt'))
print(find_word('book.txt', 'Франция'))