from random import randint
num = int(input("Введите длину вашего пароля: "))
result = ""
for i in range(num):
    num = randint(48, 122)
    char = chr(num)
    result += char
print(f"Ваш пароль: {result}")
    

