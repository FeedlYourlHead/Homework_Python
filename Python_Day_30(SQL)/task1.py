import sqlite3

DATABASE = 'movie.sqlite'

def task1():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        data = cursor.execute('''
        SELECT * FROM IMDB
        ''')
        column_names = [description for description in cursor.description]
        data_fetch = data.fetchall()
        for i in range(len(data_fetch)):
            for j in range(len(column_names)):
                print(f'{column_names[j][0]} - {data_fetch[i][j]}')
            print('==========================')

def task2():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        data = cursor.execute('''
        SELECT Title, Rating FROM IMDB 
        WHERE Rating > 8
        ORDER BY Rating DESC
        ''')
        column_names = [description for description in cursor.description]
        data_fetch = data.fetchall()
        for i in range(len(data_fetch)):
            for j in range(len(column_names)):
                print(f'{column_names[j][0]} - {data_fetch[i][j]}')
            print('==========================')

def task3():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        data = cursor.execute('''
        SELECT DISTINCT genre
        FROM genre
        ''')
        column_names = [description for description in cursor.description]
        data_fetch = data.fetchall()
        for i in range(len(data_fetch)):
            for j in range(len(column_names)):
                print(f'{column_names[j][0]} - {data_fetch[i][j]}')
            print('==========================')

def task4():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        data = cursor.execute('''
        SELECT * FROM IMDB
        WHERE Rating > 8.5
        ORDER BY Rating DESC
        ''')
        column_names = [description for description in cursor.description]
        data_fetch = data.fetchall()
        for i in range(len(data_fetch)):
            for j in range(len(column_names)):
                print(f'{column_names[j][0]} - {data_fetch[i][j]}')
            print('==========================')

def task5():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        data = cursor.execute('''
        SELECT Title, Runtime FROM IMDB
        WHERE Runtime == "120 min"  
        ''')
        column_names = [description for description in cursor.description]
        data_fetch = data.fetchall()
        for i in range(len(data_fetch)):
            for j in range(len(column_names)):
                print(f'{column_names[j][0]} - {data_fetch[i][j]}')
            print('==========================')


if __name__ == '__main__':
    while True:
        try:
            print('''
1)Задание 1 (вывод всех данных)
2)Задание 2 (все фильмы с рейтингом 8 и выше и сортировка по убыванию)
3)Задание 3 (все жанры)
4)Задание 4 (вся информация по фильмам с рейтингом 8.5)
5)Задание 5 (все фильмы длительностью 120 минут)
6)Выход
            ''')
            choice = input('Выберите задание: ')
            if choice == '1':
                task1()
            elif choice == '2':
                task2()
            elif choice == '3':
                task3()
            elif choice == '4':
                task4()
            elif choice == '5':
                task5()
            elif choice == '6':
                break
            else:
                print('Попробуйте еще раз')
        except Exception:
            pass
