tasks = []
while True:
    try:
        choice = int(input("""
        Выберите команду:
        1.add
        2.remove
        3.list
        4.exit
        ~:"""))
        if choice == 1:
            task = input("Название задачи: ")
            tasks.append(task)
            print("------------------------------------------")
            print(f'Задача "{task}" была добавлена!')
            print("------------------------------------------")
        elif choice == 2:
            while True:
                try:
                    if len(tasks) == 0:
                        print("Список пуст!!!")
                        break
                    index = int(input("Введите индекс задачи, который вы хотите удалить: "))
                    print("------------------------------------------")
                    print(f'Задача "{tasks.pop(index)}" была удалена!!!')
                    print("------------------------------------------")
                    break
                except (IndexError, ValueError):
                    print("Введите корректный индекс!!!")
                    continue
        elif choice == 3:
            print("------------------------------------------")
            for i in range(len(tasks)):
                print(f"{i}.{tasks[i]}")
            print("------------------------------------------")
        elif choice == 4:
            print("------------------------------------------")
            print("До свидания!")
            print("------------------------------------------")
            exit()
    except (TypeError, ValueError):
        print("Введите коректное значение!!!")