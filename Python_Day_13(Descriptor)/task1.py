import datetime


class FinancialDescriptor:
    """
     Назначение: Базовый дескриптор для всех финансовых атрибутов
     Функциональность:
         Валидация минимальных/максимальных значений
         Ведение истории изменений
        Автоматическое сохранение временных меток
    Атрибуты:
    ◦ name - имя атрибута
    ◦ min_value, max_value - ограничения значений
    ◦ История изменений с timestamp     
    """
    def __init__(self, min_value, max_value) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.name = None
        self.timestamp = {}

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, 0)

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} должно быть числом")

        if value < self.min_value or value > self.max_value:
            raise ValueError("Введено некорректное число")
        
        instance.__dict__[self.name] = value
        self.timestamp[self.name] = datetime.datetime.now()



class BalanceDescriptor(FinancialDescriptor):
    """
    Наследует: FinancialDescriptor
    • Особенности:
    ◦ Запрет отрицательного баланса для дебетовых счетов
    ◦ Разрешение отрицательного баланса для кредитных счетов
    (в пределах лимита)
    ◦ Автоматическая проверка достаточности средств
    """

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} должно быть числом")
        if self.name == "credit":
            if value < self.min_value:
                raise ValueError(f"Кредитный счет не может быть меньше {self.min_value}")

            if value > self.max_value:
                raise ValueError(f"Кредитный счет не может превышать {self.max_value}")

        else:
            if value < 0:
                raise ValueError("Дебетовый счет не может быть отрицательным")

            if value > self.max_value:
                raise ValueError(f"Дебетовый счет не может превышать {self.max_value}")

        instance.__dict__[self.name] = value



class TransactionDescriptor(FinancialDescriptor):
    """
    Наследует: FinancialDescriptor
    • Особенности:
        ◦ Автоматический расчет комиссии (1%)
        ◦ Проверка минимальной суммы транзакции (0.01)
        ◦ Учет комиссии при проверке достаточности средств
    """

    def __set__(self, instance, value):
        commision = 0.01
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} должно быть числом")

        if value < (0.01 - 0.01*commision):
            raise ValueError('Транзакция меньше минимальной суммы(0.01 + коммисия)')

        result = value - value*commision
        instance.__dict__[self.name] = result 



class CategoryDescriptor(FinancialDescriptor):
    """
    Наследует: FinancialDescriptor
    • Особенности:
        ◦ Валидация категорий расходов (фиксированный набор)
        ◦ Контроль месячных лимитов по категориям
        ◦ Метод для установки лимитов категорий
    """
    def __init__(self, min_value, max_value) -> None:
        super().__init__(min_value, max_value)
        self.allowed_categories = ['food', 'transport', 'shopping', 'other']
        self.category_limits = {}

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, dict):
            raise TypeError("Должен быть словарь")

        category = value.get('category')
        amount = value.get('amount')

        if category not in self.allowed_categories:
            raise ValueError(f'Неверная категорияю Допустимо: {self.allowed_categories}')

        if not isinstance(amount, (int, float)):
            raise TypeError('Сумма должна быть числом')

        if category in self.category_limits and amount > self.category_limits[category]:
            raise ValueError(f'Превышен лимит для категории {category}')


        instance.__dict__[self.name] = value

    def set_limit(self, category, limit):
        if category in self.allowed_categories:
            self.category_limits[category] = limit

        else:
            raise ValueError(f"Неверная категория: {category}")




class FinancialAccount:
    """
    2.1. Свойства экземпляра (Properties)
        • age_days - количество дней с момента создания счета
        • total_commission_paid - общая сумма уплаченных комиссий
        • monthly_statistics - статистика за текущий месяц
    2.2. Методы класса (Class Methods)
        • convert_currency() - конвертация между валютами
        • set_exchange_rate() - установка курсов валют
        • Статическое свойство: словарь курсов валют
    2.3. Статические методы (Static Methods)
        • _get_current_timestamp() - получение текущего времени
    2.4. Методы экземпляра
        • make_transaction() - проведение транзакции с полной валидацией
        • deposit() - пополнение счета
        • __init__() - инициализация с валидацией параметров
        • __str__() - строковое представление объекта
    """
    dict_exchange = {
        'USD': 90.1,
        "EUR": 93.4,
        "CNY": 11.3,
        'RUB': 1
    }

    debit = BalanceDescriptor(0, 100000)
    credit = BalanceDescriptor(-5000, 100000)
    transaction = TransactionDescriptor(0, 5000)
    category = CategoryDescriptor(0, 100000)

    def __init__(self):
        self.age_days = datetime.datetime.now()
        self.total_commission_paid = None
        self.monthly_statistics = None

    @classmethod
    def convert_currency(cls, amount, from_currency, to_currency):
        if from_currency not in cls.dict_exchange:
            raise ValueError(f"Неизвестная валюта: {from_currency}")

        if to_currency not in cls.dict_exchange:
            raise ValueError(f"Неизвестная валюта: {to_currency}")

        amount_in_rub = amount * cls.dict_exchange[from_currency]
        converted_amount = amount_in_rub / cls.dict_exchange[to_currency]

        return converted_amount

    @classmethod
    def set_exchange_rate(cls, currency, value):
        if currency not in cls.dict_exchange:
            raise ValueError(f'Неизвестная валюта: {currency}')

        if value <= 0:
            raise ValueError('Курс валюты должен быть положительным')

        cls.dict_exchange[currency] = value
        print(f'Курс {currency} обновлен: {value}')

    @staticmethod
    def _get_current_timestamp():
        pass

    def make_transaction(self):#проведение транзакции с полной валидацией
        pass

    def deposit(self, value, type_acc):#пополнение счета
        self.transaction = value
        if type_acc == "debit":
            self.debit += self.transaction

        elif type_acc == "credit":
            self.credit += self.transaction
        else:
            raise ValueError("Не некорректный вид счета")




    def __str__(self):
        return f"""
Финансовый аккаунт: 
Когда был создан аккаунт: {self.age_days}
Дебетовый счет: {self.debit}
Кредитный счет: {self.credit}

        """


def main():
    account = FinancialAccount()
    print(account.age_days)
    print(account.total_commission_paid)
    print(account.dict_exchange)
    print(account.convert_currency(10000, 'RUB', "USD"))
    print(account)
    print(account.credit)
    account.deposit(500, "debit")
    print(account.debit)
    account.set_exchange_rate("USD", 91.8)
    account.set_exchange_rate("EUR", 99.2)
    account.set_exchange_rate("CNY", 11.8)
    account.set_exchange_rate("RUB", 1)
    print(account.dict_exchange)

    account.category = {'category': "food", 'amount': 3000}
    print(account.category)

    # Задание было сложное, многие вещи мне не понятны, я в принципе понимаю, для чего нужны дескрипторы и как с ними работать, проблема в 
    # этом задании скорее в логике финансового аккаунта, не до конца понятно, как реализовать его некоторые методы и его работу в целом, поэтому отправляю как есть.



if __name__ == "__main__":
    main()
