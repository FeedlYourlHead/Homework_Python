class PainterBot:
    def __init__(self, name, style, efficiency):
        self.name = name
        self.style = style
        self.efficiency = efficiency

    def __add__(self, other):
        return ComboPainterBot(self, other)


    def paint(self, length):
        return "#"*length

    def __str__(self):
        return f"Бот {self.name} (стиль: {self.style}, эффективность: {self.efficiency})"

class LinePainterBot(PainterBot):
    def __init__(self, name, efficiency=5):
        super().__init__(name, "Линейный", efficiency)

    def paint(self, length):
        return "="*length

class WavePainterBot(PainterBot):
    def __init__(self, name, efficiency=5):
        super().__init__(name, "Волновой", efficiency)

    def paint(self, length):
        result = []
        for i in range(length):
            if i % 2 == 0:
                result.append('~')
            else:
                result.append('-')
        return ''.join(result)

class ComboPainterBot(PainterBot):
    def __init__(self, bot1, bot2):
        combo_name = f"Комбо [{bot1.name} + {bot2.name}]"
        combo_style = "Комбинированный"

        combo_efficiency = min(bot1.efficiency, bot2.efficiency)

        super().__init__(combo_name, combo_style, combo_efficiency)
        self.bot1 = bot1
        self.bot2 = bot2

    def paint(self, length):
        art1 = self.bot1.paint(length)
        art2 = self.bot2.paint(length)
        return f"{art1} | {art2}"


def gallery_exhibition(painter_list, length):
    # result = []
    for bot in painter_list:
        print(f"{bot.name} - {bot.paint(length)}")




# Тест написала нейросеть, остальное написал я. ну, почти:)




if __name__ == "__main__":
    # Создаем базовых ботов
    pixel_bot = PainterBot("Пиксель", "Пиксельный", 8)
    line_bot = LinePainterBot("Линейный", 6)
    wave_bot = WavePainterBot("Волновой", 9)
    
    print("=== БАЗОВЫЕ БОТЫ ===")
    bots = [pixel_bot, line_bot, wave_bot]
    for bot in bots:
        print(bot)
    
    print("\n=== СОЗДАНИЕ КОМБО-БОТОВ ===")
    
    # Создаем комбо-боты с помощью оператора +
    combo1 = pixel_bot + line_bot
    print(f"Создан комбо-бот: {combo1}")
    print(f"Эффективность: {combo1.efficiency}")
    
    combo2 = wave_bot + line_bot
    print(f"Создан комбо-бот: {combo2}")
    print(f"Эффективность: {combo2.efficiency}")
    
    # Можно создавать цепочки комбинаций
    mega_combo = combo1 + combo2
    print(f"Создан мега-комбо-бот: {mega_combo}")
    print(f"Эффективность: {mega_combo.efficiency}")
    
    print("\n=== ВЫСТАВКА РАБОТ ===")
    
    # Собираем всех ботов для выставки
    all_artists = bots + [combo1, combo2, mega_combo]
    
    gallery_exhibition(all_artists, 5)
    
    print("\n=== ПРИМЕРЫ РАЗНЫХ ДЛИН ===")
    
    # Показываем как выглядят рисунки разной длины
    test_lengths = [3, 6, 10]
    
    for length in test_lengths:
        print(f"\nДлина рисунка: {length}")
        print(f"Пиксельный: {pixel_bot.paint(length)}")
        print(f"Линейный: {line_bot.paint(length)}")
        print(f"Комбо: {combo1.paint(length)}")
    
    print("\n=== ТЕСТ ЦЕПОЧКИ КОМБИНАЦИЙ ===")
    
    # Создаем сложную цепочку комбинаций
    artist1 = PainterBot("Абстракционист", "Абстрактный", 7)
    artist2 = LinePainterBot("Геометр", 8)
    artist3 = WavePainterBot("Мореплаватель", 6)
    
    # Цепочка комбинаций: ((A+B)+C)
    chain_combo = (artist1 + artist2) + artist3
    print(f"Цепочка комбинаций: {chain_combo}")
    print(f"Эффективность: {chain_combo.efficiency} (ожидаем 6 - минимальную)")
    print(f"Рисунок: {chain_combo.paint(4)}")

