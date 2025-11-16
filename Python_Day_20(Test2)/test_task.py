# test_traffic_simulator.py
import pytest
from task1 import Road, Vehicle, Car, Truck, TrafficFlowSimulator


class TestVehicle:
    def test_acceleration_within_max_speed(self):
        """Тест ускорения в пределах максимальной скорости"""
        car = Car(position=0)
        car.speed = 50
        car.acceleration_rate = 10
        car.max_speed = 100
        
        car.accelerate()
        assert car.speed == 60
    
    def test_acceleration_exceeds_max_speed(self):
        """Тест ускорения выше максимальной скорости"""
        car = Car(position=0)
        car.speed = 95
        car.acceleration_rate = 10
        car.max_speed = 100
        
        car.accelerate()
        assert car.speed == 100
    
    def test_movement(self):
        """Тест движения транспортного средства"""
        car = Car(position=0)
        car.speed = 30
        
        car.move()
        assert car.position == 30
        
        car.move()
        assert car.position == 60


class TestCarAndTruckDecision:
    def test_car_accelerates_on_free_road(self):
        """Car ускоряется на свободной дороге"""
        car = Car(position=0)
        car.speed = 50
        initial_speed = car.speed
        
        # Пустая дорога
        vehicles = [car]
        road_length = 1000
        
        car.decide_action(vehicles, road_length)
        assert car.speed > initial_speed
    
    def test_car_decelerates_with_obstacle(self):
        """Car замедляется при наличии препятствия"""
        car1 = Car(position=0)
        car2 = Car(position=10)  # Препятствие близко впереди
        car1.speed = 50
        initial_speed = car1.speed
        
        vehicles = [car1, car2]
        road_length = 1000
        
        car1.decide_action(vehicles, road_length)
        assert car1.speed < initial_speed
    
    def test_truck_more_cautious_than_car(self):
        """Truck более осторожен, чем Car (замедляется на большей дистанции)"""
        # Создаем грузовик и машину на одинаковых позициях
        truck = Truck(position=0)
        car = Car(position=0)
        
        # Препятствие на дистанции 12 (между safe_distance грузовика и машины)
        obstacle = Car(position=12)
        
        vehicles_with_truck = [truck, obstacle]
        vehicles_with_car = [car, obstacle]
        road_length = 1000
        
        # Truck должен замедлиться (safe_distance = 15)
        truck_initial_speed = truck.speed
        truck.decide_action(vehicles_with_truck, road_length)
        truck_decelerated = truck.speed < truck_initial_speed
        
        # Car должен ускориться (safe_distance = 5)
        car_initial_speed = car.speed
        car.decide_action(vehicles_with_car, road_length)
        car_accelerated = car.speed > car_initial_speed
        
        assert truck_decelerated and car_accelerated


class TestRoad:
    def test_vehicle_addition(self):
        """Тест добавления транспортного средства на дорогу"""
        road = Road(length=1000)
        car = Car(position=0)
        
        road.vehicles.append(car)
        assert len(road.vehicles) == 1
        assert car in road.vehicles
    
    def test_vehicle_removal_at_road_end(self):
        """Тест удаления машины при достижении конца дороги"""
        road = Road(length=100)
        car = Car(position=95)
        car.speed = 10
        
        road.vehicles = [car]
        simulator = TrafficFlowSimulator(road)
        
        # После движения машина окажется за пределами дороги
        simulator.run_cycle()
        assert len(road.vehicles) == 0


class TestTrafficFlowSimulator:
    def test_decision_then_movement_sequence(self):
        """Тест последовательности: сначала принятие решений, затем движение"""
        road = Road(length=1000)
        car = Car(position=0)
        car.speed = 0
        car.acceleration_rate = 10
        
        road.vehicles = [car]
        simulator = TrafficFlowSimulator(road)
        
        # Запускаем цикл
        simulator.run_cycle()
        
        # После цикла машина должна иметь скорость (приняла решение ускориться)
        # и переместиться (позиция изменилась)
        assert car.speed > 0
        assert car.position > 0
    
    def test_end_to_end_cycle_with_two_vehicles(self):
        """Сквозной тест цикла с двумя машинами"""
        road = Road(length=500)
        
        # Быстрая машина сзади
        fast_car = Car(position=0)
        fast_car.speed = 80
        fast_car.acceleration_rate = 15
        
        # Медленная машина впереди
        slow_car = Car(position=50)
        slow_car.speed = 30
        slow_car.acceleration_rate = 10
        
        road.vehicles = [fast_car, slow_car]
        simulator = TrafficFlowSimulator(road)
        
        # Сохраняем начальные состояния
        initial_fast_position = fast_car.position
        initial_fast_speed = fast_car.speed
        initial_slow_position = slow_car.position
        
        # Запускаем цикл
        simulator.run_cycle()
        
        # Проверяем логичные результаты:
        # 1. Обе машины переместились
        assert fast_car.position > initial_fast_position
        assert slow_car.position > initial_slow_position
        
        # 2. Быстрая машина могла замедлиться из-за медленной впереди
        # или продолжить движение с учетом безопасной дистанции
        assert fast_car.speed <= fast_car.max_speed
        assert slow_car.speed <= slow_car.max_speed


class TestEdgeCases:
    def test_vehicle_at_road_start(self):
        """Тест машины в начале дороги"""
        road = Road(length=200)
        car = Car(position=0)
        car.speed = 20
        
        road.vehicles = [car]
        simulator = TrafficFlowSimulator(road)
        
        simulator.run_cycle()
        assert car.position == 20
        assert len(road.vehicles) == 1
    
    def test_vehicle_exactly_at_road_end(self):
        """Тест машины точно в конце дороги"""
        road = Road(length=100)
        car = Car(position=100)
        car.speed = 10
        
        road.vehicles = [car]
        simulator = TrafficFlowSimulator(road)
        
        simulator.run_cycle()
        # Машина должна быть удалена, так как position (110) > length (100)
        assert len(road.vehicles) == 0
    
    def test_multiple_vehicles_removal(self):
        """Тест удаления нескольких машин одновременно"""
        road = Road(length=50)
        
        car1 = Car(position=40)
        car1.speed = 20  # Окажется на позиции 60 - за пределами
        
        car2 = Car(position=10)
        car2.speed = 10  # Окажется на позиции 20 - в пределах
        
        road.vehicles = [car1, car2]
        simulator = TrafficFlowSimulator(road)
        
        simulator.run_cycle()
        assert len(road.vehicles) == 1
        assert car2 in road.vehicles


if __name__ == "__main__":
    pytest.main([__file__, "-v"])