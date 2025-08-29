check = input("Использовать стандартный набор участников конкурса? (y/n)")
if check == 'y':
    first = {"Петя", "Вова", "Ксюша", "Саша"}
    second = {"Саша", "Андрей", "Максим", "Ксюша", "Вова"}
    third = {"Вова", "Андрей", "Гриша", "Борис"}
else:
    first = set(input("Введите участников первого конкурса(через пробел): ").split())
    second = set(input("Введите участников второго конкурса(через пробел): ").split())
    third = set(input("Введите участников третьего конкурса(через пробел): ").split())

while True:
    try:
        print("""
    ----------------------------------------------------
    1. Узнать, кто участвовал во всех трех конкурсах.
    2. Узнать, кто участвовал хотя бы в одном конкурсе.
    3. Узнать, кто участвовал только в одном конурсе.
    4. Узнать, кто участвовал ровно в двух конкурсах.
    5. Выход.
    ----------------------------------------------------
    """)
        num_operation = int(input("Введите номер операции: "))
        if num_operation not in range(1, 6):
            raise Exception
        elif num_operation == 1:
            print(first & second & third)
        elif num_operation == 2:
            print(first | second | third)
        elif num_operation == 3:
            print((first ^ second ^ third) - (first & second & third) )
        elif num_operation == 4:
            only_1_2 = (first & second) - third
            only_1_3 = (first & third) - second
            only_2_3 = (second & third) - first
            result = only_1_2 | only_1_3 | only_2_3
            print(result)
        elif num_operation == 5:
            break
        
    except Exception:
        print("----------------------------------------------------")
        print("Введите корректное значение")
        print("----------------------------------------------------")




