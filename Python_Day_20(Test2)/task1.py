from abc import ABC, abstractmethod


class Road:
    def __init__(self, length) -> None:
        self.vehicles = {}
        self.lane = {"left": 0,
                     "right": 1,
                     "left_length": length,
                     "right_length": length}


class Vehicle(ABC):
    def __init__(self) -> None:
        self.safe_distance = 0
        self.max_speed = 0
        self.speed = 0

    def check_safe_distance(self):
        pass
        
    def overtaking(self): #метод обгона
        pass

    def accelerate(self):
        pass

    @abstractmethod
    def decide_action(self):
        pass

class Car(Vehicle):
    def __init__(self) -> None:
        super().__init__()
        self.safe_distance = 5
        self.max_speed = 230

    def decide_action(self):
        pass

class Truck(Vehicle):
    def __init__(self) -> None:
        super().__init__()
        self.safe_distance = 15
        self.max_speed = 180

    def decide_action(self):
        pass

class TrafficFlowSimulator:
    def __init__(self, road) -> None:
        self.road = road

    def add_vehicle(self, vehicle):
        pass

    def run_cycle(self):
        for vehicle in self.road.vehicle:
            vehicle.decide_action()


