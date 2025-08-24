counter = 0
while True:
    try:
        days_of_week = int(input("Введите количество дней: "))
        if days_of_week <= 0 or days_of_week > 7:
            print("Введите  число от 1 до 7")
            continue
        break
    except ValueError:
        print('Введите целое число')

for day in range(1, days_of_week + 1):
    while True:
        try:
            hours_in_day = int(input(f"Введите количество часов для дня №{day}: "))
            if hours_in_day < 0 or hours_in_day > 24:
                print("Число должно быть больше 0 и меньше 24 !!!")
                continue
            counter += hours_in_day
            break
        except ValueError:
            print('Введите целое число')
print(f"Общее количество часов за следующее количество дней - {days_of_week}, равняется {counter}")