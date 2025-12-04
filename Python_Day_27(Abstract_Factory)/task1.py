from abc import ABC, abstractmethod

#Products =========================================
class Door(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass

class Window(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass

class Wall(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass

class Roof(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass
# =========================================

#Concrete Products =========================================
    #Doors =========================================
class GlassDoor(Door):
    def describe(self):
        return 'Стеклянная раздвижная дверь в современном стиле'

class WoodenDoor(Door):
    def describe(self):
        return 'Деревянная обычная дверь в классическом стиле'

class MassiveDoor(Door):
    def describe(self):
        return 'Массивная дубовая дверь в Викторианском стиле'
    # =========================================

    #Windows =========================================
class PanoramicWindow(Window):
    def describe(self):
        return 'Панорамные окна в современном стиле'

class WoodenWindow(Window):
    def describe(self):
        return 'Деревянные окна со ставнями в классическом стиле'
class ArchedWindow(Window):
    def describe(self):
        return 'Арочные окна с витражами в Викторианском стиле'
    # =========================================

    #Walls =========================================
class GlassWall(Wall):
    def describe(self):
        return 'Стеклянные стены в современном стиле'

class BrickWall(Wall):
    def describe(self):
        return 'Кирпичные стены в классическом стиле'

class StoneWall(Wall):
    def describe(self) -> str:
        return 'Каменные стены с резьбой в Викторианском стиле'
    # =========================================

    #Roofs =========================================
class FlatRoof(Roof):
    def describe(self) -> str:
        return 'Плоские крыша в современном стиле'

class SpanRoof(Roof):
    def describe(self) -> str:
        return 'Двускатная черепичная крыша в классическом стиле'

class MultiSlopeRoof(Roof):
    def describe(self) -> str:
        return 'Сложная многоскатная крыша в Викторианском стиле'
    # =========================================

# =========================================


#Abstract Factory =========================================
class HouseFactory(ABC):
    @abstractmethod
    def create_door(self) -> Door:
        pass

    @abstractmethod
    def create_window(self) -> Window:
        pass

    @abstractmethod
    def create_wall(self) -> Wall:
        pass

    @abstractmethod
    def create_roof(self) -> Roof:
        pass
# =========================================

#Concrete Factory =========================================
class ModernHouseFactory(HouseFactory):
    def create_door(self) -> Door:
        return GlassDoor()

    def create_window(self) -> Window:
        return PanoramicWindow()

    def create_wall(self) -> Wall:
        return GlassWall()

    def create_roof(self) -> Roof:
        return FlatRoof()

class ClassicHouseFactory(HouseFactory):
    def create_door(self) -> Door:
        return WoodenDoor()

    def create_window(self) -> Window:
        return WoodenWindow()

    def create_wall(self) -> Wall:
        return BrickWall()

    def create_roof(self) -> Roof:
        return SpanRoof()

class VictorianHouseFactory(HouseFactory):
    def create_door(self) -> Door:
        return MassiveDoor()

    def create_window(self) -> Window:
        return ArchedWindow()

    def create_wall(self) -> Wall:
        return StoneWall()

    def create_roof(self) -> Roof:
        return MultiSlopeRoof()
# =========================================
class Garage(): #WARNING: Переместить!!!!
    pass

#Product Builder =========================================
class House:
    def __init__(self) -> None:
        self.walls: None | Wall = None
        self.windows = [] 
        self.doors = []
        self.roof: None | Roof = None
        self.has_garage = False

    def display(self):
        print(f'Стены: {self.walls.describe() if self.walls else 'Не построены'}')
        print(f"Окна: {self.windows[0].describe() if self.windows else 'Нет окон'} (установлено {len(self.windows)} шт.)")
        print(f"Двери: {self.doors[0].describe() if self.doors else 'нет дверей'}(установлено {len(self.doors)} шт.)")
        print(f"Крыша: {self.roof.describe() if self.roof else 'Не построена'}")
        print(f"Гараж: {'Да' if self.has_garage else 'Нет'}")

# =========================================

#Abstract Builder =========================================
class HouseBuilder(ABC):
    @abstractmethod
    def build_walls(self):
        pass

    @abstractmethod
    def build_windows(self, count:int):
        pass

    @abstractmethod
    def build_doors(self, count:int):
        pass

    @abstractmethod
    def build_roof(self):
        pass

    @abstractmethod
    def build_garage(self):
        pass

    @abstractmethod
    def get_result(self) -> House:
        pass

# =========================================



#Concrete Builder =========================================
class ConcreteHouseBuilder(HouseBuilder):
    def __init__(self, factory: HouseFactory) -> None:
        self.factory = factory
        self.house = House()

    def build_walls(self):
        self.house.walls = self.factory.create_wall()

    def build_windows(self, count:int):
        for _ in range(count):
            self.house.windows.append(self.factory.create_window())

    def build_doors(self, count:int):
        for _ in range(count):
            self.house.doors.append(self.factory.create_door())

    def build_roof(self):
        self.house.roof = self.factory.create_roof()

    def build_garage(self):
        self.house.has_garage = True

    def get_result(self) -> House:
        return self.house

# =========================================

#Director =========================================
class Director:
    @staticmethod
    def build_simple_house(builder: HouseBuilder):
        builder.build_walls()
        builder.build_windows(2)
        builder.build_doors(1)
        builder.build_roof()

    @staticmethod
    def build_luxury_house(builder:HouseBuilder):
        builder.build_walls()
        builder.build_windows(8)
        builder.build_doors(2)
        builder.build_roof()
        builder.build_garage()

# =========================================
if __name__ == '__main__':
    modern_factory = ModernHouseFactory()
    builder = ConcreteHouseBuilder(modern_factory)
    director = Director()
    print('Вариант А дом по "стандартному проекту"')
    print()
    director.build_luxury_house(builder)
    modern_luxury_house = builder.get_result()
    modern_luxury_house.display()
    print('Вариант B дом вручную')
    print()
    classic_factory = ClassicHouseFactory()
    custom_builder = ConcreteHouseBuilder(classic_factory)
    custom_builder.build_walls()
    custom_builder.build_doors(3)
    custom_builder.build_windows(5)
    custom_builder.build_roof()

    custom_house = custom_builder.get_result()
    custom_house.display()






