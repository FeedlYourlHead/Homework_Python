from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, role):
        self.name = name
        self.role = role

    @abstractmethod
    def work(self):
        pass


