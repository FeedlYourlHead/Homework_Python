"""
Уровень 2: Многопоточные шахты (threading)
- 3 типа шахт работают в отдельных потоках
- Ремонт и улучшение во время работы
"""
import threading
import time
import random
from .state import game_state, ResourceType


class MineWorker(threading.Thread):
    """Поток-работник для одной шахты"""

    def __init__(self, mine_id: str):
        super().__init__(daemon=True)
        self.mine_id = mine_id
        self.running = False
        self._stop_event = threading.Event()

    def run(self):
        """Основной цикл работы шахты"""
        mine = game_state.mines[self.mine_id]
        self.running = True

        print(f"⛏️ Шахта {mine.name} запущена")

        while not self._stop_event.is_set() and game_state.game_running:
            if not mine.is_working or mine.is_broken:
                time.sleep(0.5)
                continue

            # Цикл добычи
            time.sleep(mine.cycle_time / mine.level)

            if mine.is_broken:
                continue

            # Проверка поломки
            if random.random() < mine.break_chance * (1 if mine.mine_type != "experimental" else 2):
                mine.is_broken = True
                game_state.add_event(
                    "mine_broken",
                    f"🔧 {mine.name} сломалась!",
                    {"mine_id": self.mine_id}
                )
                continue

            # Добыча ресурса
            resource = self._get_mine_resource()
            amount = mine.resource_per_cycle * mine.level

            game_state.add_resource(resource, amount)
            mine.total_mined += amount
            game_state.stats["total_mined"] += amount

        self.running = False
        print(f"⛏️ Шахта {mine.name} остановлена")

    def _get_mine_resource(self) -> str:
        """Определить какой ресурс добывает шахта"""
        mine_resources = {
            "energy": ResourceType.CRYSTAL.value,  # Энерго-шахта добывает кристаллы
            "deep": ResourceType.URANIUM.value,  # Глубинная - уран
            "experimental": random.choice([  # Экспериментальная - случайный
                ResourceType.GOLD.value,
                ResourceType.CRYSTAL.value,
                ResourceType.URANIUM.value
            ])
        }
        return mine_resources.get(self.mine_id, ResourceType.IRON.value)

    def stop(self):
        """Остановить поток"""
        self._stop_event.set()


class MineManager:
    """Менеджер всех шахт"""

    def __init__(self):
        self.workers: dict[str, MineWorker] = {}
        self._lock = threading.Lock()

    def start_all(self):
        """Запустить все шахты"""
        for mine_id in game_state.mines:
            self.start_mine(mine_id)

    def stop_all(self):
        """Остановить все шахты"""
        with self._lock:
            for worker in self.workers.values():
                worker.stop()
            self.workers.clear()

    def start_mine(self, mine_id: str) -> dict:
        """Запустить конкретную шахту"""
        with self._lock:
            mine = game_state.mines.get(mine_id)
            if not mine:
                return {"success": False, "message": "Шахта не найдена!"}

            if mine.is_broken:
                return {"success": False, "message": "Шахта сломана! Нужен ремонт."}

            if mine_id not in self.workers or not self.workers[mine_id].running:
                worker = MineWorker(mine_id)
                self.workers[mine_id] = worker
                worker.start()

            mine.is_working = True

            return {"success": True, "message": f"{mine.name} запущена!"}

    def stop_mine(self, mine_id: str) -> dict:
        """Остановить конкретную шахту"""
        with self._lock:
            mine = game_state.mines.get(mine_id)
            if not mine:
                return {"success": False, "message": "Шахта не найдена!"}

            mine.is_working = False

            return {"success": True, "message": f"{mine.name} остановлена"}

    def repair_mine(self, mine_id: str) -> dict:
        """Отремонтировать шахту"""
        mine = game_state.mines.get(mine_id)
        if not mine:
            return {"success": False, "message": "Шахта не найдена!"}

        if not mine.is_broken:
            return {"success": False, "message": "Шахта не нуждается в ремонте!"}

        repair_cost = 100 * mine.level
        if not game_state.remove_credits(repair_cost):
            return {"success": False, "message": f"Нужно {repair_cost} кредитов для ремонта!"}

        mine.is_broken = False

        game_state.add_event(
            "mine_repaired",
            f"✅ {mine.name} отремонтирована!",
            {"mine_id": mine_id, "cost": repair_cost}
        )

        return {"success": True, "message": f"{mine.name} отремонтирована за {repair_cost} кредитов!"}

    def upgrade_mine(self, mine_id: str) -> dict:
        """Улучшить шахту"""
        mine = game_state.mines.get(mine_id)
        if not mine:
            return {"success": False, "message": "Шахта не найдена!"}

        if mine.level >= 5:
            return {"success": False, "message": "Максимальный уровень достигнут!"}

        upgrade_cost = 200 * mine.level
        if not game_state.remove_credits(upgrade_cost):
            return {"success": False, "message": f"Нужно {upgrade_cost} кредитов для улучшения!"}

        mine.level += 1
        # Улучшение снижает шанс поломки
        mine.break_chance *= 0.8

        game_state.add_event(
            "mine_upgraded",
            f"⬆️ {mine.name} улучшена до уровня {mine.level}!",
            {"mine_id": mine_id, "new_level": mine.level}
        )

        return {"success": True, "message": f"{mine.name} улучшена до уровня {mine.level}!"}

    def get_status(self) -> dict:
        """Получить статус всех шахт"""
        status = {}
        for mine_id, mine in game_state.mines.items():
            worker = self.workers.get(mine_id)
            status[mine_id] = {
                "name": mine.name,
                "level": mine.level,
                "is_working": mine.is_working,
                "is_broken": mine.is_broken,
                "total_mined": mine.total_mined,
                "thread_alive": worker.is_alive() if worker else False
            }
        return status


# Глобальный экземпляр менеджера шахт
mine_manager = MineManager()