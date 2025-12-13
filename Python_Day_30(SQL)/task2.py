import sqlite3

DATABASE = 'BookStore.db'

def create_table_and_add_record():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors(
            AuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT,
            LastName TEXT)
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books(
            BookID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            AuthorID INTEGER,
            Price REAL,
            FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
            )
        ''')
        cursor.execute('''
        INSERT INTO Authors (FirstName, LastName)
        VALUES ('Ivan', 'Ivanov')
        ''')
        cursor.execute('''
        INSERT INTO Books (Title, Price, AuthorID)
        VALUES ('War and piece', 100, 1)
        ''')
        conn.commit()

def delete_record():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM Authors
        ''')
        cursor.execute('''
        DELETE FROM Books
        ''')
        conn.commit()

if __name__ == '__main__':
    while True:
        try:
            print('''
1)Создать таблицу и добавить тестовую запись.
2)Удалить записи, сохранив таблицу.
3)Выход.
            ''')
            choice = input('~>')
            if choice == '1':
                create_table_and_add_record()
            elif choice == '2':
                delete_record()
            elif choice == '3':
                break
            else:
                print('Введите корректное значение!!')
        except Exception:
            pass