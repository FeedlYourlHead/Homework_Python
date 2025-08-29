from random import shuffle, choice
from string import ascii_lowercase, ascii_uppercase, digits

num = int(input("Введите длину вашего пароля: "))
if num < 4:
    print("Пароль должен быть больше 4 символов")
else:
    result = []
    symbols = '!@#$%^&*()'
    count = 0
    while count < num:
        result.append(choice(ascii_lowercase))
        count += 1
        if count == num:
            break
        result.append(choice(ascii_uppercase))
        count += 1
        if count == num:
            break
        result.append(choice(digits))
        count += 1
        if count == num:
            break
        result.append(choice(symbols))
        count += 1
shuffle(result)
result = ''.join([str(x) for x in result])
print(result)
    

