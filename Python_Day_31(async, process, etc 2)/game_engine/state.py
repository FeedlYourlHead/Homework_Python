"""
Модуль состояния игры - центральное хранилище всех данных
"""
import threading
import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class ResourceType(Enum):
    IRON = "iron"
    GOLD = "gold"
    CRYSTAL = "crystal"
    URANIUM = "uranium"


class EventType(Enum):
    METEOR_SHOWER = "meteor_shower"
    SOLAR_FLARE = "solar_flare"
    PIRATE_ATTACK = "pirate_attack"
    TRADE_BONUS = "trade_bonus"


@dataclass
class Planet:
    name: str
    resource: ResourceType
    base_price: float
    current_price: float = 0
    distance: int = 1  # Время полёта в секундах

    def __post_init__(self):
        self.current_price = self.base_price


@dataclass
class Ship:
    location: str = "station"  # station или название планеты
    is_flying: bool = False
    destination: Optional[str] = None
    flight_progress: float = 0.0
    flight_duration: float = 0.0
    cargo: Dict[str, int] = field(default_factory=dict)
    cargo_capacity: int = 100

    def get_cargo_total(self) -> int:
        return sum(self.cargo.values())


@dataclass
class Mine:
    name: str
    mine_type: str  # energy, deep, experimental
    level: int = 1
    is_working: bool = False
    is_broken: bool = False
    production_rate: float = 1.0
    break_chance: float = 0.0
    resource_per_cycle: int = 1
    cycle_time: float = 1.0  # секунды
    total_mined: int = 0


class GameState:
    """Потокобезопасное состояние игры"""

    def __init__(self):
        self._lock = threading.RLock()
        self.reset()

    def reset(self):
        with self._lock:
            # Ресурсы на станции
            self.resources = {
                ResourceType.IRON.value: 50,
                ResourceType.GOLD.value: 20,
                ResourceType.CRYSTAL.value: 10,
                ResourceType.URANIUM.value: 5
            }

            # Деньги
            self.credits = 1000

            # Планеты
            self.planets = {
                "Mars": Planet("Mars", ResourceType.IRON, 10, distance=3),
                "Venus": Planet("Venus", ResourceType.GOLD, 50, distance=5),
                "Europa": Planet("Europa", ResourceType.CRYSTAL, 100, distance=7),
                "Titan": Planet("Titan", ResourceType.URANIUM, 200, distance=10)
            }

            # Корабль
            self.ship = Ship()

            # Шахты
            self.mines = {
                "energy": Mine("Энерго-шахта", "energy",
                               production_rate=2.0, resource_per_cycle=1,
                               cycle_time=1.0, break_chance=0.01),
                "deep": Mine("Глубинная шахта", "deep",
                             production_rate=0.3, resource_per_cycle=5,
                             cycle_time=5.0, break_chance=0.02),
                "experimental": Mine("Экспериментальная", "experimental",
                                     production_rate=1.0, resource_per_cycle=3,
                                     cycle_time=2.0, break_chance=0.15)
            }

            # События
            self.active_events: List[dict] = []
            self.event_log: List[dict] = []

            # Статистика
            self.stats = {
                "total_trades": 0,
                "total_mined": 0,
                "pirates_defeated": 0,
                "events_survived": 0
            }

            # Аналитика (результаты от процессов)
            self.analytics = {
                "best_route": None,
                "price_predictions": {},
                "battle_result": None
            }

            self.game_running = True
            self.start_time = time.time()

    def add_resource(self, resource: str, amount: int) -> bool:
        with self._lock:
            if resource in self.resources:
                self.resources[resource] += amount
                return True
            return False

    def remove_resource(self, resource: str, amount: int) -> bool:
        with self._lock:
            if resource in self.resources and self.resources[resource] >= amount:
                self.resources[resource] -= amount
                return True
            return False

    def add_credits(self, amount: float):
        with self._lock:
            self.credits += amount

    def remove_credits(self, amount: float) -> bool:
        with self._lock:
            if self.credits >= amount:
                self.credits -= amount
                return True
            return False

    def add_event(self, event_type: str, message: str, data: dict = None):
        with self._lock:
            event = {
                "type": event_type,
                "message": message,
                "time": time.time(),
                "data": data or {}
            }
            self.active_events.append(event)
            self.event_log.append(event)
            # Храним только последние 50 событий в логе
            if len(self.event_log) > 50:
                self.event_log = self.event_log[-50:]

    def clear_event(self, event_type: str):
        with self._lock:
            self.active_events = [e for e in self.active_events if e["type"] != event_type]

    def get_state_snapshot(self) -> dict:
        """Получить копию состояния для API"""
        with self._lock:
            return {
                "resources": dict(self.resources),
                "credits": round(self.credits, 2),
                "planets": {
                    name: {
                        "name": p.name,
                        "resource": p.resource.value,
                        "current_price": round(p.current_price, 2),
                        "base_price": p.base_price,
                        "distance": p.distance
                    }
                    for name, p in self.planets.items()
                },
                "ship": {
                    "location": self.ship.location,
                    "is_flying": self.ship.is_flying,
                    "destination": self.ship.destination,
                    "flight_progress": round(self.ship.flight_progress, 2),
                    "cargo": dict(self.ship.cargo),
                    "cargo_capacity": self.ship.cargo_capacity,
                    "cargo_total": self.ship.get_cargo_total()
                },
                "mines": {
                    name: {
                        "name": m.name,
                        "type": m.mine_type,
                        "level": m.level,
                        "is_working": m.is_working,
                        "is_broken": m.is_broken,
                        "total_mined": m.total_mined
                    }
                    for name, m in self.mines.items()
                },
                "active_events": list(self.active_events),
                "event_log": list(self.event_log[-10:]),
                "stats": dict(self.stats),
                "analytics": dict(self.analytics),
                "game_time": round(time.time() - self.start_time, 1)
            }


# Глобальный экземпляр состояния
game_state = GameState()