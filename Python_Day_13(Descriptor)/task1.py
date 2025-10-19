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
    pass

class BalanceDescriptor(FinancialDescriptor):
    """
    Наследует: FinancialDescriptor
    • Особенности:
    ◦ Запрет отрицательного баланса для дебетовых счетов
    ◦ Разрешение отрицательного баланса для кредитных счетов
    (в пределах лимита)
    ◦ Автоматическая проверка достаточности средств
    """
    pass

class TransactionDescriptor(FinancialDescriptor):
    """
    Наследует: FinancialDescriptor
    • Особенности:
        ◦ Автоматический расчет комиссии (1%)
        ◦ Проверка минимальной суммы транзакции (0.01)
        ◦ Учет комиссии при проверке достаточности средств
    """
    pass

class CategoryDescriptor(FinancialDescriptor):
    """
    Наследует: FinancialDescriptor
    • Особенности:
        ◦ Валидация категорий расходов (фиксированный набор)
        ◦ Контроль месячных лимитов по категориям
        ◦ Метод для установки лимитов категорий
    """
    pass





class FinancialAccount:
    # 2.1. Свойства экземпляра (Properties)
    #     • age_days - количество дней с момента создания счета
    #     • total_commission_paid - общая сумма уплаченных комиссий
    #     • monthly_statistics - статистика за текущий месяц
    # 2.2. Методы класса (Class Methods)
    #     • convert_currency() - конвертация между валютами
    #     • set_exchange_rate() - установка курсов валют
    #     • Статическое свойство: словарь курсов валют
    # 2.3. Статические методы (Static Methods)
    #     • _get_current_timestamp() - получение текущего времени
    # 2.4. Методы экземпляра
    #     • make_transaction() - проведение транзакции с полной валидацией
    #     • deposit() - пополнение счета
    #     • __init__() - инициализация с валидацией параметров
    #     • __str__() - строковое представление объекта

    def __init__(self, age_days, total_commission_paid, monthly_statistics):
        self.age_days = age_days
        self.total_commission_paid = total_commission_paid
        self.monthly_statistics = monthly_statistics

    @classmethod
    def convert_currency(cls):
        pass

    @classmethod
    def set_exchange_rate(cls):
        pass

    @staticmethod
    def _get_current_timestamp():
        pass

    def make_transaction(self):#проведение транзакции с полной валидацией
        pass

    def deposit(self):#пополнение счета
        pass


