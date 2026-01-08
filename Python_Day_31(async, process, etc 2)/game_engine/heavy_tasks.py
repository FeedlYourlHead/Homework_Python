"""
Уровень 3: Тяжёлые задачи (multiprocessing)
- Навигатор: расчёт маршрутов
- Аналитик: предсказание цен
- Защитник: симуляция боя
"""
import multiprocessing as mp
from multiprocessing import Process, Queue, Value
import random
import time
import math
from typing import Dict, List, Optional
from ctypes import c_bool


def navigator_worker(input_queue: Queue, output_queue: Queue, running: Value):
    """Процесс-навигатор: рассчитывает оптимальные маршруты"""
    print("🧭 Навигатор запущен")

    while running.value:
        try:
            task = input_queue.get(timeout=1)
            if task is None:
                break

            planets = task.get("planets", {})
            current_location = task.get("current_location", "station")

            # Алгоритм поиска лучшего маршрута (упрощённый)
            best_route = calculate_best_route(planets, current_location)

            output_queue.put({
                "type": "navigation",
                "result": best_route,
                "timestamp": time.time()
            })

        except Exception:
            continue

    print("🧭 Навигатор остановлен")


def calculate_best_route(planets: Dict, current: str) -> Dict:
    """Вычисление лучшего торгового маршрута"""
    # Имитация сложных вычислений
    time.sleep(0.5)

    if not planets:
        return {"route": [], "profit": 0}

    # Сортируем планеты по потенциальной прибыли
    scored_planets = []
    for name, data in planets.items():
        if isinstance(data, dict):
            price = data.get("current_price", 0)
            base = data.get("base_price", 1)
            distance = data.get("distance", 1)

            # Счёт = отклонение цены / расстояние
            score = abs(price - base) / base / distance
            scored_planets.append((name, score, price, base))

    scored_planets.sort(key=lambda x: x[1], reverse=True)

    best_route = []
    for planet, score, price, base in scored_planets[:3]:
        action = "buy" if price < base else "sell"
        best_route.append({
            "planet": planet,
            "action": action,
            "score": round(score, 3)
        })

    return {
        "route": best_route,
        "estimated_profit": sum(p[1] * 100 for p in scored_planets[:3])
    }


def analyst_worker(input_queue: Queue, output_queue: Queue, running: Value):
    """Процесс-аналитик: предсказывает изменение цен"""
    print("📈 Аналитик запущен")

    price_history: Dict[str, List[float]] = {}

    while running.value:
        try:
            task = input_queue.get(timeout=1)
            if task is None:
                break

            planets = task.get("planets", {})

            predictions = {}
            for name, data in planets.items():
                if isinstance(data, dict):
                    current = data.get("current_price", 0)
                    base = data.get("base_price", 1)

                    # Добавляем в историю
                    if name not in price_history:
                        price_history[name] = []
                    price_history[name].append(current)

                    # Храним только последние 10 значений
                    if len(price_history[name]) > 10:
                        price_history[name] = price_history[name][-10:]

                    # Простой алгоритм предсказания
                    prediction = predict_price(price_history[name], base)
                    predictions[name] = prediction

            output_queue.put({
                "type": "analysis",
                "predictions": predictions,
                "timestamp": time.time()
            })

        except Exception:
            continue

    print("📈 Аналитик остановлен")


def predict_price(history: List[float], base_price: float) -> Dict:
    """Предсказание цены на основе истории"""
    # Имитация сложного ML-алгоритма
    time.sleep(0.3)

    if len(history) < 2:
        return {"trend": "unknown", "confidence": 0, "predicted": base_price}

    # Простой трендовый анализ
    avg_recent = sum(history[-3:]) / min(3, len(history))
    avg_old = sum(history[:-3]) / max(1, len(history) - 3) if len(history) > 3 else history[0]

    trend_strength = (avg_recent - avg_old) / base_price

    if trend_strength > 0.05:
        trend = "up"
    elif trend_strength < -0.05:
        trend = "down"
    else:
        trend = "stable"

    predicted = avg_recent * (1 + trend_strength * 0.5)
    confidence = min(len(history) * 10, 80)  # Максимум 80% уверенности

    return {
        "trend": trend,
        "confidence": confidence,
        "predicted": round(predicted, 2),
        "recommendation": "buy" if trend == "down" else ("sell" if trend == "up" else "hold")
    }


def defender_worker(input_queue: Queue, output_queue: Queue, running: Value):
    """Процесс-защитник: симулирует бой с пиратами"""
    print("🛡️ Защитник запущен")

    while running.value:
        try:
            task = input_queue.get(timeout=1)
            if task is None:
                break

            threat_level = task.get("threat_level", 1)
            defense_power = task.get("defense_power", 5)

            # Симуляция боя
            result = simulate_battle(threat_level, defense_power)

            output_queue.put({
                "type": "battle",
                "result": result,
                "timestamp": time.time()
            })

        except Exception:
            continue

    print("🛡️ Защитник остановлен")


def simulate_battle(threat_level: int, defense_power: int) -> Dict:
    """Симуляция боя с пиратами"""
    # Имитация сложных вычислений
    time.sleep(1)

    rounds = []
    player_hp = 100
    pirate_hp = 50 * threat_level

    round_num = 0
    while player_hp > 0 and pirate_hp > 0 and round_num < 10:
        round_num += 1

        # Атака игрока
        player_damage = random.randint(5, 15) * defense_power
        pirate_hp -= player_damage

        # Атака пиратов
        pirate_damage = random.randint(3, 10) * threat_level
        player_hp -= pirate_damage

        rounds.append({
            "round": round_num,
            "player_damage": player_damage,
            "pirate_damage": pirate_damage,
            "player_hp": max(0, player_hp),
            "pirate_hp": max(0, pirate_hp)
        })

    victory = pirate_hp <= 0
    loot = random.randint(100, 500) * threat_level if victory else 0

    return {
        "victory": victory,
        "rounds": rounds,
        "final_player_hp": max(0, player_hp),
        "loot": loot,
        "threat_level": threat_level
    }


class HeavyTaskManager:
    """Менеджер процессов для тяжёлых задач"""

    def __init__(self):
        self.processes: Dict[str, Process] = {}
        self.input_queues: Dict[str, Queue] = {}
        self.output_queues: Dict[str, Queue] = {}
        self.running = Value(c_bool, False)

    def start_all(self):
        """Запустить все процессы"""
        if self.running.value:
            return

        self.running.value = True

        # Навигатор
        self.input_queues["navigator"] = Queue()
        self.output_queues["navigator"] = Queue()
        self.processes["navigator"] = Process(
            target=navigator_worker,
            args=(self.input_queues["navigator"],
                  self.output_queues["navigator"],
                  self.running)
        )

        # Аналитик
        self.input_queues["analyst"] = Queue()
        self.output_queues["analyst"] = Queue()
        self.processes["analyst"] = Process(
            target=analyst_worker,
            args=(self.input_queues["analyst"],
                  self.output_queues["analyst"],
                  self.running)
        )

        # Защитник
        self.input_queues["defender"] = Queue()
        self.output_queues["defender"] = Queue()
        self.processes["defender"] = Process(
            target=defender_worker,
            args=(self.input_queues["defender"],
                  self.output_queues["defender"],
                  self.running)
        )

        for process in self.processes.values():
            process.start()

        print("🔧 Все процессы запущены")

    def stop_all(self):
        """Остановить все процессы"""
        self.running.value = False

        for queue in self.input_queues.values():
            queue.put(None)

        for process in self.processes.values():
            process.join(timeout=2)
            if process.is_alive():
                process.terminate()

        self.processes.clear()
        self.input_queues.clear()
        self.output_queues.clear()

        print("🔧 Все процессы остановлены")

    def request_navigation(self, planets: Dict, current_location: str):
        """Запросить расчёт маршрута"""
        if "navigator" in self.input_queues:
            self.input_queues["navigator"].put({
                "planets": planets,
                "current_location": current_location
            })

    def request_analysis(self, planets: Dict):
        """Запросить анализ цен"""
        if "analyst" in self.input_queues:
            self.input_queues["analyst"].put({
                "planets": planets
            })

    def request_battle(self, threat_level: int, defense_power: int = 5):
        """Запросить симуляцию боя"""
        if "defender" in self.input_queues:
            self.input_queues["defender"].put({
                "threat_level": threat_level,
                "defense_power": defense_power
            })

    def get_results(self) -> List[Dict]:
        """Получить результаты от всех процессов"""
        results = []

        for name, queue in self.output_queues.items():
            while not queue.empty():
                try:
                    result = queue.get_nowait()
                    results.append(result)
                except:
                    break

        return results


# Глобальный экземпляр
heavy_task_manager = HeavyTaskManager()