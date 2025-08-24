import random as r
words = ['python', 'список', 'цикл', 'игра', 'число']

random_word = r.choice(words)
shuffe_word = list(random_word)
r.shuffle(shuffe_word)
print(f"Отгадайте слово: {''.join(shuffe_word)}")
user_input = input("Введите ваше слово: ")
if user_input == random_word:
    print("Верно")
else:
    print(f"Неверно, правильное слово {random_word}")