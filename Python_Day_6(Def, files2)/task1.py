def word_count(filename):
    """Функция, которая считает количество слов, в файле"""
    with open(f"{filename}", "r", encoding="utf-8") as f:
        return len(f.read().split(" "))


def find_word(filename, word):
    """Функция, которая ищет слово"""
    with open(f"{filename}", "r", encoding="utf-8") as f:
        return f.read().lower().count(f"{word.lower()}")


def save_statistics(filename):
    """Функция, которая сохраняет статистику по словам в файле"""
    stop_words = ["и", "в", "на", "с"]
    word_counter = {}
    with open(f"{filename}", "r", encoding="utf-8") as f:
        for line in f:
            words = line.lower().split()

            for word in words:
                cleaned_word = "".join(char for char in word if char.isalpha())
                if cleaned_word not in stop_words:
                    word_counter[cleaned_word] = word_counter.get(cleaned_word, 0) + 1

    sorted_words = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(f"Всего, количество слов в книге: {word_count('book.txt')}\n")
        for i in range(0, 5):
            f.write(
                f"Топ {i + 1} слово: '{sorted_words[i][0]}', количество слов:{sorted_words[i][1]}\n"
            )

    return "Статистика успешно сохранена в файле 'stats.txt'(стоп-слова - и, в, на, с исключены)"


word = input("Введите слово, чтобы посчитать его частотность в книге: ")
print(f"Всего, количество слов в книге: {word_count('book.txt')}")
print(
    f'Слово "{word}", встречается в книге, следующее количество раз: {find_word("book.txt", word)}'
)
print(save_statistics("book.txt"))
