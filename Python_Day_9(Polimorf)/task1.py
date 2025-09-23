class Dish:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - цена {self.price}"


class Order:
    def __init__(self, *args):
        self.dishes = args

    def total_price(self):
        return sum(dish.price for dish in self.dishes)

    def __add__(self, other):
        return Order(*(self.dishes + other.dishes))

    def __gt__(self, other):
        return self.total_price() > other.total_price()

    def __str__(self):
        dishes_list = "\n".join(str(dish) for dish in self.dishes)
        return f"Ваш заказ:\n{dishes_list}\nОбщая стоимость: {self.total_price()}"


class MainDish(Dish):
    def __init__(self, name, price, is_vegan):
        super().__init__(name, price)
        self.is_vegan = is_vegan

    def __str__(self):
        veg = "(вегетарианское)" if self.is_vegan else "(не вегетарианское)"
        return f"{super().__str__()}{veg}"


class Dessert(Dish):
    def __init__(self, name, price, hot):
        super().__init__(name, price)
        self.hot = hot

    def __str__(self):
        hot = "(горячий десерт)" if self.hot else "(холодный десерт)"
        return super().__str__() + hot


class Drink(Dish):
    def __init__(self, name, price, is_alchogolic):
        super().__init__(name, price)
        self.is_alchogolic = is_alchogolic

    def __str__(self):
        alc = (
            "(алкогольный напиток)"
            if self.is_alchogolic
            else "(безалкогольный напиток)"
        )
        return super().__str__() + alc


def print_menu(list_dish):
    """Функция, которая печатает заранее составленное меню, чтобы пользователь мог посмотреть, что он хочет выбрать."""
    for index, tup in enumerate(list_dish):
        print(f"{index + 1}){tup[0]} - {tup[1]} рублей.")


def choose_dish():
    """Функция, в которой пользователь выбирает какое блюдо он хочет добавить в заказ."""
    list_main_dished = [
        ("Стейк с картофелем", 1200, False),
        ("Овощное рагу", 900, True),
        ("Красная рыба с рисом", 1400, False),
    ]
    list_desserts = [
        ("Шоколадное мороженое", 400, False),
        ("Шоколадный торт", 600, True),
        ("Чизкейк", 550, False),
    ]
    list_drinks = [
        ("Чай", 200, False),
        ("Красное вино", 800, True),
        ("Кофе", 300, False),
    ]

    choice = int(
        input("""
    Введите, что вы хотите заказать:
    1.Основное блюдо.
    2.Дессерт.
    3.Напиток.
    """)
    )
    if choice not in range(1, 4):
        raise Exception
    elif choice == 1:
        print_menu(list_main_dished)
        return MainDish(*list_main_dished[int(input("Выбор: ")) - 1])
    elif choice == 2:
        print_menu(list_desserts)
        return Dessert(*list_desserts[int(input("Выбор: ")) - 1])
    elif choice == 3:
        print_menu(list_drinks)
        return Drink(*list_drinks[int(input("Выбор: ")) - 1])


def choose_two_orders(list_orders):
    """Вспомогательная функция, в которой пользователь выбирает два заказа, для демонстрации, что объекты класса Order можно складывать и сравнивать"""
    if len(list_orders) < 1:
        raise Exception
    for i, dish in enumerate(list_orders):
        print(f"{i + 1}) {dish}")
    index_1 = int(input("Выберите первый заказ: ")) - 1
    index_2 = int(input("Выберите второй заказ: ")) - 1
    if index_1 not in range(len(list_orders)) or index_2 not in range(len(list_orders)):
        raise Exception
    order_1 = list_orders[index_1]
    order_2 = list_orders[index_2]

    return order_1, order_2


def main():
    """Главная функция"""
    list_orders = []
    while True:
        try:
            choice = int(
                input(""" Введите номер команды:
            1.Сделать заказ.
            2.Суммировать заказы.
            3.Сравнить заказ по стоимости.
            4.Показать список заказов.
            5.Выход.
            """)
            )
            if choice not in range(1, 6):
                raise Exception
            elif choice == 1:
                dish_obj = choose_dish()
                ord_obj = Order(dish_obj)
                list_orders.append(ord_obj)
                print(str(ord_obj) + "\nЗаказ был успешно добавлен!!!")
            elif choice == 2:
                order_1, order_2 = choose_two_orders(list_orders)
                list_orders.remove(order_1)
                list_orders.remove(order_2)
                list_orders.append(order_1 + order_2)
            elif choice == 3:
                order_1, order_2 = choose_two_orders(list_orders)
                if order_1 > order_2:
                    print("Первый заказ стоит дороже второго!")
                else:
                    print("Второй заказ стоит дороже первого!")
            elif choice == 4:
                print("-----------------------------------")
                for i, dish in enumerate(list_orders):
                    print(f"{i + 1}) {dish}\n")
                print("-----------------------------------")
            elif choice == 5:
                break
        except Exception:
            print("Введите корректное значение!!!")


if __name__ == "__main__":
    main()
