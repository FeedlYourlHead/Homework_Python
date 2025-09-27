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
    def work(self, task):
        return f"Разрабатываю программу"

class Tester(Employee):
    def work(self, task):
        return f"Тестирую программу"

class Manager(Employee):
    def work(self, task):
        return f"Управляю командой"

class LeadDeveloper(Developer, Manager):
    pass

class Task:
    def __init__(self, task, emloyee) -> None:
        self.task = task
        self.emloyee = emloyee

class Project:
    def __init__(self, tasks, emloyees) -> None:
        self.tasks = tasks
        self.emloyees = emloyees
