"""
Уровень 1: Асинхронный трейдер (asyncio)
- Полёты между планетами
- Изменение цен каждые 3 секунды
- Случайные события
"""
import asyncio
import random
import threading
import time
from typing import Optional
from .state import game_state, EventType


class AsyncTrader:
    """Асинхронный трейдер с event loop в отдельном потоке"""

    def __init__(self):
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self._tasks = []

    def start(self):
        """Запустить асинхронный движок в отдельном потоке"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("🚀 AsyncTrader запущен")

    def stop(self):
        """Остановить движок"""
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

    def _run_loop(self):
        """Запустить event loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            # Запускаем все асинхронные задачи
            self.loop.run_until_complete(self._main())
        except Exception as e:
            print(f"AsyncTrader ошибка: {e}")
        finally:
            self.loop.close()

    async def _main(self):
        """Главная корутина"""
        # Создаём задачи
        tasks = [
            asyncio.create_task(self._price_updater()),
            asyncio.create_task(self._event_generator()),
            asyncio.create_task(self._flight_manager()),
        ]
        self._tasks = tasks

        # Ждём пока игра запущена
        while self.running and game_state.game_running:
            await asyncio.sleep(0.1)

        # Отменяем задачи
        for task in tasks:
            task.cancel()

    async def _price_updater(self):
        """Обновление цен каждые 3 секунды"""
        while self.running:
            await asyncio.sleep(3)

            for planet in game_state.planets.values():
                # Цена колеблется ±30% от базовой
                variation = random.uniform(-0.3, 0.3)
                planet.current_price = planet.base_price * (1 + variation)

            game_state.add_event(
                "price_update",
                "📊 Цены на рынках обновились!",
                {"time": time.time()}
            )

    async def _event_generator(self):
        """Генератор случайных событий"""
        while self.running:
            # Событие каждые 10-20 секунд
            await asyncio.sleep(random.uniform(10, 20))

            event = random.choice([
                EventType.METEOR_SHOWER,
                EventType.SOLAR_FLARE,
                EventType.PIRATE_ATTACK,
                EventType.TRADE_BONUS
            ])

            await self._handle_event(event)

    async def _handle_event(self, event: EventType):
        """Обработка события"""
        if event == EventType.METEOR_SHOWER:
            # Метеоритный дождь - урон шахтам
            damage = random.randint(1, 3)
            for mine in list(game_state.mines.values())[:damage]:
                if random.random() < 0.3:
                    mine.is_broken = True
            game_state.add_event(
                "meteor_shower",
                "☄️ Метеоритный дождь! Проверьте шахты!",
                {"damage_chance": damage}
            )
            game_state.stats["events_survived"] += 1

        elif event == EventType.SOLAR_FLARE:
            # Солнечная вспышка - сбой торговли на 5 секунд
            game_state.add_event(
                "solar_flare",
                "🌞 Солнечная вспышка! Связь нестабильна!",
                {"duration": 5}
            )
            await asyncio.sleep(5)
            game_state.clear_event("solar_flare")
            game_state.stats["events_survived"] += 1

        elif event == EventType.PIRATE_ATTACK:
            # Пиратская атака - запускаем защитника
            game_state.add_event(
                "pirate_attack",
                "🏴‍☠️ Пиратская атака! Активирована защита!",
                {"threat_level": random.randint(1, 5)}
            )

        elif event == EventType.TRADE_BONUS:
            # Бонус к торговле
            bonus = random.randint(50, 200)
            game_state.add_credits(bonus)
            game_state.add_event(
                "trade_bonus",
                f"💰 Торговый бонус! Получено {bonus} кредитов!",
                {"bonus": bonus}
            )

    async def _flight_manager(self):
        """Управление полётами корабля"""
        while self.running:
            await asyncio.sleep(0.1)

            ship = game_state.ship
            if ship.is_flying and ship.destination:
                # Обновляем прогресс полёта
                ship.flight_progress += 0.1 / ship.flight_duration

                if ship.flight_progress >= 1.0:
                    # Прибыли
                    ship.location = ship.destination
                    ship.is_flying = False
                    ship.destination = None
                    ship.flight_progress = 0.0

                    game_state.add_event(
                        "arrival",
                        f"🛬 Корабль прибыл на {ship.location}!",
                        {"location": ship.location}
                    )

    def fly_to(self, destination: str) -> dict:
        """Отправить корабль к планете"""
        ship = game_state.ship

        if ship.is_flying:
            return {"success": False, "message": "Корабль уже в полёте!"}

        if destination not in game_state.planets and destination != "station":
            return {"success": False, "message": "Неизвестный пункт назначения!"}

        if destination == ship.location:
            return {"success": False, "message": "Вы уже здесь!"}

        # Вычисляем время полёта
        if destination == "station":
            duration = 2
        else:
            duration = game_state.planets[destination].distance

        ship.is_flying = True
        ship.destination = destination
        ship.flight_duration = duration
        ship.flight_progress = 0.0

        game_state.add_event(
            "departure",
            f"🚀 Корабль отправился к {destination}! ETA: {duration}с",
            {"destination": destination, "duration": duration}
        )

        return {"success": True, "message": f"Курс на {destination}!"}

    def buy_resource(self, resource: str, amount: int) -> dict:
        """Купить ресурс на текущей планете"""
        ship = game_state.ship

        if ship.is_flying:
            return {"success": False, "message": "Нельзя торговать в полёте!"}

        if ship.location == "station":
            return {"success": False, "message": "На станции нельзя покупать!"}

        # Проверяем солнечную вспышку
        if any(e["type"] == "solar_flare" for e in game_state.active_events):
            return {"success": False, "message": "Связь нарушена солнечной вспышкой!"}

        planet = game_state.planets.get(ship.location)
        if not planet or planet.resource.value != resource:
            return {"success": False, "message": f"Этот ресурс не продаётся здесь!"}

        total_cost = planet.current_price * amount
        if not game_state.remove_credits(total_cost):
            return {"success": False, "message": "Недостаточно кредитов!"}

        if ship.get_cargo_total() + amount > ship.cargo_capacity:
            game_state.add_credits(total_cost)  # Возврат
            return {"success": False, "message": "Недостаточно места в трюме!"}

        ship.cargo[resource] = ship.cargo.get(resource, 0) + amount
        game_state.stats["total_trades"] += 1

        return {
            "success": True,
            "message": f"Куплено {amount} {resource} за {total_cost:.2f} кредитов"
        }

    def sell_resource(self, resource: str, amount: int) -> dict:
        """Продать ресурс на текущей планете"""
        ship = game_state.ship

        if ship.is_flying:
            return {"success": False, "message": "Нельзя торговать в полёте!"}

        if ship.location == "station":
            # На станции - выгружаем в хранилище
            if ship.cargo.get(resource, 0) < amount:
                return {"success": False, "message": "Недостаточно ресурса в трюме!"}

            ship.cargo[resource] -= amount
            if ship.cargo[resource] == 0:
                del ship.cargo[resource]
            game_state.add_resource(resource, amount)

            return {"success": True, "message": f"Выгружено {amount} {resource} на станцию"}

        planet = game_state.planets.get(ship.location)
        if not planet:
            return {"success": False, "message": "Неизвестная локация!"}

        if ship.cargo.get(resource, 0) < amount:
            return {"success": False, "message": "Недостаточно ресурса в трюме!"}

        # Цена продажи = 90% от текущей цены покупки
        sell_price = planet.current_price * 0.9 * amount

        ship.cargo[resource] -= amount
        if ship.cargo[resource] == 0:
            del ship.cargo[resource]

        game_state.add_credits(sell_price)
        game_state.stats["total_trades"] += 1

        return {
            "success": True,
            "message": f"Продано {amount} {resource} за {sell_price:.2f} кредитов"
        }

    def load_from_station(self, resource: str, amount: int) -> dict:
        """Загрузить ресурс со станции в трюм"""
        ship = game_state.ship

        if ship.location != "station":
            return {"success": False, "message": "Корабль не на станции!"}

        if game_state.resources.get(resource, 0) < amount:
            return {"success": False, "message": "Недостаточно ресурса на станции!"}

        if ship.get_cargo_total() + amount > ship.cargo_capacity:
            return {"success": False, "message": "Недостаточно места в трюме!"}

        game_state.remove_resource(resource, amount)
        ship.cargo[resource] = ship.cargo.get(resource, 0) + amount

        return {"success": True, "message": f"Загружено {amount} {resource}"}


# Глобальный экземпляр трейдера
async_trader = AsyncTrader()