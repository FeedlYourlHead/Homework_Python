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

#Builder =========================================
class House:
    def __init__(self, walls, windows, doors, roofs, garage=None) -> None:
        self.walls = walls
        self.windows = windows 
        self.doors = doors
        self.roofs = roofs
        self.garage = garage

    def display(self):
        pass #TODO:Доделать

# =========================================

if __name__ == '__main__':
    wall = GlassWall()
    window = WoodenWindow()
    door = MassiveDoor()
    roof = MultiSlopeRoof()
    house = House(wall, window, door, roof)
    print(house.display())


