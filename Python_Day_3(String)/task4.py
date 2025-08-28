from random import randint
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits,

num = int(input("Введите длину вашего пароля: "))
if num < 4:
    print("Пароль должен быть больше 4 символов")
else:
    result = ""
    for i in range(num):
        num = randint(48, 122)
        char = chr(num)
        result += char
    print(ascii_lowercase)

