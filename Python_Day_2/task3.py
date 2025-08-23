import random as r
list_with_treasure = ['X']
for i in range(9):
    list_with_treasure.append('.')
r.shuffle(list_with_treasure)
attempt = 3
while attempt != 0:
    try:
        user_input = int(input("Введите номер ячейки(от 1 до 10): "))
        if user_input > 0:
            if list_with_treasure[user_input - 1] == 'X':
                print("Поздравяем вы нашли сокровище")
                break
            else:
                attempt -= 1
                print(f"Пусто. Попробуйте снова.(Попыток осталось: {attempt})")
        else:
            print("Введите корректный номер ячейки")
    except (ValueError, IndexError):
        print("Введите число от 1 до 10")

