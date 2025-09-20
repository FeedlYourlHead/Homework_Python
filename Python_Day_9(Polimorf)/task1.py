class Dish:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"Блюдо: {self.name} - цена {self.price}"


class Order:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __add__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __str__(self):
        return f"Ваш заказ: {pass}"


class MainDish(Dish):
    def __init__(self, name, price, is_vegan):
        super().__init__(name, price)
        self.is_vegan = is_vegan


class Dessert(Dish):
    def __init__(self, name, price, type_of):
        super().__init__(name, price)
        self.type_of = type_of


class Drink(Dish):
    def __init__(self, name, price, hot_or_cold):
        super().__init__(name, price)
        self.hot_or_cold = hot_or_cold


def main():
    while True:
        try:
            choice = int(
                input("""
            Введите номер команды:
            1.Сделать заказ.
            2.Суммировать заказы.
            3.Сравнить заказ по стоимости.
            4.Выход.
            """)
            )
            if choice not in range(1,5):
                raise Exception
            elif choice == 1:
                pass
        except Exception:
            print("Введите корректное значение!!!")

if __name__ == "__main__":
    main()
