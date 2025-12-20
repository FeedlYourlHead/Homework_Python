import sqlite3
from pandas import read_sql #pip install pandas

DATABASE = 'University.db'

def task1():
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT g.name as 'Название группы', d.name as 'Название кафедры' FROM Groups as g
        JOIN Departments as d ON g.DepartmentId = d.ID
        ORDER BY d.name
        '''
        print(read_sql(query, conn))
        print('===============================================')
        query = '''
        SELECT g.name as 'Название группы', d.name as 'Название кафедры' FROM Groups as g
        JOIN Departments as d ON g.DepartmentId = d.ID
        ORDER BY g.name
        '''
        print(read_sql(query, conn))

def task2():
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT l.LectureRoom as 'Аудитория', l.ID as 'ID Аудитории', s.Name as 'Название предмета', t.Surname as 'Фамилия преподователя'
        FROM Lectures as l
        INNER JOIN Subjects as s ON l.SubjectId = s.Id 
        INNER JOIN Teachers as t ON l.TeacherId = t.Id
        ORDER BY s.name 
                '''
        print(read_sql(query, conn))

def task3(): #Я так понял тут нет таких
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT c.Name AS 'Имя куратора', c.Surname AS 'Фамилия куратора'
        FROM Curators AS c
        LEFT JOIN GroupsCurators AS gc ON c.ID = gc.CuratorId
        WHERE gc.CuratorID IS NULL
        '''
        print(read_sql(query, conn))

def task4():
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT 
            g.name as "Название группы",
            g.year as "Год обучения",
            d.name as "Название кафедры",
            f.name as "Название факультета"
        FROM Groups as g
        INNER JOIN Departments as d ON g.DepartmentID = d.Id
        INNER JOIN Faculties as f ON d.FacultyId = f.Id
        '''
        print(read_sql(query, conn))

def task5():
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT 
            g.name as "Название группы",
            d.Financing as "Финансирование" 
        FROM Groups AS g
        INNER JOIN Departments as d ON g.DepartmentId = d.Id
        WHERE d.financing > 170000
        '''
        print(read_sql(query, conn))

def task6():
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT
            f.Name as FacultyName,
            COUNT(d.Id) as DepartmentCount
        FROM Faculties as f
        LEFT JOIN Departments as d ON f.Id = d.FacultyId
        GROUP BY f.Id, f.name
        ORDER BY DepartmentCount DESC
        '''
        print(read_sql(query, conn))

def task7():
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT
            c.Name AS CuratorName,
            c.Surname as CuratorSurname,
            g.Name AS GroupName
        FROM Curators as c
        LEFT JOIN GroupsCurators as gc ON c.ID = gc.CuratorId
        LEFT JOIN Groups as g ON gc.GroupId = g.Id
        '''
        print(read_sql(query, conn))

def task8():
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT
            l.Id as Lectureid,
            l.LectureRoom,
            s.Name AS SubjectName
        FROM GROUPS as g
        INNER JOIN GroupsLectures as gl ON g.Id = gl.GroupId
        INNER JOIN Lectures as l ON gl.LectureId = l.Id
        INNER JOIN Subjects as s ON l.SubjectID = s.Id
        WHERE g.Name = 'CS-101'
        ORDER BY l.Id
        '''
        print(read_sql(query, conn))

def task9():
    with sqlite3.connect(DATABASE) as conn:
        query = '''
        SELECT 
            t.Name AS TeacherName,
            t.Surname AS TeacherSurname,
            t.Salary,
            GROUP_CONCAT(s.Name, ', ') AS Subjects
        FROM Teachers as t
        INNER JOIN Lectures as l ON t.Id = l.TeacherId
        INNER JOIN Subjects as s ON l.SubjectId = s.Id
        WHERE t.Salary = (SELECT MAX(Salary) FROM Teachers)
        GROUP BY t.Id, t.Name, t.Surname, t.Salary
        '''
        print(read_sql(query, conn))


if __name__ == '__main__':

    while True:
        choice = input('''
        Выберите задание:
        
1) Вывести список всех групп (их названия) вместе с названиями
кафедр, к которым они относятся. Отсортировать результат по
названию кафедры, а затем по названию группы.

2) Вывести список всех лекций (аудитория и ID) вместе с названием
предмета и фамилией преподавателя, который их ведет.
Отсортировать по названию предмета.

3) Найти всех кураторов, которые не прикреплены ни к одной группе.
Вывести их имя и фамилию.

4)Вывести полную информацию о группах: название группы, год
обучения, название кафедры и название факультета, к которому
относится кафедра.

5) Вывести названия всех групп, которые относятся к кафедрам с
финансированием больше 170 000. Показать название группы и
финансирование ее кафедры.

6) Для каждого факультета посчитать общее количество кафедр на
нем. Вывести название факультета и количество кафедр.
Отсортировать по убыванию количества кафедр.

7) Вывести имена и фамилии всех кураторов и названия групп, за
которые они отвечают. Убедитесь, что отображаются все кураторы,
даже если у них нет групп (и наоборот, но это маловероятно по
структуре данных).

8) Вывести расписание для группы 'CS-101': список всех лекций
(аудитория), которые она посещает, с указанием названия предмета и
времени (предположим, время - это Lectures.Id как порядковый номер).
Отсортировать по времени (Id лекции).

9) Найти преподавателя с самой высокой зарплатой. Вывести его имя,
фамилию, зарплату и перечень названий всех предметов, которые он
ведет.

10) Выход
        
        ''')
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
            task6()
        elif choice == '7':
            task7()
        elif choice == '8':
            task8()
        elif choice == '9':
            task9()
        elif choice == '10':
            break

