from abc import ABC, abstractmethod


class Road:
    def __init__(self, length) -> None:
        self.vehicles = []
        self.length = length


class Vehicle(ABC):
    def __init__(self, position) -> None:
        self.acceleration_rate = 0
        self.id = 0
        self.safe_distance = 0
        self.max_speed = 0
        self.speed = 0
        self.position = position

    def move(self):
        self.position += self.speed

    def get_position(self):
        return self.position

    def accelerate(self):
        new_speed = self.speed + self.acceleration_rate
        self.speed = min(new_speed, self.max_speed)

    def decelerate(self):
        new_speed = self.speed - self.acceleration_rate
        self.speed = max(new_speed, 0)

    @abstractmethod
    def decide_action(self, vehicles, length):
        pass

class Car(Vehicle):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.acceleration_rate = 10
        self.safe_distance = 5
        self.max_speed = 230

    def decide_action(self, vehicles, length):
        # Найти ближ. припятствие
        list_of_obstacle = [] #список припятствий
        for vehicle in vehicles:
            if vehicle == self:
                continue
            if vehicle.position > self.position:
                difference_position = vehicle.position - self.position
                list_of_obstacle.append(difference_position)

        if not list_of_obstacle:
            self.accelerate()
            return

        near_obstacle_position = min(list_of_obstacle)

        if near_obstacle_position <= self.safe_distance:
            self.decelerate()
        else:
            self.accelerate()

class Truck(Vehicle):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.acceleration_rate = 5
        self.safe_distance = 15
        self.max_speed = 180

    def decide_action(self, vehicles, length):
        list_of_obstacle = []
        for vehicle in vehicles:
            if vehicle == self:
                continue
            if vehicle.position > self.position:
                difference_position = vehicle.position - self.position
                list_of_obstacle.append(difference_position)

            if not list_of_obstacle:
                self.accelerate()
                return
        near_obstacle_position = min(list_of_obstacle)

        if near_obstacle_position <= self.safe_distance:
            self.decelerate()
        else:
            self.accelerate()

class TrafficFlowSimulator:
    def __init__(self, road) -> None:
        self.road = road

    def add_vehicle(self, vehicle) -> None:
        self.road.vehicles.append(vehicle)

    def run_cycle(self):
        for vehicle in self.road.vehicle:
            vehicle.decide_action(self.road.vehicles, self.road.length)

        for vehicle in self.road.vehicles:
            vehicle.move()

        new_vehicles_list = []
        for vehicle in self.road.vehicles:
            if vehicle.position <= self.road.length:
                new_vehicles_list.append(vehicle)
        self.road.vehicles = new_vehicles_list


