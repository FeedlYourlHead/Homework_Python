from abc import ABC, abstractmethod
from functools import wraps

def log_production(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        print(f"---НАЧАЛО ПРОИЗВОДСТВА: {instance.name}---")
        res = func(*args, **kwargs)
        print(f'---ПРОИЗВОДСТВО ЗАВЕРШЕНО: {instance.name}---')
        return res
    return wrapper

class Resource(ABC):
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValueError("Amount должно быть целым числом")

        if value < 0:
            raise ValueError("Amount не может быть отрицательным")

        self._amount = value

    def __str__(self):
        return f'Resource: {self.name}, amount: {self.amount}'

    def __add__(self, other):
        if self.name != other.name:
            raise TypeError("Не могут быть добавлены разные типы ресурсов")
        return __class__(self.name, self.amount + other.amount)

class Building(ABC):
    def __init__(self, name, storage):
        self.name = name
        self.storage = storage

    @abstractmethod
    def produce(self):
        pass

    @staticmethod
    def calculate_production_cost(type_resource):
        if isinstance(type_resource, str):
            resource_name = type_resource

        else:
            resource_name = type_resource.__name__

        result = 10 if resource_name == 'Food' else 5
        return result

    @classmethod
    def create_initial_setup(cls, name):
        starter_pack = {"Wood": 10,
                        "Food": 5}
        return cls(name, starter_pack)

class Wood(Resource):
    def __init__(self, amount=10):
        super().__init__(name="Wood",amount=amount)

class Food(Resource):
    def __init__(self, amount=5):
        super().__init__(name="Food", amount=amount)

class ResourceLimiter:
    def __init__(self, limit):
        self.limit = limit

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, 0)

    def __set__(self, instance, value):
        if value > self.limit:
            raise ValueError(f'Не может быть присвоено больше предела {self.limit}')
        instance.__dict__[self.name] = value

class Farm(Building):
    max_food = ResourceLimiter(50)
    def __init__(self, name, storage):
        super().__init__(name, storage)

    @log_production
    def produce(self, amount=10):
        # res_name = "Food"
        # curr_food = self.storage.get(res_name, Food(0))
        # storage_limit = self.max_food
        # space_av = storage_limit - curr_food.amount
        # actual_produced = min(amount, space_av)
        # if actual_produced <= 0:
        #     print(f'лимит {self.name} не может произвести food')
        #     return 0
        #
        # new_food = Food(actual_produced)
        # if res_name in self.storage:
        #     self.storage[res_name] = new_food + self.storage[res_name]
        #
        # else:
        #     self.storage[res_name] = new_food
        # print(f'{self.name} произвела {actual_produced} {res_name}')
        # return actual_produced
        res_name = 'Food'

        current_resource = self.storage.get(res_name)
        if current_resource is None:
            current_amount = 0

        else:
            current_amount = current_resource.amount


        storage_limit = self.max_food

        space_available = storage_limit - current_amount
        actual_produced = min(amount, space_available)

        if actual_produced <= 0:
            print(f'Лимит {self.name} достигнут, не может произвести food')
            return 0

        new_food = Food(actual_produced)
        if res_name in self.storage:
            self.storage[res_name] = new_food + self.storage[res_name]

        else:
            self.storage[res_name] = new_food

        print(f'{self.name} произвела {actual_produced} {res_name}')
        return actual_produced


class LumberMill(Building):
    max_wood = ResourceLimiter(50)
    def __init__(self, name, storage):
        super().__init__(name, storage)

    @log_production
    def produce(self, amount=5):
        res_name = 'Wood'
        curr_wood = self.storage.get(res_name, Wood(0))
        storage_limit = self.max_wood
        space_av = storage_limit - curr_wood.amount
        actual_produced = min(amount, space_av)
        if actual_produced <= 0:
            print(f'лимит {self.name} не может произвести wood')
            return 0

        new_wood = Wood(actual_produced)
        if res_name in self.storage:
            self.storage[res_name] = new_wood + self.storage[res_name]

        else:
            self.storage[res_name] = new_wood
        print(f'{self.name} произвела {actual_produced} {res_name}')
        return actual_produced


if __name__ == '__main__':
    res_food = Food()
    res_food2 = Food()
    res_wood = Wood()
    farm = Farm("Farm", {'Food': res_food}) #создание экземляра класса Farm
    lumber = LumberMill('Lumber', {'Wood': res_wood}) #создание экземляра класса LumberMill
    # print(res_food+res_food2) #Демонстрация сложения ресурсов
    # try:
    #     res_food.amount = -5
    # except Exception as e:
    #     print(e) #Попытка присвоить отрицательный amount ресурсу

    farm.produce()
    farm.produce()
    farm.produce()
    farm.produce()
    # lumber.produce()
    print(res_food)
    print(res_food2)
    print(res_wood)

    print(farm.calculate_production_cost("Food"))
