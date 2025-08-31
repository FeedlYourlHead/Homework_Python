users = {}
while True:
    try:
        print("""
Список команд:
1.add
2.remove
3.list
4.exit
            """)
        command = int(input("Введите номер команды:"))
        if command not in range(1, 5):
            raise Exception
        elif command == 1:
            full_name = tuple(input("Введите имя и фамилию участника(через пробел):").split())
            interests = set(input("Введите интересы участника, через запятую: ").split(", "))
            users[full_name] = interests
        elif command == 2:
            delete_user = tuple(input("Введите имя и фамилию участника, которого вы хотите удалить(через пробел):").split())
            users.pop(delete_user)
            print(f"Пользователь {delete_user[0]} {delete_user[1]} был успешно удален")
        elif command == 3:
            for user in users.items():
                print(f"Пользователь {user[0][0]} {user[0][1]}, имеет следующие интересы: {user[1]} ")
        elif command == 4:
            exit()
    except Exception:
        print("Введите корректное значение!!!")