class Student:
    all_students = []
    grade = []

    def __new__(cls):
        pass

    def __init__(self, name) -> None:
        self.name = name
        pass

    def add_student(self, name):
        pass



def main():
    while True:
        try:
            choice = int(input("""
            1.Добавить нового студента.
            2.Добавить оценки студенту
            3.Вывести среднюю оценку студента.
            4.Вывести среднюю оценку всех студентов.
            """))
            if choice not in range(1, 5):
                raise Exception
            elif choice == 1:
                pass #Добавить нового студента
            elif choice == 2:
                pass #Добавить оценки студенту
            elif choice == 3:
                pass#Вывести среднюю оценку студента.
            elif choice == 4:
                pass#Вывести среднюю оценку всех студентов.

        except Exception:
            pass
if __name__ == "__main__":
    main()
