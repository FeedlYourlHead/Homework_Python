class Student:
    all_students = []
    grades = []

    def __init__(self, name:str, grades:list = None) -> None:
        if grades is None:
            grades = []
        self.name = name
        self.grades = grades 
        Student.all_students.append(self)
        Student.grades.extend(grades)

    def add_student(self):
        name = input("Имя студента: ")
        return Student(name)

    def add_grade(self, grade):
        if self.is_valid_grade(grade):
            self.grades.append(grade)
            Student.grades.append(grade)
        else:
            raise ValueError

    def average_grade(self):
        if not self.grades:
            return 
        return sum(self.grades) / len(self.grades)

    @classmethod
    def show_all_students(cls):
        if not cls.all_students:
            return
        result = ''
        for i, student in enumerate(cls.all_students, 1):
            result += f"{i}){student}\n"
        return result.strip()
    
    @classmethod
    def average_grade_all(cls):
        if not cls.grades:
            return 
        return sum(cls.grades) / len(cls.grades)

    @staticmethod
    def is_valid_grade(grade):
        return isinstance(grade, int) and grade in range(1, 6)


    def __str__(self) -> str:
        return f"Студент:{self.name}, Оценки: {', '.join(str(grade) for grade in self.grades)}"

def main():
    while True:
        try:
            choice = input("""
            1. Добавить нового студента.
            2. Добавить оценки студенту.
            3. Вывести среднюю оценку студента.
            4. Вывести среднюю оценку всех студентов.
            5. Вывести список студентов.
            6. Выход.
            """)
            
            if not choice.isdigit() or int(choice) not in range(1, 7):
                raise ValueError
            
            choice = int(choice)

            if choice == 1:
                temp_student = Student("", []) 
                new_student = temp_student.add_student() 
                Student.all_students.remove(temp_student)
                Student.grades.clear()
                for student in Student.all_students:
                     Student.grades.extend(student.grades)


            elif choice == 2:
                print("Выберите студента, которому вы хотите добавить оценку.")
                print(Student.show_all_students())
                
                student_num_str = input("№ студента: ")
                if not student_num_str.isdigit():
                    raise ValueError("Введите номер студента числом.")
                student_num = int(student_num_str)
                
                if student_num not in range(1, len(Student.all_students) + 1):
                    raise IndexError("Некорректный № студента.")
                    
                
                chosen_student = Student.all_students[student_num - 1] 
                
                grade_str = input(f"Введите оценку для {chosen_student.name} (1-5): ")
                if not grade_str.isdigit():
                    raise ValueError("Оценка должна быть целым числом.")
                grade = int(grade_str)
                chosen_student.add_grade(grade)
                
            elif choice == 3:
                print("Выберите студента, у которого вы хотите посмотреть среднюю оценку.")
                print(Student.show_all_students())
                
                student_num_str = input("№ студента: ")
                if not student_num_str.isdigit():
                    raise ValueError("Введите номер студента числом.")
                student_num = int(student_num_str)
                
                if student_num not in range(1, len(Student.all_students) + 1):
                    raise IndexError("Некорректный № студента.")
                
                avg = Student.all_students[student_num - 1].average_grade()
                print(f"Средняя оценка: {avg}")

            elif choice == 4:
                print(f"Средняя оценка всех студентов - {Student.average_grade_all()}")
            elif choice == 5:
                print(Student.show_all_students())
            elif choice == 6:
                exit()

        except Exception:
            print("Введите коректное значение")    
    
if __name__ == "__main__":
    main()
