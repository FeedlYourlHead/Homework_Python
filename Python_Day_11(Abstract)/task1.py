from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.completed_tasks = 0

    @abstractmethod
    def work(self, task) -> str:
        """Функция, которая возвращает результат работы сотрудника."""
        pass

    def __eq__(self, other) -> bool:
        if not isinstance(other, Employee):
            return NotImplemented
        return self.completed_tasks == other.completed_tasks

    def __gt__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return self.completed_tasks > other.completed_tasks

    def __lt__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return self.completed_tasks < other.completed_tasks

class Developer(Employee):
    def __init__(self, name):
        super().__init__(name, role="Developer")

    def work(self, task):
        task.condition -= 1
        if task.condition == 0:
            self.completed_tasks += 1
            return "Работа окончена"
        return f"Разрабатываю код, до окончания задания {task.name} осталось: {task.condition}"

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
    def __init__(self, name, command):
        super().__init__(name)
        self.role = "LeadDeveloper"
        self.command = command

    def work(self, task):
        return f""

class Task:
    def __init__(self, task, emloyee) -> None:
        self.task = task
        self.emloyee = emloyee
        self.condition = 3

class Project:
    def __init__(self, tasks, emloyees) -> None:
        self.tasks = tasks #Список экземпляров Task
        self.emloyees = emloyees

def main():
    # lead = LeadDeveloper("Boris")
    # task = Task("Сделать фичу", lead)
    # print(lead.work(task))
    pass

if __name__ == "__main__": 
    main()
