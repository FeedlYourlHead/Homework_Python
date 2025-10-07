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
        return f"Разрабатываю код, до окончания задания '{task.task}' осталось: {task.condition}"

class Tester(Employee):
    def __init__(self, name):
        super().__init__(name, role="Tester")
    def work(self, task):
        task.condition -= 1
        if task.condition == 0:
            self.completed_tasks += 1
            return "Работа окончена"
        return f"Тестирую код, до окончания задания '{task.task}' осталось: {task.condition}"

class Manager(Employee):
    def __init__(self, name):
        super().__init__(name, role="Manager")

    def work(self, task):
        task.condition -= 1
        if task.condition == 0:
            self.completed_tasks += 1
            return "Работа окончена"
        return f"Управляю командой, до окончания задания '{task.task}' осталось: {task.condition}"

class LeadDeveloper(Developer, Manager):
    def __init__(self, name, command:list):
        Employee.__init__(self, name, role="LeadDeveloper") #Не смог здесь использовать метод super(), возникал конфликт множественного наследования
        self.command = command

    def work(self, task):
        task.condition -= 1
        if task.condition == 0:
            self.completed_tasks += 1
            return "Работа окончена"

        manager_work = f"Управляю командой, до окончания задания '{task.task}' осталось: {task.condition}"
        developer_work = f"Разрабатываю код, до окончания задания '{task.task}' осталось: {task.condition}"
        return f"{manager_work}\n{developer_work}"

class Task:
    def __init__(self, task:str, employee:Employee) -> None:
        self.task = task
        self.employee = employee
        self.condition = 3

class Project:
    def __init__(self) -> None:
        self.task = []
        self.employee = []

    def add_task(self, task):
        self.task.append(task)
        return f"Задание '{task.task}', было добавлено в проект."

    def add_employee(self, employee):
        self.employee.append(employee)
        return f"Сотрудник '{employee.name}' был добавлен в проект."

    def __str__(self) -> str:
        lst_e = [f'{i+1}){x.name} - {x.role}' for i,x in enumerate(self.employee)]
        lst_t = [f'{i+1}){x.task}' for i,x in enumerate(self.task)]
        return f"Информация по проекту:\nЗадействованные сотрудники:\n{'\n'.join(str(x) for x in lst_e)}\nЗадания проекта:\n{'\n'.join(str(x) for x in lst_t)}"

def main():
    tester = Tester("Anton")
    develop = Developer("Boris")
    manager = Manager("Ivan")
    lead = LeadDeveloper("Petr",[tester, develop, manager])
    task_tester = Task("Протестировать фичу", tester)
    task_develop = Task("Разработать фичу", develop)
    task_develop2 = Task("Разработать еще одну фичу", develop)
    task_manager = Task("Управлять сотрудниками", manager)
    task_lead = Task("Делать работу ТимЛида", lead)
    print("Проверка методов work")
    for _ in range(3):
        print(develop.work(task_develop))
    print("--------------------------------")
    for _ in range(3):
        print(develop.work(task_develop2))
    print("--------------------------------")
    for _ in range(3):
        print(tester.work(task_tester))
    print("--------------------------------")
    for _ in range(3):
        print(manager.work(task_manager))
    print("--------------------------------")
    for _ in range(3):
        print(lead.work(task_lead))
    print("--------------------------------")
    proj = Project()
    print(proj.add_employee(tester))
    print(proj.add_task(task_tester))
    print("--------------------------------")
    print(proj.add_employee(manager))
    print(proj.add_task(task_manager))
    print("--------------------------------")
    print(proj.add_employee(develop))
    print(proj.add_task(task_develop))
    print(proj.add_task(task_develop2))
    print("--------------------------------")
    print(proj.add_employee(lead))
    print(proj.add_task(task_lead))
    print("--------------------------------")
    print(proj)
    print("--------------------------------")
    print("Проверка перегрузки операторов")
    print(tester < develop)
    print(lead == manager)
    print(lead > develop)

if __name__ == "__main__": 
    main()
