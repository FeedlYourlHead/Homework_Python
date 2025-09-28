from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, role):
        self.name = name
        self.role = role

    @abstractmethod
    def work(self, task) -> str:
        """Функция, которая возвращает результат работы работника"""
        pass

class Developer(Employee):
    def __init__(self, name):
        super().__init__(name, role="Developer")

    def work(self, task):
        task.condition -= 1
        return  f"Работа окончена" if task.condition == 0 else f"Разрабатываю код, до окончания задания {task.name} осталось: {task.condition}"

class Tester(Employee):
    def __init__(self, name):
        super().__init__(name, role="Tester")
    def work(self, task):
        task.condition -= 1
        return  f"Работа окончена" if task.condition == 0 else f"Тестирую код, до окончания задания {task.name} осталось: {task.condition}"

class Manager(Employee):
    def __init__(self, name):
        super().__init__(name, role="Manager")
    def work(self, task):
        task.condition -= 1
        return  f"Работа окончена" if task.condition == 0 else f"Управляю командой, до окончания задания {task.name} осталось: {task.condition}"

class LeadDeveloper(Developer, Manager):
    def __init__(self, name, role):
        super(Developer).__init__(name)
        super(Manager).__init__(name, role)

class Task:
    def __init__(self, task, emloyee) -> None:
        self.task = task
        self.emloyee = emloyee
        self.condition = 3

class Project:
    def __init__(self, tasks, emloyees) -> None:
        self.tasks = tasks
        self.emloyees = emloyees

# dev = Developer("Boris")
# print(dev.name)
# print(dev.role)


def make_project():
    pass


def main():
    while True:
        try:
            choice = int(input("""Введите номер команды:
            1. Создать проект.
            2. Добавить задачу в проект.
            3. Добавить сотрудника в проект.
            4. Управление сотрудниками.
            5. Выход."""))
            if choice == 1:
                make_project()
            elif choice == 2:
                pass
            elif choice == 5:
                break
        except Exception:
            pass

