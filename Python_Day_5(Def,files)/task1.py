import os

def create_note(name, text):
    """Функция, которая создает заметки"""
    with open(f"notes/{name}.txt", 'w', encoding='utf-8') as f:
        f.write(text)


def view_list_of_notes():
    """Функция просмотра списка заметок"""
    files = os.listdir('notes')
    result = 'Список файлов:\n'
    for file in files:
        result += file + '\n'
    return result


def read_note(note):
    """Функция чтения заметки"""
    with open(f"notes/{note}.txt", encoding="utf-8") as f:
        return "-------\n" + f.read() + "\n-------"


def delete_note(name):
    """Функция удаления заметки"""
    os.remove(f"notes/{name}.txt")
    print(f"Заметка {name} была удалена!!!")
 
if not os.path.exists('notes'):
    os.mkdir('notes')
while True:
    try:
        choice = int(input('''
        1. Создание заметки.
        2. Просмотр списка заметок.
        3. Чтение заметки.
        4. Удаление заметки.
        5. Выйти из программы.
                    '''))
        if choice not in range(1,6):
            raise Exception
        elif choice == 1:
            name = input("Введите название заметки: ")
            if name.endswith(".txt"):
                name = name[:-4]
            text = input("Введите текст заметки: ")
            create_note(name, text)
        elif choice == 2:
            print(view_list_of_notes())
        elif choice == 3:
            name = input("Введите название заметки: ")
            if name.endswith(".txt"):
                name = name[:-4]
            print(read_note(name))
        elif choice == 4:
            name = input("Введите имя файла: ")
            if name.endswith(".txt"):
                name = name[:-4]
            delete_note(name)
        elif choice == 5:
            break

    except Exception:
        print("Введите корректное значение!!!")
